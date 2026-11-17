"""Conta de quem usa o FeedBerry (UC01 Fazer login, UC02 Criar conta)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, String, event
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from extensions import db

from .enums import Papel
from .tipos import DataHoraUTC, agora_utc, coluna_enum

if TYPE_CHECKING:
    from .equipe import Equipe
    from .feedback import Feedback
    from .lembrete import Lembrete
    from .meta_desenvolvimento import MetaDesenvolvimento


class UsuarioNaoPodeSerApagado(Exception):
    """Usuários não são apagados, só desativados, para o histórico não sumir."""


class Usuario(db.Model):
    __tablename__ = "usuario"
    __table_args__ = (
        # Garante no banco o que o @validates faz na aplicação: e-mail em minúsculas.
        CheckConstraint("email = lower(email)", name="email_minusculo"),
        CheckConstraint("tentativas_login_falhas >= 0", name="tentativas_nao_negativas"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(254), unique=True)
    # Só o hash scrypt (auth/security.py). A senha nunca é guardada.
    senha_hash: Mapped[str] = mapped_column(String(255))
    papel: Mapped[Papel] = mapped_column(coluna_enum(Papel, "papel"), default=Papel.COLABORADOR)
    # use_alter: usuario e equipe apontam uma para a outra (membro e líder).
    equipe_id: Mapped[int | None] = mapped_column(
        ForeignKey("equipe.id", ondelete="SET NULL", use_alter=True)
    )
    ativo: Mapped[bool] = mapped_column(default=True)
    # Base para o bloqueio após 3 tentativas do fluxograma de login (CT05).
    tentativas_login_falhas: Mapped[int] = mapped_column(default=0)
    criado_em: Mapped[datetime] = mapped_column(DataHoraUTC(), default=agora_utc)

    equipe: Mapped[Equipe | None] = relationship(
        back_populates="membros", foreign_keys=[equipe_id]
    )
    # post_update nos dois lados do par lider/equipe_liderada (ver Equipe.lider).
    equipe_liderada: Mapped[Equipe | None] = relationship(
        back_populates="lider", foreign_keys="Equipe.lider_id", post_update=True
    )
    feedbacks_recebidos: Mapped[list[Feedback]] = relationship(
        back_populates="destinatario", foreign_keys="Feedback.destinatario_id"
    )
    feedbacks_escritos: Mapped[list[Feedback]] = relationship(
        back_populates="autor", foreign_keys="Feedback.autor_id"
    )
    metas: Mapped[list[MetaDesenvolvimento]] = relationship(
        back_populates="colaborador", foreign_keys="MetaDesenvolvimento.colaborador_id"
    )
    lembretes_recebidos: Mapped[list[Lembrete]] = relationship(
        back_populates="destinatario", foreign_keys="Lembrete.destinatario_id"
    )

    @validates("email")
    def _normalizar_email(self, _chave, email: str) -> str:
        return email.strip().lower()

    def desativar(self) -> None:
        self.ativo = False

    def __repr__(self) -> str:
        return f"<Usuario {self.id} {self.email} {self.papel.value if self.papel else None}>"


@event.listens_for(Usuario, "before_delete")
def _impedir_exclusao(_mapper, _conexao, usuario: Usuario):
    raise UsuarioNaoPodeSerApagado(
        f"O usuário {usuario.id} não pode ser apagado. Use usuario.desativar()."
    )

"""Feedback (UC03, UC09, UC10, UC12, UC13)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from extensions import db

from .enums import TipoFeedback
from .tipos import DataHoraUTC, agora_utc, coluna_enum

if TYPE_CHECKING:
    from .lembrete import Lembrete
    from .ponto_melhoria import PontoMelhoria
    from .usuario import Usuario


class Feedback(db.Model):
    __tablename__ = "feedback"
    __table_args__ = (
        # Ninguém dá feedback para si mesmo.
        CheckConstraint(
            "autor_id IS NULL OR autor_id <> destinatario_id", name="autor_diferente_destinatario"
        ),
        # Anônimo só do colaborador para o líder (UC13 estende UC12).
        CheckConstraint(
            "NOT anonimo OR tipo = 'COLABORADOR_PARA_LIDER'", name="anonimo_so_para_lider"
        ),
        # Anônimo => sem autor guardado; identificado => com autor. Assim nem
        # quem acessa o banco descobre quem escreveu um feedback anônimo.
        CheckConstraint(
            "(anonimo AND autor_id IS NULL) OR (NOT anonimo AND autor_id IS NOT NULL)",
            name="autor_conforme_anonimato",
        ),
        CheckConstraint("length(trim(conteudo)) > 0", name="conteudo_preenchido"),
        # Consulta de histórico (UC09/UC10): feedbacks de uma pessoa por data.
        Index("ix_feedback_destinatario_id_criado_em", "destinatario_id", "criado_em"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[TipoFeedback] = mapped_column(coluna_enum(TipoFeedback, "tipo_feedback"))
    # RESTRICT: usuários não são apagados, e o histórico não pode sumir junto.
    autor_id: Mapped[int | None] = mapped_column(ForeignKey("usuario.id", ondelete="RESTRICT"))
    destinatario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id", ondelete="RESTRICT"))
    conteudo: Mapped[str] = mapped_column(Text)
    anonimo: Mapped[bool] = mapped_column(default=False)
    criado_em: Mapped[datetime] = mapped_column(DataHoraUTC(), default=agora_utc)

    autor: Mapped[Usuario | None] = relationship(
        back_populates="feedbacks_escritos", foreign_keys=[autor_id]
    )
    destinatario: Mapped[Usuario] = relationship(
        back_populates="feedbacks_recebidos", foreign_keys=[destinatario_id]
    )
    pontos_melhoria: Mapped[list[PontoMelhoria]] = relationship(
        back_populates="feedback", cascade="all, delete-orphan", passive_deletes=True
    )
    lembretes: Mapped[list[Lembrete]] = relationship(
        back_populates="feedback", passive_deletes=True
    )

    def __repr__(self) -> str:
        return f"<Feedback {self.id} {self.tipo.value if self.tipo else None}>"

"""Meta de desenvolvimento de um colaborador (UC05, UC11)."""

from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from extensions import db

from .enums import StatusMeta
from .tipos import DataHoraUTC, agora_utc, coluna_enum

if TYPE_CHECKING:
    from .lembrete import Lembrete
    from .ponto_melhoria import PontoMelhoria
    from .usuario import Usuario


class MetaDesenvolvimento(db.Model):
    __tablename__ = "meta_desenvolvimento"
    __table_args__ = (CheckConstraint("length(trim(titulo)) > 0", name="titulo_preenchido"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    colaborador_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id", ondelete="RESTRICT"), index=True
    )
    # Quem definiu a meta (o líder, no UC05).
    definida_por_id: Mapped[int] = mapped_column(ForeignKey("usuario.id", ondelete="RESTRICT"))
    # A meta pode nascer de um ponto de melhoria. Se o ponto sumir, a meta fica.
    ponto_melhoria_id: Mapped[int | None] = mapped_column(
        ForeignKey("ponto_melhoria.id", ondelete="SET NULL")
    )
    titulo: Mapped[str] = mapped_column(String(150))
    descricao: Mapped[str | None] = mapped_column(Text)
    prazo: Mapped[date | None]
    status: Mapped[StatusMeta] = mapped_column(
        coluna_enum(StatusMeta, "status_meta"), default=StatusMeta.NAO_INICIADA
    )
    criada_em: Mapped[datetime] = mapped_column(DataHoraUTC(), default=agora_utc)
    atualizada_em: Mapped[datetime] = mapped_column(
        DataHoraUTC(), default=agora_utc, onupdate=agora_utc
    )

    colaborador: Mapped[Usuario] = relationship(
        back_populates="metas", foreign_keys=[colaborador_id]
    )
    definida_por: Mapped[Usuario] = relationship(foreign_keys=[definida_por_id])
    ponto_melhoria: Mapped[PontoMelhoria | None] = relationship(back_populates="metas")
    lembretes: Mapped[list[Lembrete]] = relationship(back_populates="meta", passive_deletes=True)

    def __repr__(self) -> str:
        return f"<MetaDesenvolvimento {self.id} {self.titulo!r}>"

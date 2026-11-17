"""Ponto de melhoria registrado em um feedback (UC04, UC07, UC11)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from extensions import db

from .enums import StatusPontoMelhoria
from .tipos import DataHoraUTC, agora_utc, coluna_enum

if TYPE_CHECKING:
    from .feedback import Feedback
    from .meta_desenvolvimento import MetaDesenvolvimento


class PontoMelhoria(db.Model):
    __tablename__ = "ponto_melhoria"
    __table_args__ = (CheckConstraint("length(trim(descricao)) > 0", name="descricao_preenchida"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    # CASCADE: o ponto só existe dentro do feedback que o registrou.
    feedback_id: Mapped[int] = mapped_column(
        ForeignKey("feedback.id", ondelete="CASCADE"), index=True
    )
    descricao: Mapped[str] = mapped_column(Text)
    # O status responde se a pessoa "melhorou no ponto apontado" (Q2-L).
    status: Mapped[StatusPontoMelhoria] = mapped_column(
        coluna_enum(StatusPontoMelhoria, "status_ponto_melhoria"),
        default=StatusPontoMelhoria.ABERTO,
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DataHoraUTC(), default=agora_utc, onupdate=agora_utc
    )

    feedback: Mapped[Feedback] = relationship(back_populates="pontos_melhoria")
    metas: Mapped[list[MetaDesenvolvimento]] = relationship(
        back_populates="ponto_melhoria", passive_deletes=True
    )

    def __repr__(self) -> str:
        return f"<PontoMelhoria {self.id} {self.status.value if self.status else None}>"

"""Equipe: define quem é líder de quem (UC07, UC08)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from extensions import db

from .tipos import DataHoraUTC, agora_utc

if TYPE_CHECKING:
    from .usuario import Usuario


class Equipe(db.Model):
    __tablename__ = "equipe"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), unique=True)
    # Único: uma pessoa lidera no máximo uma equipe. Opcional para permitir
    # criar a equipe antes de escolher o líder.
    lider_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuario.id", ondelete="RESTRICT"), unique=True
    )
    criado_em: Mapped[datetime] = mapped_column(DataHoraUTC(), default=agora_utc)

    # post_update: a equipe e o líder apontam um para o outro, então o
    # SQLAlchemy grava o lider_id em um UPDATE depois de inserir os dois.
    lider: Mapped[Usuario | None] = relationship(
        back_populates="equipe_liderada", foreign_keys=[lider_id], post_update=True
    )
    membros: Mapped[list[Usuario]] = relationship(
        back_populates="equipe", foreign_keys="Usuario.equipe_id"
    )

    def __repr__(self) -> str:
        return f"<Equipe {self.id} {self.nome}>"

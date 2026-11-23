"""Lembrete de retorno sobre um feedback ou uma meta (UC06, UC14).

O envio real (e-mail) fica com o Serviço de notificação, fora da issue #13.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from extensions import db

from .enums import StatusLembrete
from .tipos import DataHoraUTC, coluna_enum

if TYPE_CHECKING:
    from .feedback import Feedback
    from .meta_desenvolvimento import MetaDesenvolvimento
    from .usuario import Usuario


class Lembrete(db.Model):
    __tablename__ = "lembrete"
    __table_args__ = (
        # Todo lembrete é sobre alguma coisa: um feedback, uma meta ou os dois.
        CheckConstraint("feedback_id IS NOT NULL OR meta_id IS NOT NULL", name="tem_vinculo"),
        # Lembrete marcado como enviado precisa da data de envio.
        CheckConstraint(
            "status <> 'ENVIADO' OR enviado_em IS NOT NULL", name="enviado_tem_data"
        ),
        # Busca dos lembretes que vencem (ex.: PENDENTE com data_agendada <= agora).
        Index("ix_lembrete_status_data_agendada", "status", "data_agendada"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    agendado_por_id: Mapped[int] = mapped_column(ForeignKey("usuario.id", ondelete="RESTRICT"))
    destinatario_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id", ondelete="RESTRICT"), index=True
    )
    # CASCADE: lembrete de algo que não existe mais não tem o que lembrar.
    feedback_id: Mapped[int | None] = mapped_column(ForeignKey("feedback.id", ondelete="CASCADE"))
    meta_id: Mapped[int | None] = mapped_column(
        ForeignKey("meta_desenvolvimento.id", ondelete="CASCADE")
    )
    data_agendada: Mapped[datetime] = mapped_column(DataHoraUTC())
    mensagem: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[StatusLembrete] = mapped_column(
        coluna_enum(StatusLembrete, "status_lembrete"), default=StatusLembrete.PENDENTE
    )
    enviado_em: Mapped[datetime | None] = mapped_column(DataHoraUTC())

    agendado_por: Mapped[Usuario] = relationship(foreign_keys=[agendado_por_id])
    destinatario: Mapped[Usuario] = relationship(
        back_populates="lembretes_recebidos", foreign_keys=[destinatario_id]
    )
    feedback: Mapped[Feedback | None] = relationship(back_populates="lembretes")
    meta: Mapped[MetaDesenvolvimento | None] = relationship(back_populates="lembretes")

    def __repr__(self) -> str:
        return f"<Lembrete {self.id} {self.status.value if self.status else None}>"

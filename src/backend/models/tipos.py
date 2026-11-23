"""Tipos de coluna e valores padrão compartilhados pelos modelos."""

import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum
from sqlalchemy.types import TypeDecorator


def agora_utc() -> datetime:
    return datetime.now(timezone.utc)


class DataHoraUTC(TypeDecorator):
    """Data e hora sempre em UTC.

    - Na gravação, converte para UTC. Data sem fuso (naive) é recusada, porque
      não dá para saber se ela estava em UTC ou no horário de Brasília.
    - Na leitura, devolve a data com o fuso UTC, mesmo no SQLite (que não
      guarda fuso).
    """

    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(self, valor, _dialeto):
        if valor is None:
            return None
        if valor.tzinfo is None or valor.utcoffset() is None:
            raise ValueError("Data sem fuso horário. Use uma data com fuso (ex.: agora_utc()).")
        return valor.astimezone(timezone.utc)

    def process_result_value(self, valor, _dialeto):
        if valor is None:
            return None
        if valor.tzinfo is None:
            return valor.replace(tzinfo=timezone.utc)
        return valor.astimezone(timezone.utc)


def coluna_enum(tipo_enum: type[enum.Enum], nome: str) -> Enum:
    """Enum guardado como texto + CHECK, igual em qualquer banco."""
    return Enum(
        tipo_enum,
        name=nome,
        native_enum=False,
        create_constraint=True,
        length=max(len(item.value) for item in tipo_enum),
        validate_strings=True,
        values_callable=lambda itens: [item.value for item in itens],
    )

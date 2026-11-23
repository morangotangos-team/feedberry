"""Valores fixos do domínio.

No banco, cada enum vira um VARCHAR com CHECK (native_enum=False), o que
funciona igual no SQLite e no PostgreSQL. Para incluir um valor novo (ex.:
feedback entre colegas, papel de RH), basta acrescentá-lo aqui e gerar uma
migração.
"""

import enum


class Papel(enum.Enum):
    """Papel da conta. O líder também é colaborador (diagrama de casos de uso)."""

    COLABORADOR = "COLABORADOR"
    LIDER = "LIDER"


class TipoFeedback(enum.Enum):
    LIDER_PARA_COLABORADOR = "LIDER_PARA_COLABORADOR"  # UC03
    COLABORADOR_PARA_LIDER = "COLABORADOR_PARA_LIDER"  # UC12 (e UC13, anônimo)


class StatusPontoMelhoria(enum.Enum):
    ABERTO = "ABERTO"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDO = "CONCLUIDO"


class StatusMeta(enum.Enum):
    NAO_INICIADA = "NAO_INICIADA"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDA = "CONCLUIDA"
    CANCELADA = "CANCELADA"


class StatusLembrete(enum.Enum):
    PENDENTE = "PENDENTE"
    ENVIADO = "ENVIADO"
    CANCELADO = "CANCELADO"

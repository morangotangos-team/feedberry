"""Configurações do back-end do FeedBerry."""

import os
from pathlib import Path

PASTA_BACKEND = Path(__file__).resolve().parent

# Sem DATABASE_URL, usa um SQLite em src/backend/instance/feedberry.db. Um
# caminho relativo no SQLite é resolvido pelo Flask-SQLAlchemy dentro da
# pasta instance/ da aplicação, que fica fora do Git.
BANCO_PADRAO = "sqlite:///feedberry.db"


def _url_do_banco() -> str:
    url = os.environ.get("DATABASE_URL", "").strip() or BANCO_PADRAO
    # Alguns serviços (ex.: Heroku, Render) entregam "postgres://", que o
    # SQLAlchemy 2.x não aceita mais. O nome certo é "postgresql://".
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    return url


class Config:
    SQLALCHEMY_DATABASE_URI = _url_do_banco()

    # Boa prática de segurança: limita o tamanho das requisições (16 KB sobra
    # para e-mail, senha e perfil). Sem limite, um corpo enorme seria lido
    # inteiro na memória. Acima disso, o Flask responde 413.
    MAX_CONTENT_LENGTH = 16 * 1024

"""Extensões do Flask compartilhadas pela aplicação.

Ficam em um módulo próprio para que os modelos importem o `db` sem importar
o app.py (o que criaria import circular).
"""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, event
from sqlalchemy.engine import Engine

# Dá nomes previsíveis às constraints (pk_, fk_, uq_, ck_, ix_). Sem isso,
# cada banco inventa um nome, e as migrações não conseguem apagar ou alterar
# uma constraint depois (o SQLite, em especial, depende desses nomes).
CONVENCAO_DE_NOMES = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

db = SQLAlchemy(metadata=MetaData(naming_convention=CONVENCAO_DE_NOMES))
migrate = Migrate()


@event.listens_for(Engine, "connect")
def _ligar_chaves_estrangeiras_no_sqlite(conexao_dbapi, _registro):
    """O SQLite só confere chaves estrangeiras se isso for ligado a cada conexão.

    Sem este PRAGMA, o SQLite aceitaria um feedback para um usuário que não
    existe e ignoraria o ON DELETE RESTRICT. Em outros bancos não faz nada.
    """
    if type(conexao_dbapi).__module__.startswith("sqlite3"):
        cursor = conexao_dbapi.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

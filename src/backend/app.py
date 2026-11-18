"""Ponto de entrada do back-end do FeedBerry.

Rodar a partir de src/backend:  python app.py
Depois abra http://127.0.0.1:5000/ para usar a tela de login.
Modo debug (só na sua máquina): defina FLASK_DEBUG=1 antes de rodar.
Banco de dados: flask db upgrade (cria ou atualiza o esquema).
"""

from flask import Flask

from auth import auth_bp
from config import PASTA_BACKEND, PASTA_FRONTEND, Config
from extensions import db, migrate


def create_app(config_extra=None):
    # O Flask entrega os arquivos de src/frontend/ na raiz do site, na mesma
    # origem da API (ADR-005). Assim a tela chama fetch("/auth/login") sem CORS.
    app = Flask(__name__, static_folder=str(PASTA_FRONTEND), static_url_path="")
    app.config.from_object(Config)
    if config_extra:
        app.config.update(config_extra)

    # Mantém acentos legíveis nas respostas JSON.
    app.json.ensure_ascii = False

    db.init_app(app)
    # render_as_batch: o SQLite não altera colunas nem constraints com ALTER
    # TABLE; no modo batch o Alembic recria a tabela quando precisa.
    migrate.init_app(app, db, directory=str(PASTA_BACKEND / "migrations"), render_as_batch=True)

    # Registra os modelos no metadata, para o Flask-Migrate enxergar as tabelas.
    import models  # noqa: F401

    app.register_blueprint(auth_bp)

    @app.get("/")
    def tela_de_login():
        return app.send_static_file("index.html")

    return app


if __name__ == "__main__":
    # Boa prática de segurança: o debug não fica fixo no código. O depurador
    # do Werkzeug executa código Python, então só deve ser ligado de propósito
    # em desenvolvimento, com FLASK_DEBUG=1 (o Flask lê essa variável sozinho).
    create_app().run()

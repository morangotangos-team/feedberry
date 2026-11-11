"""Ponto de entrada do back-end do FeedBerry.

Rodar a partir de src/backend:  python app.py
Modo debug (só na sua máquina): defina FLASK_DEBUG=1 antes de rodar.
"""

from flask import Flask

from auth import auth_bp
from config import Config


def create_app(config_extra=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_extra:
        app.config.update(config_extra)

    # Mantém acentos legíveis nas respostas JSON.
    app.json.ensure_ascii = False

    app.register_blueprint(auth_bp)
    return app


if __name__ == "__main__":
    # Boa prática de segurança: o debug não fica fixo no código. O depurador
    # do Werkzeug executa código Python, então só deve ser ligado de propósito
    # em desenvolvimento, com FLASK_DEBUG=1 (o Flask lê essa variável sozinho).
    create_app().run()

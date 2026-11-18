"""Fixtures compartilhadas pelos testes.

Cada teste recebe um banco SQLite novo em memória, então nenhum teste toca no
instance/feedberry.db de quem está rodando.
"""

import secrets

import pytest

from app import create_app
from extensions import db
from models import Papel, Usuario
from services.security import gerar_hash_senha

CONFIG_DE_TESTE = {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"}


@pytest.fixture
def app():
    app = create_app(CONFIG_DE_TESTE)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sessao(app):
    return db.session


@pytest.fixture
def criar_usuario(sessao):
    """Cria e grava um usuário. A senha é aleatória, a menos que seja informada."""

    def _criar(email, papel=Papel.COLABORADOR, nome="Pessoa de Teste", senha=None, **campos):
        usuario = Usuario(
            nome=nome,
            email=email,
            papel=papel,
            senha_hash=gerar_hash_senha(senha or secrets.token_urlsafe(12)),
            **campos,
        )
        sessao.add(usuario)
        sessao.commit()
        return usuario

    return _criar

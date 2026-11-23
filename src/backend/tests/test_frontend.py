"""Testes da entrega das telas pelo Flask (issue #16, ADR-005).

Rodar a partir de src/backend:  python -m pytest
"""

import re

import pytest

from app import create_app


@pytest.fixture
def client():
    return create_app({"TESTING": True}).test_client()


def test_raiz_entrega_a_tela_de_login(client):
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert "text/html" in resposta.content_type
    assert 'data-perfil="publicador"' in resposta.get_data(as_text=True)


@pytest.mark.parametrize("caminho", ["/login/login.js", "/servicos/auth.js", "/publicador/home.html"])
def test_arquivos_do_front_sao_entregues(client, caminho):
    assert client.get(caminho).status_code == 200


def test_arquivos_fora_do_front_nao_sao_entregues(client):
    resposta = client.get("/../backend/data/usuarios.json")

    assert resposta.status_code == 404


def test_api_de_login_continua_no_mesmo_endereco(client):
    resposta = client.post("/auth/login", json={})

    assert resposta.status_code == 400
    assert resposta.is_json


@pytest.mark.parametrize("metodo", ["get", "put", "patch", "delete"])
def test_login_por_outro_metodo_responde_405(client, metodo):
    # Servir as telas na raiz não pode transformar GET /auth/login em 404.
    resposta = getattr(client, metodo)("/auth/login")

    assert resposta.status_code == 405
    assert resposta.headers["Allow"] == "POST"
    assert resposta.is_json


def test_formularios_de_login_enviam_por_post(client):
    # Sem method, o navegador usa GET e, se o JS não carregar, põe e-mail e
    # senha na URL (issue #36). Com POST, os dados vão no corpo da requisição.
    html = client.get("/").get_data(as_text=True)
    formularios = re.findall(r"<form\b[^>]*>", html)

    assert len(formularios) == 2  # publicador e receptor
    for formulario in formularios:
        assert re.search(r'\bmethod="post"', formulario, re.IGNORECASE), formulario

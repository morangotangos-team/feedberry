"""Testes do login (issue #9).

Rodar a partir de src/backend:  python -m pytest

As senhas usadas aqui são geradas na hora com `secrets`, então nenhuma
senha fica escrita no código. Cada teste usa um arquivo de usuários
temporário, sem tocar no data/usuarios.json do projeto.
"""

import json
import logging
import secrets
from pathlib import Path

import pytest

from app import create_app
from auth.security import gerar_hash_senha, verificar_senha
from auth.service import MENSAGEM_CREDENCIAIS_INVALIDAS

ARQUIVO_USUARIOS_DO_PROJETO = Path(__file__).resolve().parent.parent / "data" / "usuarios.json"


@pytest.fixture
def senhas():
    return {
        "publicador": secrets.token_urlsafe(12),
        "receptor": secrets.token_urlsafe(12),
    }


@pytest.fixture
def client(tmp_path, senhas):
    usuarios = [
        {
            "nome": "Pessoa Publicadora",
            "email": "publicador@exemplo.com",
            "perfil": "publicador",
            "senha_hash": gerar_hash_senha(senhas["publicador"]),
        },
        {
            "nome": "Pessoa Receptora",
            "email": "receptor@exemplo.com",
            "perfil": "receptor",
            "senha_hash": gerar_hash_senha(senhas["receptor"]),
        },
    ]
    arquivo = tmp_path / "usuarios.json"
    arquivo.write_text(json.dumps(usuarios), encoding="utf-8")

    app = create_app({"TESTING": True, "USUARIOS_ARQUIVO": arquivo})
    return app.test_client()


def fazer_login(client, email, senha, perfil):
    return client.post("/auth/login", json={"email": email, "senha": senha, "perfil": perfil})


# ---------- Login válido ----------

def test_login_valido_do_publicador_retorna_sucesso_e_perfil(client, senhas):
    resposta = fazer_login(client, "publicador@exemplo.com", senhas["publicador"], "publicador")

    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["sucesso"] is True
    assert corpo["usuario"] == {
        "nome": "Pessoa Publicadora",
        "email": "publicador@exemplo.com",
        "perfil": "publicador",
    }


def test_login_valido_do_receptor_retorna_sucesso_e_perfil(client, senhas):
    resposta = fazer_login(client, "receptor@exemplo.com", senhas["receptor"], "receptor")

    assert resposta.status_code == 200
    assert resposta.get_json()["usuario"]["perfil"] == "receptor"


def test_email_nao_diferencia_maiusculas_nem_espacos(client, senhas):
    resposta = fazer_login(client, "  Publicador@Exemplo.COM ", senhas["publicador"], "publicador")

    assert resposta.status_code == 200


def test_resposta_de_sucesso_nao_expoe_o_hash_da_senha(client, senhas):
    resposta = fazer_login(client, "publicador@exemplo.com", senhas["publicador"], "publicador")

    assert "senha_hash" not in resposta.get_data(as_text=True)


# ---------- Login inválido: mesma mensagem genérica ----------

def test_senha_errada_retorna_erro_generico(client):
    resposta = fazer_login(client, "publicador@exemplo.com", "senha-errada", "publicador")

    assert resposta.status_code == 401
    assert resposta.get_json() == {"sucesso": False, "mensagem": MENSAGEM_CREDENCIAIS_INVALIDAS}


def test_email_nao_cadastrado_retorna_erro_generico(client):
    resposta = fazer_login(client, "ninguem@exemplo.com", "qualquer-senha", "publicador")

    assert resposta.status_code == 401
    assert resposta.get_json() == {"sucesso": False, "mensagem": MENSAGEM_CREDENCIAIS_INVALIDAS}


def test_perfil_diferente_do_cadastrado_retorna_erro_generico(client, senhas):
    # Senha certa, mas o receptor tentou entrar pela aba do publicador.
    resposta = fazer_login(client, "receptor@exemplo.com", senhas["receptor"], "publicador")

    assert resposta.status_code == 401
    assert resposta.get_json() == {"sucesso": False, "mensagem": MENSAGEM_CREDENCIAIS_INVALIDAS}


def test_email_errado_e_senha_errada_tem_a_mesma_resposta(client):
    email_errado = fazer_login(client, "ninguem@exemplo.com", "senha-errada", "publicador")
    senha_errada = fazer_login(client, "publicador@exemplo.com", "senha-errada", "publicador")

    assert email_errado.status_code == senha_errada.status_code
    assert email_errado.get_json() == senha_errada.get_json()


# ---------- Dados de entrada inválidos ----------

@pytest.mark.parametrize("email, senha", [("", "abc"), ("publicador@exemplo.com", ""), ("   ", "   ")])
def test_campos_vazios_retornam_erro_de_validacao(client, email, senha):
    resposta = fazer_login(client, email, senha, "publicador")

    assert resposta.status_code == 400
    assert resposta.get_json() == {"sucesso": False, "mensagem": "Preencha e-mail e senha."}


@pytest.mark.parametrize("email", ["maria.com", "maria@", "@exemplo.com", "maria@exemplo"])
def test_email_em_formato_invalido_retorna_erro_de_validacao(client, email):
    resposta = fazer_login(client, email, "qualquer-senha", "publicador")

    assert resposta.status_code == 400
    assert resposta.get_json()["mensagem"] == "E-mail inválido."


@pytest.mark.parametrize("perfil", [None, "", "admin", "lider"])
def test_perfil_invalido_retorna_erro_de_validacao(client, senhas, perfil):
    resposta = fazer_login(client, "publicador@exemplo.com", senhas["publicador"], perfil)

    assert resposta.status_code == 400
    assert resposta.get_json()["sucesso"] is False


def test_corpo_que_nao_e_json_retorna_erro_de_validacao(client):
    resposta = client.post("/auth/login", data="email=a&senha=b")

    assert resposta.status_code == 400
    assert resposta.get_json()["sucesso"] is False


def test_requisicao_grande_demais_e_recusada(client):
    resposta = fazer_login(client, "publicador@exemplo.com", "x" * 20_000, "publicador")

    assert resposta.status_code == 413


# ---------- Armazenamento seguro ----------

def test_hash_usa_salt_diferente_a_cada_vez(senhas):
    senha = senhas["publicador"]
    hash_1 = gerar_hash_senha(senha)
    hash_2 = gerar_hash_senha(senha)

    assert hash_1 != hash_2
    assert senha not in hash_1
    assert verificar_senha(hash_1, senha)
    assert verificar_senha(hash_2, senha)
    assert not verificar_senha(hash_1, senha + "x")


def test_arquivo_de_usuarios_do_projeto_so_guarda_hash():
    usuarios = json.loads(ARQUIVO_USUARIOS_DO_PROJETO.read_text(encoding="utf-8"))

    assert usuarios, "o arquivo deve ter usuários de teste"
    for usuario in usuarios:
        assert set(usuario) == {"nome", "email", "perfil", "senha_hash"}
        assert usuario["senha_hash"].startswith("scrypt:")
        assert usuario["perfil"] in ("publicador", "receptor")


def test_senha_nao_aparece_nos_logs(client, senhas, caplog):
    with caplog.at_level(logging.DEBUG):
        fazer_login(client, "publicador@exemplo.com", senhas["publicador"], "publicador")
        fazer_login(client, "publicador@exemplo.com", "senha-errada-no-log", "publicador")

    assert senhas["publicador"] not in caplog.text
    assert "senha-errada-no-log" not in caplog.text

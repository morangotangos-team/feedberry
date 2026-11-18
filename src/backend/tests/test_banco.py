"""Testes da migração e do seed (issue #13)."""

import logging
import secrets
from pathlib import Path

import pytest
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from flask_migrate import downgrade, upgrade
from sqlalchemy import inspect, select

import seeds
from app import create_app
from extensions import db
from models import Equipe, Papel, Usuario

PASTA_BACKEND = Path(__file__).resolve().parent.parent
TABELAS = {"usuario", "equipe", "feedback", "ponto_melhoria", "meta_desenvolvimento", "lembrete"}


# ---------- Migração ----------

def test_migracao_cria_o_banco_do_zero_igual_aos_modelos(tmp_path):
    arquivo = tmp_path / "feedberry.db"
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{arquivo}"})

    with app.app_context():
        upgrade()
        assert TABELAS <= set(inspect(db.engine).get_table_names())

        # Nenhuma diferença entre o que a migração criou e os modelos:
        # se alguém mudar um modelo e esquecer a migração, este teste falha.
        with db.engine.connect() as conexao:
            diferencas = compare_metadata(MigrationContext.configure(conexao), db.metadata)
        assert diferencas == []

        downgrade(revision="base")
        assert not TABELAS & set(inspect(db.engine).get_table_names())
        db.engine.dispose()


def test_migracoes_e_seed_nao_guardam_senha_nem_hash():
    arquivos = list((PASTA_BACKEND / "migrations").rglob("*.py")) + [PASTA_BACKEND / "seeds.py"]

    for arquivo in arquivos:
        conteudo = arquivo.read_text(encoding="utf-8")
        assert "scrypt:" not in conteudo, arquivo
        assert "bulk_insert" not in conteudo, arquivo


# ---------- Seed ----------

@pytest.fixture
def senhas_do_seed(monkeypatch):
    senhas = {
        "SEED_SENHA_LIDER": secrets.token_urlsafe(12),
        "SEED_SENHA_COLABORADOR": secrets.token_urlsafe(12),
        "SEED_SENHA_VALIDACAO": secrets.token_urlsafe(12),
    }
    for variavel, senha in senhas.items():
        monkeypatch.setenv(variavel, senha)
    return senhas


def test_seed_cria_equipe_lider_e_colaborador(sessao, senhas_do_seed):
    criados = seeds.popular_banco(sessao)

    assert criados == ["lider@exemplo.com", "colaborador@exemplo.com", "validacao@exemplo.com"]
    equipe = sessao.scalar(select(Equipe))
    assert equipe.lider.email == "lider@exemplo.com"
    assert equipe.lider.papel is Papel.LIDER
    assert {u.email for u in equipe.membros} == {"lider@exemplo.com", "colaborador@exemplo.com"}


def test_seed_guarda_so_o_hash_e_nao_loga_a_senha(sessao, senhas_do_seed, caplog):
    with caplog.at_level(logging.DEBUG):
        seeds.popular_banco(sessao)

    for usuario in sessao.scalars(select(Usuario)):
        assert usuario.senha_hash.startswith("scrypt:")
        for senha in senhas_do_seed.values():
            assert senha not in usuario.senha_hash
    for senha in senhas_do_seed.values():
        assert senha not in caplog.text


def test_seed_pode_rodar_de_novo_sem_duplicar(sessao, senhas_do_seed):
    seeds.popular_banco(sessao)

    assert seeds.popular_banco(sessao) == []
    assert len(sessao.scalars(select(Usuario)).all()) == 3
    assert len(sessao.scalars(select(Equipe)).all()) == 1


def test_seed_sem_senha_no_ambiente_nao_grava_nada(sessao, monkeypatch):
    monkeypatch.setenv("SEED_SENHA_LIDER", secrets.token_urlsafe(12))
    monkeypatch.delenv("SEED_SENHA_COLABORADOR", raising=False)

    with pytest.raises(seeds.SenhaDoSeedAusente, match="SEED_SENHA_COLABORADOR"):
        seeds.popular_banco(sessao)
    assert sessao.scalars(select(Usuario)).all() == []


def test_usuarios_do_seed_entram_com_o_perfil_traduzido(app, sessao, senhas_do_seed):
    seeds.popular_banco(sessao)
    client = app.test_client()

    lider = client.post(
        "/auth/login",
        json={"email": "lider@exemplo.com", "senha": senhas_do_seed["SEED_SENHA_LIDER"], "perfil": "publicador"},
    )
    colaborador = client.post(
        "/auth/login",
        json={
            "email": "colaborador@exemplo.com",
            "senha": senhas_do_seed["SEED_SENHA_COLABORADOR"],
            "perfil": "receptor",
        },
    )

    assert lider.status_code == 200
    assert lider.get_json()["usuario"]["perfil"] == "publicador"
    assert colaborador.status_code == 200
    assert colaborador.get_json()["usuario"]["perfil"] == "receptor"


def test_seed_cria_o_usuario_de_validacao_fora_da_equipe(app, sessao, senhas_do_seed):
    seeds.popular_banco(sessao)

    validacao = sessao.scalar(select(Usuario).where(Usuario.email == "validacao@exemplo.com"))
    assert validacao.nome == "Usuário de Validação"
    assert validacao.papel is Papel.LIDER
    assert validacao.equipe is None
    assert sessao.scalar(select(Equipe)).lider.email == "lider@exemplo.com"

    resposta = app.test_client().post(
        "/auth/login",
        json={
            "email": "validacao@exemplo.com",
            "senha": senhas_do_seed["SEED_SENHA_VALIDACAO"],
            "perfil": "publicador",
        },
    )
    assert resposta.status_code == 200
    assert resposta.get_json()["usuario"]["nome"] == "Usuário de Validação"

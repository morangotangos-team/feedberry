"""Rotas HTTP do login."""

from flask import Blueprint, current_app, jsonify, request

from repositories.usuario_repository import UsuarioRepository

from .service import (
    MENSAGEM_CREDENCIAIS_INVALIDAS,
    AuthService,
    CredenciaisInvalidas,
    ErroDeValidacao,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/login")
def login():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify(sucesso=False, mensagem="Envie e-mail, senha e perfil em JSON."), 400

    repositorio = UsuarioRepository(current_app.config["USUARIOS_ARQUIVO"])
    servico = AuthService(repositorio)

    try:
        usuario = servico.autenticar(dados.get("email"), dados.get("senha"), dados.get("perfil"))
    except ErroDeValidacao as erro:
        return jsonify(sucesso=False, mensagem=str(erro)), 400
    except CredenciaisInvalidas:
        return jsonify(sucesso=False, mensagem=MENSAGEM_CREDENCIAIS_INVALIDAS), 401

    return jsonify(sucesso=True, usuario=usuario), 200


@auth_bp.route("/login", methods=["GET", "PUT", "PATCH", "DELETE"])
def login_metodo_nao_permitido():
    # Como o Flask também entrega as telas na raiz do site, um GET em /auth/login
    # cairia na busca de arquivos estáticos e voltaria 404. Esta rota garante a
    # resposta correta do HTTP: 405, avisando no cabeçalho Allow que só POST vale.
    resposta = jsonify(sucesso=False, mensagem="Método não permitido. Use POST.")
    resposta.status_code = 405
    resposta.headers["Allow"] = "POST"
    return resposta

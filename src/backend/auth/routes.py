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

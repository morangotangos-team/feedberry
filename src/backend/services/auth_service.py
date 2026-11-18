"""Regras do login: valida os dados e confere as credenciais."""

import re

from .security import simular_verificacao, verificar_senha

PERFIS_VALIDOS = ("publicador", "receptor")
MENSAGEM_CREDENCIAIS_INVALIDAS = "E-mail ou senha inválidos."

_FORMATO_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ErroDeValidacao(Exception):
    """Os dados enviados estão incompletos ou em formato errado."""


class CredenciaisInvalidas(Exception):
    """E-mail, senha ou perfil não conferem. A causa exata não é revelada."""


class AuthService:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def autenticar(self, email, senha, perfil) -> dict:
        email = email.strip().lower() if isinstance(email, str) else ""
        senha = senha if isinstance(senha, str) else ""

        if not email or not senha.strip():
            raise ErroDeValidacao("Preencha e-mail e senha.")
        if not _FORMATO_EMAIL.match(email):
            raise ErroDeValidacao("E-mail inválido.")
        if perfil not in PERFIS_VALIDOS:
            raise ErroDeValidacao("Perfil inválido. Use 'publicador' ou 'receptor'.")

        usuario = self.repositorio.buscar_por_email(email)
        if usuario is None:
            simular_verificacao(senha)
            raise CredenciaisInvalidas()

        senha_correta = verificar_senha(usuario["senha_hash"], senha)
        if not senha_correta or usuario["perfil"] != perfil:
            raise CredenciaisInvalidas()

        return {
            "nome": usuario["nome"],
            "email": usuario["email"],
            "perfil": usuario["perfil"],
        }

"""Hash e verificação de senhas.

Técnica: scrypt, pela função generate_password_hash do Werkzeug (que já vem
com o Flask). Cada senha recebe um salt aleatório, e o resultado guarda o
método, os parâmetros, o salt e o hash, por exemplo:

    scrypt:32768:8:1$<salt>$<hash>

A justificativa da escolha está em docs/Funcionalidades/login.md.
"""

import secrets

from werkzeug.security import check_password_hash, generate_password_hash

METODO_HASH = "scrypt"

# Hash de uma senha aleatória que ninguém conhece. Serve para gastar o mesmo
# tempo de verificação quando o e-mail não existe, para que o tempo de
# resposta não revele quais e-mails estão cadastrados.
_HASH_FICTICIO = generate_password_hash(secrets.token_urlsafe(16), method=METODO_HASH)


def gerar_hash_senha(senha: str) -> str:
    return generate_password_hash(senha, method=METODO_HASH)


def verificar_senha(senha_hash: str, senha: str) -> bool:
    # check_password_hash compara em tempo constante.
    return check_password_hash(senha_hash, senha)


def simular_verificacao(senha: str) -> None:
    check_password_hash(_HASH_FICTICIO, senha)

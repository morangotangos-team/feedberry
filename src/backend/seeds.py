"""Cria usuários e uma equipe de teste no banco.

Rodar a partir de src/backend, depois do `flask db upgrade`:

    # PowerShell
    $env:SEED_SENHA_LIDER = "<senha do líder>"
    $env:SEED_SENHA_COLABORADOR = "<senha do colaborador>"
    python seeds.py

As senhas vêm só das variáveis de ambiente e são gravadas como hash scrypt.
Elas nunca ficam no código e nunca são impressas. Rodar de novo não duplica
nada: quem já existe é mantido como está.
"""

import os
import sys

from sqlalchemy import select

from auth.security import gerar_hash_senha
from extensions import db
from models import Equipe, Papel, Usuario

NOME_EQUIPE = "Equipe de Teste"

USUARIOS_DE_TESTE = (
    # (nome, e-mail, papel, variável com a senha)
    ("Líder de Teste", "lider@exemplo.com", Papel.LIDER, "SEED_SENHA_LIDER"),
    ("Colaborador de Teste", "colaborador@exemplo.com", Papel.COLABORADOR, "SEED_SENHA_COLABORADOR"),
)


class SenhaDoSeedAusente(Exception):
    pass


def _senha_do_ambiente(variavel: str) -> str:
    senha = os.environ.get(variavel, "")
    if not senha.strip():
        raise SenhaDoSeedAusente(f"Defina a variável de ambiente {variavel} com a senha de teste.")
    return senha


def popular_banco(sessao=None) -> list[str]:
    """Cria o que faltar e devolve os e-mails dos usuários criados nesta execução."""
    sessao = sessao if sessao is not None else db.session

    # Lê todas as senhas antes de gravar qualquer coisa: ou cria tudo, ou nada.
    senhas = {email: _senha_do_ambiente(variavel) for _, email, _, variavel in USUARIOS_DE_TESTE}

    equipe = sessao.scalar(select(Equipe).where(Equipe.nome == NOME_EQUIPE))
    if equipe is None:
        equipe = Equipe(nome=NOME_EQUIPE)
        sessao.add(equipe)

    criados = []
    for nome, email, papel, _ in USUARIOS_DE_TESTE:
        usuario = sessao.scalar(select(Usuario).where(Usuario.email == email))
        if usuario is None:
            usuario = Usuario(
                nome=nome,
                email=email,
                papel=papel,
                senha_hash=gerar_hash_senha(senhas[email]),
                equipe=equipe,
            )
            sessao.add(usuario)
            criados.append(email)
        if papel is Papel.LIDER and equipe.lider is None:
            equipe.lider = usuario

    sessao.commit()
    return criados


def main() -> int:
    from app import create_app

    app = create_app()
    with app.app_context():
        try:
            criados = popular_banco()
        except SenhaDoSeedAusente as erro:
            print(f"Erro: {erro}", file=sys.stderr)
            return 1
    if criados:
        print("Usuários de teste criados: " + ", ".join(criados))
    else:
        print("Nada a criar: os usuários de teste já existem.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

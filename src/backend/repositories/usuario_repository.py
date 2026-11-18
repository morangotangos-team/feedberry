"""Acesso aos usuários, pelo banco de dados (ORM).

Mantém o método buscar_por_email e o mesmo formato de retorno de quando os
usuários ficavam no data/usuarios.json, para que o AuthService e as regras
de login não mudem.
"""

from sqlalchemy import select

from extensions import db
from models import Papel, Usuario

# ADR-006: no MVP, publicador é o líder e receptor é o colaborador. O login
# usa o perfil e o banco guarda o papel do domínio; a tradução fica só aqui.
# Quando o canal líder <-> gestor entrar, este mapa deixa de ser um para um.
PERFIL_POR_PAPEL = {
    Papel.LIDER: "publicador",
    Papel.COLABORADOR: "receptor",
}


class UsuarioRepository:
    def __init__(self, sessao=None):
        self.sessao = sessao if sessao is not None else db.session

    def buscar_por_email(self, email: str):
        """Devolve o usuário ativo com esse e-mail (sem diferenciar maiúsculas) ou None.

        Usuário desativado é tratado como inexistente, então não consegue
        entrar e recebe a mesma mensagem genérica do login.
        """
        email = email.strip().lower()
        usuario = self.sessao.scalar(
            select(Usuario).where(Usuario.email == email, Usuario.ativo.is_(True))
        )
        if usuario is None:
            return None
        return {
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": PERFIL_POR_PAPEL[usuario.papel],
            "senha_hash": usuario.senha_hash,
        }

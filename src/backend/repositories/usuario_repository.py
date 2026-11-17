"""Acesso aos usuários, pelo banco de dados (ORM).

Mantém o método buscar_por_email e o mesmo formato de retorno de quando os
usuários ficavam no data/usuarios.json, para que o AuthService e as regras
de login não mudem.
"""

from sqlalchemy import select

from extensions import db
from models import Papel, Usuario

# Decisão provisória da issue #13 (ver ADR-007 e ADR-006): o login ainda usa
# o perfil publicador/receptor, e o banco guarda o papel do domínio. A
# tradução fica só aqui; se o grupo decidir outra coisa, muda só este mapa.
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

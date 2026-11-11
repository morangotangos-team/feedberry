"""Acesso aos usuários.

Enquanto não há banco de dados, os usuários ficam em um arquivo JSON. Quando o
banco chegar, troca-se só esta classe, mantendo o método buscar_por_email, e
as rotas e as regras de login continuam iguais.
"""

import json
from pathlib import Path


class UsuarioRepository:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = Path(caminho_arquivo)

    def buscar_por_email(self, email: str):
        """Devolve o usuário com esse e-mail (sem diferenciar maiúsculas) ou None."""
        email = email.strip().lower()
        for usuario in self._carregar():
            if usuario["email"].strip().lower() == email:
                return usuario
        return None

    def _carregar(self) -> list:
        with self.caminho_arquivo.open(encoding="utf-8") as arquivo:
            return json.load(arquivo)

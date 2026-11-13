"""Configurações do back-end do FeedBerry."""

from pathlib import Path

PASTA_BACKEND = Path(__file__).resolve().parent


class Config:
    # Enquanto não há banco de dados, os usuários ficam neste arquivo JSON.
    USUARIOS_ARQUIVO = PASTA_BACKEND / "data" / "usuarios.json"

    # Boa prática de segurança: limita o tamanho das requisições (16 KB sobra
    # para e-mail, senha e perfil). Sem limite, um corpo enorme seria lido
    # inteiro na memória. Acima disso, o Flask responde 413.
    MAX_CONTENT_LENGTH = 16 * 1024

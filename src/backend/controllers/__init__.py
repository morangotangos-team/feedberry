"""Camada de controllers: rotas HTTP (blueprints) de cada funcionalidade."""

from .auth_controller import auth_bp

__all__ = ["auth_bp"]

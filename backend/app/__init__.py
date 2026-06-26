"""Application bootstrap: FastAPI factory, middleware, lifespan hooks."""

from app.factory import create_app

__all__ = ["create_app"]

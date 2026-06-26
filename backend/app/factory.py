"""FastAPI application factory — structural wiring only."""

from fastapi import FastAPI

from config.settings import settings


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # API routers will be registered here in a later step.
    # from api.router import api_router
    # application.include_router(api_router, prefix=settings.api_prefix)

    @application.get("/health")
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return application

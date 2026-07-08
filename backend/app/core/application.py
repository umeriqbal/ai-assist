from fastapi import FastAPI

from app.api.routers.health import router as health_router
from app.core.config import settings


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    #
    # Routers
    #

    app.include_router(
        health_router,
        tags=["Health"],
    )

    return app
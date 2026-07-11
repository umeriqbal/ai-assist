from fastapi import FastAPI

from app.api.routers.chat import router as chat_router
from app.api.routers.document import router as document_router
from app.api.routers.evaluation import router as evaluation_router
from app.api.routers.health import router as health_router
from app.api.routers.qa import router as qa_router
from app.core.config import settings
from app.core.logging import configure_logging


def create_app() -> FastAPI:

    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    app.include_router(
        health_router,
        tags=["Health"],
    )

    app.include_router(
        chat_router,
    )

    app.include_router(
        document_router,
    )

    app.include_router(
        qa_router,
    )

    app.include_router(
        evaluation_router,
    )

    return app
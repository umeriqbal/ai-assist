from datetime import UTC, datetime

from fastapi import APIRouter, Depends

from app.core.config import settings
from app.core.logging import logger
from app.dependencies.llm import get_openai_provider
from app.providers.openai_provider import OpenAIProvider

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():

    logger.info("Root endpoint called")

    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


@router.get("/live")
async def liveness():

    logger.info("Liveness probe")

    return {
        "status": "alive",
    }


@router.get("/ready")
async def readiness(
    provider: OpenAIProvider = Depends(get_openai_provider),
):

    logger.info("Readiness probe")

    #
    # We don't call OpenAI yet.
    # We simply verify that the provider
    # can be constructed successfully.
    #

    return {
        "status": "ready",
        "provider": provider.__class__.__name__,
    }


@router.get("/health")
async def health():

    logger.info("Health check requested")

    return {
        "status": "healthy",
        "timestamp": datetime.now(UTC).isoformat(),
        "environment": settings.environment,
        "version": settings.app_version,
    }
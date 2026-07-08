from datetime import UTC, datetime

from fastapi import APIRouter

from app.core.config import settings
from app.core.logging import logger

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
async def readiness():

    logger.info("Readiness probe")

    #
    # Later we'll verify:
    #
    # - PostgreSQL
    # - Redis
    # - OpenAI
    # - Vector Database
    #

    return {
        "status": "ready",
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
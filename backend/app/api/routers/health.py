from fastapi import APIRouter

from app.core.logging import logger

router = APIRouter()


@router.get("/")
async def root():

    logger.info(
        "Root endpoint called"
    )

    return {
        "message": "Enterprise AI Assistant",
    }


@router.get("/health")
async def health():

    logger.info(
        "Health check requested"
    )

    return {
        "status": "healthy",
    }
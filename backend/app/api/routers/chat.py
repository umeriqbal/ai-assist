from fastapi import APIRouter, Depends

from app.dependencies.services import get_chat_service
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.get("/health")
async def chat_health(
    service: ChatService = Depends(
        get_chat_service
    ),
):

    return {
        "message": await service.health_check()
    }
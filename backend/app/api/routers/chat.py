from fastapi import APIRouter, Depends

from app.dependencies.services import get_chat_service
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.get(
    "/health",
)
async def chat_health(
    service: ChatService = Depends(
        get_chat_service,
    ),
):

    return {
        "message": await service.health_check()
    }


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    service: ChatService = Depends(
        get_chat_service,
    ),
) -> ChatResponse:

    response = await service.chat(
        request.prompt,
    )

    return ChatResponse(
        response=response,
    )
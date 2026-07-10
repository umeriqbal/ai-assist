from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.dependencies.services import (
    get_chat_service,
    get_streaming_service,
)
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.services.streaming_service import StreamingService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.get("/health")
async def chat_health(
    service: ChatService = Depends(get_chat_service),
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
    service: ChatService = Depends(get_chat_service),
) -> ChatResponse:

    response = await service.chat(
        request.prompt,
    )

    return ChatResponse(
        response=response,
    )


@router.post("/stream")
async def stream_chat(
    request: ChatRequest,
    service: StreamingService = Depends(
        get_streaming_service
    ),
):

    async def event_stream():

        async for chunk in service.stream(
            request.prompt
        ):
            yield chunk

    return StreamingResponse(
        event_stream(),
        media_type="text/plain",
    )
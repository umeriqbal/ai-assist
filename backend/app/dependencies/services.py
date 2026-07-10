from functools import lru_cache

from app.dependencies.llm import get_openai_provider
from app.services.chat_service import ChatService
from app.services.streaming_service import StreamingService


@lru_cache
def get_chat_service() -> ChatService:
    return ChatService(
        provider=get_openai_provider(),
    )


@lru_cache
def get_streaming_service() -> StreamingService:
    return StreamingService(
        provider=get_openai_provider(),
    )
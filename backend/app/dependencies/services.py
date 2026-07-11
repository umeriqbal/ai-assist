from functools import lru_cache

from app.dependencies.llm import get_embedding_model, get_openai_provider
from app.services.chat_service import ChatService
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
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


@lru_cache
def get_document_service() -> DocumentService:
    return DocumentService()


@lru_cache
def get_chunking_service() -> ChunkingService:
    return ChunkingService(
        document_service=get_document_service(),
    )


@lru_cache
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService(
        embedding_model=get_embedding_model(),
    )
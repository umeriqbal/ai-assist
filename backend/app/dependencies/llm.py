from functools import lru_cache

from app.agents.in_memory_conversation_memory import InMemoryConversationMemory
from app.agents.memory import ConversationMemory
from app.providers.claude_provider import ClaudeProvider
from app.providers.openai_provider import OpenAIProvider
from app.rag.embeddings.embedding_model import EmbeddingModel
from app.rag.embeddings.factory import EmbeddingModelFactory
from app.rag.stores.factory import VectorStoreFactory
from app.rag.stores.vector_store import VectorStore


@lru_cache
def get_openai_provider() -> OpenAIProvider:
    """
    Return a singleton OpenAI provider.
    """

    return OpenAIProvider()


@lru_cache
def get_claude_provider() -> ClaudeProvider:
    """
    Return a singleton Claude provider.

    Not wired into any service by default — OpenAI remains the active
    `LLMProvider` everywhere. This exists so a service can be pointed
    at Claude by swapping which `get_*_provider()` its constructor
    call uses, without changing the service itself.
    """

    return ClaudeProvider()


@lru_cache
def get_embedding_model() -> EmbeddingModel:
    """
    Return a singleton embedding model.
    """

    return EmbeddingModelFactory.create()


@lru_cache
def get_vector_store() -> VectorStore:
    """
    Return a singleton vector store.

    Must be cached: the in-memory implementation only holds data
    for the lifetime of a single instance, so every caller needs
    to share the same one.
    """

    return VectorStoreFactory.create()


@lru_cache
def get_conversation_memory() -> ConversationMemory:
    """
    Return a singleton conversation memory store.

    Must be cached: the in-memory implementation only holds data for
    the lifetime of a single instance, so every caller needs to share
    the same one.
    """

    return InMemoryConversationMemory()
from functools import lru_cache

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
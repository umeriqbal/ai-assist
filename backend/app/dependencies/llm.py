from functools import lru_cache

from app.providers.openai_provider import OpenAIProvider
from app.rag.embeddings.embedding_model import EmbeddingModel
from app.rag.embeddings.factory import EmbeddingModelFactory


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
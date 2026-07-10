from functools import lru_cache

from app.providers.openai_embedding_provider import (
    OpenAIEmbeddingProvider,
)


@lru_cache
def get_embedding_provider() -> OpenAIEmbeddingProvider:
    """
    Return a singleton embedding provider.
    """

    return OpenAIEmbeddingProvider()
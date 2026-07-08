from functools import lru_cache

from app.providers.openai_provider import OpenAIProvider


@lru_cache
def get_openai_provider() -> OpenAIProvider:
    """
    Return a singleton OpenAI provider.
    """

    return OpenAIProvider()
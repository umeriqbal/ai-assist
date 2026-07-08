from openai import AsyncOpenAI

from app.core.config import settings


class OpenAIProvider:
    """
    Wrapper around the OpenAI client.

    This class owns the SDK client.
    Higher-level services will use this provider
    instead of talking directly to the SDK.
    """

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key=settings.openai_api_key,
        )

    @property
    def client(self) -> AsyncOpenAI:
        return self._client
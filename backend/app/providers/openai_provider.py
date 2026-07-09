from openai import AsyncOpenAI

from app.core.config import settings
from app.providers.base import LLMProvider


class OpenAIProvider(LLMProvider):
    """
    OpenAI implementation of the LLM provider interface.
    """

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key=settings.openai_api_key,
        )

    @property
    def client(self) -> AsyncOpenAI:
        return self._client

    async def health_check(self) -> bool:
        """
        For now, simply verify the client exists.

        Later we'll make a lightweight API request.
        """

        return self._client is not None
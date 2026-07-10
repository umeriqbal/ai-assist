from collections.abc import AsyncIterator

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

    async def health_check(self) -> bool:
        return self._client is not None

    async def chat(
        self,
        prompt: str,
    ) -> str:

        response = await self._client.responses.create(
            model=settings.openai_chat_model,
            input=prompt,
        )

        return response.output_text

    async def stream_chat(
        self,
        prompt: str,
    ) -> AsyncIterator[str]:
        """
        Stream tokens from the OpenAI Responses API.
        """

        stream = await self._client.responses.create(
            model=settings.openai_chat_model,
            input=prompt,
            stream=True,
        )

        async for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta
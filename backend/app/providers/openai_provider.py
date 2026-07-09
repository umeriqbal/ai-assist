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
        """
        For now, simply verify the client exists.

        Later we'll make a lightweight API request.
        """
        return self._client is not None

    async def chat(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a chat response using OpenAI.

        This is intentionally simple.
        We'll add streaming, tools, structured outputs,
        and conversation history in later sprints.
        """

        response = await self._client.responses.create(
            model=settings.openai_chat_model,
            input=prompt,
        )

        return response.output_text
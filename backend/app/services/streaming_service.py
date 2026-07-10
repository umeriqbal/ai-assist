from collections.abc import AsyncIterator

from app.providers.base import LLMProvider


class StreamingService:
    """
    Business service responsible for streaming chat responses.
    """

    def __init__(
        self,
        provider: LLMProvider,
    ) -> None:
        self._provider = provider

    async def stream(
        self,
        prompt: str,
    ) -> AsyncIterator[str]:
        """
        Stream a response from the configured LLM provider.
        """

        prompt = prompt.strip()

        async for chunk in self._provider.stream_chat(prompt):
            yield chunk
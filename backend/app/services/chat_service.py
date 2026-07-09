from app.providers.base import LLMProvider


class ChatService:
    """
    Business service responsible for chat operations.
    """

    def __init__(
        self,
        provider: LLMProvider,
    ) -> None:
        self._provider = provider

    async def health_check(self) -> str:
        healthy = await self._provider.health_check()

        return (
            "Chat service is ready."
            if healthy
            else "Chat service is unavailable."
        )

    async def chat(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a chat response.

        The service delegates the LLM interaction
        to the provider.
        """

        return await self._provider.chat(prompt)
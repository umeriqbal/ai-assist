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

        if healthy:
            return "Chat service is ready."

        return "Chat service is unavailable."
from app.providers.openai_provider import OpenAIProvider


class ChatService:
    """
    Business service responsible for chat operations.
    """

    def __init__(
        self,
        provider: OpenAIProvider,
    ) -> None:

        self._provider = provider

    async def health_check(self) -> str:
        """
        Simple method proving the service works.

        Later this class will generate chat
        completions and stream responses.
        """

        return "Chat service is ready."
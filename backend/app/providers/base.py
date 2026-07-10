from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class LLMProvider(ABC):
    """
    Abstract interface implemented by all LLM providers.
    """

    @abstractmethod
    async def health_check(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def chat(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def stream_chat(
        self,
        prompt: str,
    ) -> AsyncIterator[str]:
        """
        Stream a response token-by-token.
        """
        raise NotImplementedError
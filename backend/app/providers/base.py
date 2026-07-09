from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Abstract interface implemented by all LLM providers.
    """

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Verify the provider is available.
        """
        raise NotImplementedError

    @abstractmethod
    async def chat(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a chat response.
        """
        raise NotImplementedError
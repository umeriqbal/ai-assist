from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Abstract base class for Large Language Model providers.
    """

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Verify the provider is available.
        """
        raise NotImplementedError
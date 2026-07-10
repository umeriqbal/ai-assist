from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """
    Abstract interface for embedding providers.
    """

    @abstractmethod
    async def embed_text(self, text: str) -> list[float]:
        """
        Generate an embedding for a single piece of text.
        """
        raise NotImplementedError

    @abstractmethod
    async def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple pieces of text.
        """
        raise NotImplementedError
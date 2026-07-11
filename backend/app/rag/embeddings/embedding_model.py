from abc import ABC, abstractmethod


class EmbeddingModel(ABC):
    """
    Base interface for embedding model providers.

    Implementations wrap whatever SDK/framework is used to compute
    embeddings, so callers only ever see plain Python types.
    """

    @abstractmethod
    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Embed a batch of texts in a single call.
        """
        raise NotImplementedError

    @abstractmethod
    async def embed_query(
        self,
        text: str,
    ) -> list[float]:
        """
        Embed a single query string.
        """
        raise NotImplementedError
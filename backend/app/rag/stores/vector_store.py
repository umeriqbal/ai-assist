from abc import ABC, abstractmethod

from app.rag.embeddings.embedded_chunk import EmbeddedChunk
from app.rag.stores.scored_chunk import ScoredChunk


class VectorStore(ABC):
    """
    Interface implemented by all vector stores.
    """

    @abstractmethod
    async def add_documents(
        self,
        embedded_chunks: list[EmbeddedChunk],
    ) -> None:
        """
        Index embedded chunks.
        """
        raise NotImplementedError

    @abstractmethod
    async def similarity_search(
        self,
        query_vector: list[float],
        k: int = 5,
    ) -> list[ScoredChunk]:
        """
        Return the k chunks most similar to a query vector,
        ranked by descending similarity score.
        """
        raise NotImplementedError

    @abstractmethod
    async def document_count(self) -> int:
        """
        Return the number of indexed chunks.
        """
        raise NotImplementedError
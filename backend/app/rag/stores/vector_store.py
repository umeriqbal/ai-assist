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
        metadata_filter: dict[str, str] | None = None,
    ) -> list[ScoredChunk]:
        """
        Return the k chunks most similar to a query vector,
        ranked by descending similarity score.

        If `metadata_filter` is provided, only chunks whose metadata
        matches every key/value pair are considered, and the filter
        is applied before ranking so the returned results are the
        true top-k within the filtered set.
        """
        raise NotImplementedError

    @abstractmethod
    async def document_count(self) -> int:
        """
        Return the number of indexed chunks.
        """
        raise NotImplementedError
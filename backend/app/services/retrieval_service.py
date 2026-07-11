from app.rag.stores.scored_chunk import ScoredChunk
from app.rag.stores.vector_store import VectorStore
from app.services.embedding_service import EmbeddingService


class RetrievalService:
    """
    Business service responsible for semantic retrieval.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        self._embedding_service = embedding_service
        self._vector_store = vector_store

    async def retrieve(
        self,
        query: str,
        k: int = 4,
        source: str | None = None,
    ) -> list[ScoredChunk]:

        query = query.strip()

        if not query:
            raise ValueError("Search query cannot be empty.")

        query_vector = await self._embedding_service.embed_query(query)

        metadata_filter = {"source": source} if source else None

        return await self._vector_store.similarity_search(
            query_vector=query_vector,
            k=k,
            metadata_filter=metadata_filter,
        )

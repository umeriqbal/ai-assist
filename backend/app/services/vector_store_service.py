from app.rag.stores.vector_store import VectorStore
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService


class VectorStoreService:
    """
    Business service responsible for indexing chunks.
    """

    def __init__(
        self,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        self._chunking_service = chunking_service
        self._embedding_service = embedding_service
        self._vector_store = vector_store

    async def index_text(
        self,
        text: str,
        source: str = "manual-upload",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> int:

        chunks = await self._chunking_service.chunk_text(
            text=text,
            source=source,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        embedded_chunks = await self._embedding_service.embed_chunks(chunks)

        await self._vector_store.add_documents(embedded_chunks)

        return len(embedded_chunks)

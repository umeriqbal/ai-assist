from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from app.rag.document_ingestion_service import DocumentIngestionService
from app.services.vector_store_service import VectorStoreService


@dataclass
class UploadResult:
    """
    The result of uploading and indexing a file.
    """

    source: str
    pages_loaded: int
    chunks_indexed: int


class DocumentUploadService:
    """
    Business service responsible for ingesting an uploaded file and
    indexing it, so it becomes searchable and answerable.
    """

    def __init__(
        self,
        ingestion_service: DocumentIngestionService,
        vector_store_service: VectorStoreService,
    ) -> None:
        self._ingestion_service = ingestion_service
        self._vector_store_service = vector_store_service

    async def upload(
        self,
        file_path: str | Path,
        source: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> UploadResult:

        documents = await self._ingestion_service.ingest(file_path)

        created_at = datetime.now(UTC).isoformat()

        for document in documents:
            document.metadata["source"] = source
            document.metadata["created_at"] = created_at

        chunks_indexed = await self._vector_store_service.index_documents(
            documents=documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        return UploadResult(
            source=source,
            pages_loaded=len(documents),
            chunks_indexed=chunks_indexed,
        )

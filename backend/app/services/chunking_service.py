from langchain_core.documents import Document

from app.rag.splitters.recursive_splitter import RecursiveDocumentSplitter
from app.services.document_service import DocumentService


class ChunkingService:
    """
    Business service responsible for splitting documents into chunks.
    """

    def __init__(
        self,
        document_service: DocumentService,
    ) -> None:
        self._document_service = document_service

    async def chunk_text(
        self,
        text: str,
        source: str = "manual-upload",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> list[Document]:

        document = await self._document_service.create_document(
            text=text,
            source=source,
        )

        splitter = RecursiveDocumentSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        return splitter.split([document])

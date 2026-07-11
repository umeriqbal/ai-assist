from datetime import UTC, datetime

from langchain_core.documents import Document

from app.rag.document_factory import DocumentFactory


class DocumentService:
    """
    Business service responsible for document creation.
    """

    async def create_document(
        self,
        text: str,
        source: str = "manual-upload",
    ) -> Document:

        text = text.strip()

        if not text:
            raise ValueError("Document text cannot be empty.")

        metadata = {
            "source": source,
            "created_at": datetime.now(UTC).isoformat(),
        }

        return DocumentFactory.create(
            text=text,
            metadata=metadata,
        )
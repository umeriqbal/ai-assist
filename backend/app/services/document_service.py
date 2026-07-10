from langchain_core.documents import Document

from app.rag.document_factory import DocumentFactory


class DocumentService:

    async def create_document(
        self,
        text: str,
        metadata: dict | None = None
    ) -> Document:

        text = text.strip()

        if not text:
            raise ValueError("Document text cannot be empty.")

        return DocumentFactory.create(
            text=text,
            metadata=metadata,
        )
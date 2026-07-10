from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from app.rag.loaders.document_loader import DocumentLoader


class PDFLoader(DocumentLoader):
    """
    PDF implementation of the DocumentLoader interface.
    """

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return (".pdf",)

    async def load(
        self,
        file_path: str | Path,
    ) -> list[Document]:
        loader = PyPDFLoader(str(file_path))
        return await loader.aload()
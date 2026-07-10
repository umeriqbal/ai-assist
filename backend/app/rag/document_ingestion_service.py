from pathlib import Path

from langchain_core.documents import Document

from app.rag.loaders.pdf_loader import PDFLoader


class DocumentIngestionService:
    """
    Coordinates the ingestion of documents into the RAG pipeline.

    This service is responsible for selecting the appropriate
    loader and returning LangChain Documents.

    At the current stage only PDF files are supported.
    """

    def __init__(
        self,
        pdf_loader: PDFLoader | None = None,
    ) -> None:
        self._pdf_loader = pdf_loader or PDFLoader()

    async def ingest(
        self,
        file_path: str | Path,
    ) -> list[Document]:
        """
        Ingest a document.

        Args:
            file_path:
                Path to the document.

        Returns:
            A list of LangChain Document objects.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                f"Unsupported file type: {path.suffix}"
            )

        return await self._pdf_loader.load(path)
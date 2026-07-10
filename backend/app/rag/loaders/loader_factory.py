from pathlib import Path

from app.rag.loaders.document_loader import DocumentLoader
from app.rag.loaders.pdf_loader import PDFLoader


class DocumentLoaderFactory:
    """
    Returns the appropriate loader for a given file type.
    """

    def __init__(
        self,
        loaders: list[DocumentLoader] | None = None,
    ) -> None:
        self._loaders = loaders or [
            PDFLoader(),
        ]

    def get_loader(
        self,
        file_path: str | Path,
    ) -> DocumentLoader:
        extension = Path(file_path).suffix.lower()

        for loader in self._loaders:
            if extension in loader.SUPPORTED_EXTENSIONS:
                return loader

        raise ValueError(
            f"No loader registered for '{extension}'."
        )
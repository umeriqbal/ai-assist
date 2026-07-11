"""
PDF Loader

Responsible for loading PDF documents and converting them into
LangChain Document objects.

This module contains no business logic.
"""

import asyncio
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader

from app.rag.loaders.document_loader import DocumentLoader

_SUPPORTED_EXTENSIONS = (".pdf",)


class PDFLoader(DocumentLoader):
    """
    Loads PDF files using LangChain's PyPDFLoader.
    """

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return _SUPPORTED_EXTENSIONS

    async def load(self, file_path: str | Path) -> List[Document]:
        """
        Load a PDF into LangChain Documents.

        Parameters
        ----------
        file_path:
            Absolute or relative path to the PDF.

        Returns
        -------
        List[Document]
            One document per PDF page.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.

        ValueError
            If the file extension is unsupported.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if path.suffix.lower() not in self.supported_extensions:
            raise ValueError(
                f"Unsupported file type '{path.suffix}'. "
                f"Supported: {', '.join(self.supported_extensions)}"
            )

        loader = PyPDFLoader(str(path))

        # PyPDFLoader.load() is a blocking, synchronous call — run it
        # off the event loop so it doesn't stall other requests.
        documents = await asyncio.to_thread(loader.load)

        return documents
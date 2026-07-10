"""
PDF Loader

Responsible for loading PDF documents and converting them into
LangChain Document objects.

This module contains no business logic.
"""

from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:
    """
    Loads PDF files using LangChain's PyPDFLoader.
    """

    SUPPORTED_EXTENSIONS = {".pdf"}

    def load(self, file_path: str | Path) -> List[Document]:
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

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type '{path.suffix}'. "
                f"Supported: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )

        loader = PyPDFLoader(str(path))

        documents = loader.load()

        return documents
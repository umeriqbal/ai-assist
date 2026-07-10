from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:
    """
    Responsible for loading PDF files and converting them
    into LangChain Document objects.

    Each page of the PDF becomes a separate Document.
    """

    async def load(
        self,
        file_path: str | Path,
    ) -> list[Document]:
        """
        Load a PDF and return LangChain Documents.

        Args:
            file_path:
                Path to the PDF.

        Returns:
            List of LangChain Documents.
        """

        loader = PyPDFLoader(
            str(file_path),
        )

        return await loader.aload()
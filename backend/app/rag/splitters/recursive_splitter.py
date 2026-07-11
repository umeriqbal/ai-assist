"""
Recursive Text Splitter

Responsible for splitting LangChain Documents into
smaller chunks suitable for embedding.

This module contains no business logic.
"""

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RecursiveDocumentSplitter:
    """
    Splits LangChain documents into overlapping chunks.

    Chunk overlap helps preserve context between
    neighbouring chunks.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
            add_start_index=True,
        )

    def split(
        self,
        documents: List[Document],
    ) -> List[Document]:
        """
        Split LangChain Documents into smaller chunks.

        Parameters
        ----------
        documents:
            List of LangChain Document objects.

        Returns
        -------
        List[Document]
            Chunked documents. Each chunk's metadata is extended
            with `chunk_index` and `chunk_count` so chunks can be
            ordered and traced back to their source document.
        """

        if not documents:
            return []

        chunks = self._splitter.split_documents(documents)

        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = index
            chunk.metadata["chunk_count"] = len(chunks)

        return chunks
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentTextSplitter:
    """
    Responsible for splitting LangChain Documents into
    smaller semantic chunks while preserving metadata.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split(
        self,
        document: Document,
    ) -> list[Document]:
        """
        Split a single LangChain Document into multiple
        LangChain Documents.

        Metadata is automatically preserved.
        """

        return self._split_documents([document])

    def split_many(
        self,
        documents: list[Document],
    ) -> list[Document]:
        """
        Split multiple documents into chunks.
        """

        return self._split_documents(documents)

    def _split_documents(
        self,
        documents: list[Document],
    ) -> list[Document]:
        return self._splitter.split_documents(documents)
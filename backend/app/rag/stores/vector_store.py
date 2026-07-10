from abc import ABC, abstractmethod

from langchain_core.documents import Document


class VectorStore(ABC):
    """
    Interface implemented by all vector stores.
    """

    @abstractmethod
    async def add_documents(
        self,
        documents: list[Document],
    ) -> None:
        """
        Index documents.
        """
        raise NotImplementedError

    @abstractmethod
    async def similarity_search(
        self,
        query: str,
        k: int = 5,
    ) -> list[Document]:
        """
        Search for similar documents.
        """
        raise NotImplementedError
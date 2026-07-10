from abc import ABC, abstractmethod

from langchain_core.documents import Document


class VectorStore(ABC):
    """
    Abstract interface for vector stores.
    """

    @abstractmethod
    async def add_documents(
        self,
        documents: list[Document],
        embeddings: list[list[float]],
    ) -> None:
        """
        Store documents together with their embeddings.
        """
        raise NotImplementedError

    @abstractmethod
    async def similarity_search(
        self,
        embedding: list[float],
        k: int = 5,
    ) -> list[Document]:
        """
        Return the k most similar documents.
        """
        raise NotImplementedError
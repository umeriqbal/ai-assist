from abc import ABC, abstractmethod

from langchain_core.embeddings import Embeddings


class EmbeddingModel(ABC):
    """
    Base interface for embedding model providers.
    """

    @abstractmethod
    def get_embeddings(self) -> Embeddings:
        """
        Return a LangChain Embeddings implementation.
        """
        raise NotImplementedError
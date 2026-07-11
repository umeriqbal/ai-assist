from app.rag.stores.in_memory_vector_store import InMemoryVectorStore
from app.rag.stores.vector_store import VectorStore


class VectorStoreFactory:
    """
    Factory for creating vector store implementations.
    """

    @staticmethod
    def create() -> VectorStore:
        return InMemoryVectorStore()
from app.rag.stores.chroma_store import ChromaStore
from app.rag.stores.vector_store import VectorStore


class VectorStoreFactory:
    """
    Factory for creating vector store implementations.
    """

    @staticmethod
    def create() -> VectorStore:
        return ChromaStore()
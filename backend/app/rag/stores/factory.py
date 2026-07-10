from app.rag.stores.chroma_store import ChromaVectorStore
from app.rag.stores.vector_store import VectorStore


class VectorStoreFactory:
    """
    Factory for creating vector store implementations.
    """

    @staticmethod
    def create() -> VectorStore:
        return ChromaVectorStore()
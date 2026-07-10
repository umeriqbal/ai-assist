from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.rag.embeddings.embedding_model import EmbeddingModel
from app.rag.embeddings.factory import EmbeddingModelFactory
from app.rag.stores.vector_store import VectorStore


class ChromaStore(VectorStore):
    """
    ChromaDB implementation of the VectorStore interface.
    """

    def __init__(
        self,
        embedding_model: EmbeddingModel | None = None,
    ) -> None:
        self._embedding_model = (
            embedding_model
            or EmbeddingModelFactory.create()
        )

        self._store = Chroma(
            collection_name="enterprise-ai-assistant",
            embedding_function=self._embedding_model.get_embeddings(),
            persist_directory="./data/chroma",
        )

    async def add_documents(
        self,
        documents: list[Document],
    ) -> None:
        self._store.add_documents(documents)

    async def similarity_search(
        self,
        query: str,
        k: int = 5,
    ) -> list[Document]:
        return self._store.similarity_search(
            query=query,
            k=k,
        )
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from app.core.config import settings
from app.rag.stores.vector_store import VectorStore


class ChromaStore(VectorStore):
    """
    ChromaDB implementation of the VectorStore interface.
    """

    def __init__(self) -> None:
        self._store = Chroma(
            collection_name="enterprise-ai-assistant",
            embedding_function=OpenAIEmbeddings(
                api_key=settings.openai_api_key,
                model=settings.openai_embedding_model,
            ),
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
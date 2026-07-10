"""
Chroma Vector Store

Responsible for persisting and querying document embeddings.

Responsibilities:
- Create/load the Chroma database
- Add documents
- Perform similarity search
- Expose a retriever

Does NOT:
- Load files
- Split documents
- Generate embeddings
- Contain business logic
"""

from typing import List

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_chroma import Chroma

from app.core.config import settings
from app.rag.embeddings.openai_embedding_model import OpenAIEmbeddingProvider
from app.rag.stores.vector_store import VectorStore

class ChromaVectorStore(VectorStore):
    """
    Wrapper around LangChain's Chroma vector store.
    """

    def __init__(self) -> None:
        self._embedding_provider = OpenAIEmbeddingProvider()

        self._vector_store = Chroma(
            collection_name="knowledge_base",
            embedding_function=self._embedding_provider.embeddings,
            persist_directory=settings.chroma_persist_directory,
        )

    @property
    def vector_store(self) -> Chroma:
        """
        Return the underlying Chroma instance.
        """
        return self._vector_store

    def add_documents(
        self,
        documents: List[Document],
    ) -> None:
        """
        Add chunked documents to the vector store.
        """

        if not documents:
            return

        self._vector_store.add_documents(documents)

    def similarity_search(
        self,
        query: str,
        k: int = 4,
    ) -> List[Document]:
        """
        Perform a similarity search.
        """

        return self._vector_store.similarity_search(
            query=query,
            k=k,
        )

    def as_retriever(
        self,
        k: int = 4,
    ) -> BaseRetriever:
        """
        Return a LangChain retriever.
        """

        return self._vector_store.as_retriever(
            search_kwargs={
                "k": k,
            }
        )

    def document_count(self) -> int:
        """
        Return the number of indexed documents.
        """

        return self._vector_store._collection.count()

    def delete_collection(self) -> None:
        """
        Delete all indexed documents.
        """

        self._vector_store.delete_collection()

    def reset(self) -> None:
        """
        Recreate an empty collection.
        """

        self.delete_collection()

        self._vector_store = Chroma(
            collection_name="knowledge_base",
            embedding_function=self._embedding_provider.embeddings,
            persist_directory=settings.chroma_persist_directory,
        )
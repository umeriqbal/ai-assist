"""
OpenAI Embeddings

Provides a configured OpenAI embedding model for the RAG pipeline.

Responsibilities:
- Create and configure the embedding model.
- Expose the embedding instance to the vector store.

Does NOT:
- Load documents
- Split documents
- Store vectors
- Perform retrieval
"""

from langchain_openai import OpenAIEmbeddings

from app.core.config import settings


class OpenAIEmbeddingProvider:
    """
    Factory for the OpenAI embedding model.
    """

    def __init__(self) -> None:
        self._embeddings = OpenAIEmbeddings(
            api_key=settings.openai_api_key,
            model=settings.embedding_model,
        )

    @property
    def embeddings(self) -> OpenAIEmbeddings:
        """
        Return the configured embedding model.
        """
        return self._embeddings
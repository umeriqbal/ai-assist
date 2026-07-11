"""
OpenAI Embeddings

Provides a configured OpenAI embedding model for the RAG pipeline.

Responsibilities:
- Create and configure the embedding model.
- Call the OpenAI embeddings API (via LangChain) and return plain
  Python vectors.

Does NOT:
- Load documents
- Split documents
- Store vectors
- Perform retrieval
"""

from langchain_openai import OpenAIEmbeddings

from app.core.config import settings
from app.rag.embeddings.embedding_model import EmbeddingModel


class OpenAIEmbeddingModel(EmbeddingModel):
    """
    OpenAI implementation of the embedding model interface.
    """

    def __init__(self) -> None:
        self._embeddings = OpenAIEmbeddings(
            api_key=settings.openai_api_key,
            model=settings.embedding_model,
        )

    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return await self._embeddings.aembed_documents(texts)

    async def embed_query(
        self,
        text: str,
    ) -> list[float]:
        return await self._embeddings.aembed_query(text)
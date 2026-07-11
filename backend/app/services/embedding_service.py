from langchain_core.documents import Document

from app.rag.embeddings.embedded_chunk import EmbeddedChunk
from app.rag.embeddings.embedding_model import EmbeddingModel


class EmbeddingService:
    """
    Business service responsible for embedding chunked documents.
    """

    def __init__(
        self,
        embedding_model: EmbeddingModel,
    ) -> None:
        self._embedding_model = embedding_model

    async def embed_chunks(
        self,
        chunks: list[Document],
    ) -> list[EmbeddedChunk]:

        if not chunks:
            return []

        texts = [chunk.page_content for chunk in chunks]

        vectors = await self._embedding_model.embed_documents(texts)

        return [
            EmbeddedChunk(document=chunk, vector=vector)
            for chunk, vector in zip(chunks, vectors)
        ]

    async def embed_query(
        self,
        text: str,
    ) -> list[float]:

        return await self._embedding_model.embed_query(text)

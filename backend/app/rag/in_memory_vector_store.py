import math

from langchain_core.documents import Document

from app.rag.vector_store import VectorStore


class InMemoryVectorStore(VectorStore):
    """
    Simple in-memory vector store.

    This implementation is intended for learning and testing.
    It will later be replaced by PostgreSQL + pgvector.
    """

    def __init__(self) -> None:
        self._documents: list[Document] = []
        self._embeddings: list[list[float]] = []

    async def add_documents(
        self,
        documents: list[Document],
        embeddings: list[list[float]],
    ) -> None:
        if len(documents) != len(embeddings):
            raise ValueError(
                "Documents and embeddings must have the same length."
            )

        self._documents.extend(documents)
        self._embeddings.extend(embeddings)

    async def similarity_search(
        self,
        embedding: list[float],
        k: int = 5,
    ) -> list[Document]:
        scores: list[tuple[float, Document]] = []

        for stored_embedding, document in zip(
            self._embeddings,
            self._documents,
            strict=True,
        ):
            similarity = self._cosine_similarity(
                embedding,
                stored_embedding,
            )

            scores.append((similarity, document))

        scores.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            document
            for _, document in scores[:k]
        ]

    @staticmethod
    def _cosine_similarity(
        vector_a: list[float],
        vector_b: list[float],
    ) -> float:
        dot_product = sum(
            a * b
            for a, b in zip(vector_a, vector_b, strict=True)
        )

        norm_a = math.sqrt(sum(x * x for x in vector_a))
        norm_b = math.sqrt(sum(x * x for x in vector_b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)
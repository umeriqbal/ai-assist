"""
In-Memory Vector Store

A brute-force vector store used as the first implementation of the
Sprint 4 storage stage. Holds embedded chunks in a Python list and
ranks them by cosine similarity on every search.

Intentionally not optimised for scale: it exists to demonstrate the
retrieval algorithm before a production-grade store (PostgreSQL +
pgvector) replaces it behind the same VectorStore interface.
"""

import math

from app.rag.embeddings.embedded_chunk import EmbeddedChunk
from app.rag.stores.scored_chunk import ScoredChunk
from app.rag.stores.vector_store import VectorStore


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot_product = sum(x * y for x, y in zip(a, b))

    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


class InMemoryVectorStore(VectorStore):
    """
    Stores embedded chunks in memory for the lifetime of the process.
    """

    def __init__(self) -> None:
        self._entries: list[EmbeddedChunk] = []

    async def add_documents(
        self,
        embedded_chunks: list[EmbeddedChunk],
    ) -> None:

        self._entries.extend(embedded_chunks)

    async def similarity_search(
        self,
        query_vector: list[float],
        k: int = 5,
        metadata_filter: dict[str, str] | None = None,
    ) -> list[ScoredChunk]:

        candidates = self._entries

        if metadata_filter:
            candidates = [
                entry
                for entry in candidates
                if metadata_filter.items() <= entry.document.metadata.items()
            ]

        scored = [
            ScoredChunk(
                document=entry.document,
                score=_cosine_similarity(query_vector, entry.vector),
            )
            for entry in candidates
        ]

        scored.sort(key=lambda chunk: chunk.score, reverse=True)

        return scored[:k]

    async def document_count(self) -> int:
        return len(self._entries)

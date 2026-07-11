import asyncio

from langchain_core.documents import Document

from app.rag.embeddings.embedded_chunk import EmbeddedChunk
from app.rag.stores.in_memory_vector_store import InMemoryVectorStore


def _chunk(content: str, vector: list[float]) -> EmbeddedChunk:
    return EmbeddedChunk(
        document=Document(page_content=content),
        vector=vector,
    )


def test_similarity_search_ranks_identical_vector_highest():
    store = InMemoryVectorStore()

    asyncio.run(
        store.add_documents(
            [
                _chunk("unrelated", [0.0, 1.0]),
                _chunk("exact match", [1.0, 0.0]),
                _chunk("somewhat related", [0.7, 0.7]),
            ]
        )
    )

    results = asyncio.run(store.similarity_search([1.0, 0.0], k=3))

    assert results[0].document.page_content == "exact match"
    assert results[0].score > results[1].score > results[2].score


def test_identical_vectors_score_close_to_one():
    store = InMemoryVectorStore()

    asyncio.run(store.add_documents([_chunk("same direction", [2.0, 2.0])]))

    results = asyncio.run(store.similarity_search([1.0, 1.0], k=1))

    assert results[0].score > 0.999


def test_orthogonal_vectors_score_close_to_zero():
    store = InMemoryVectorStore()

    asyncio.run(store.add_documents([_chunk("perpendicular", [1.0, 0.0])]))

    results = asyncio.run(store.similarity_search([0.0, 1.0], k=1))

    assert abs(results[0].score) < 0.001


def test_similarity_search_respects_k():
    store = InMemoryVectorStore()

    asyncio.run(
        store.add_documents(
            [_chunk(str(i), [float(i), 0.0]) for i in range(10)]
        )
    )

    results = asyncio.run(store.similarity_search([1.0, 0.0], k=3))

    assert len(results) == 3


def test_document_count_tracks_added_chunks():
    store = InMemoryVectorStore()

    asyncio.run(store.add_documents([_chunk("a", [1.0]), _chunk("b", [1.0])]))

    assert asyncio.run(store.document_count()) == 2

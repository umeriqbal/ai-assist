import asyncio

import pytest

from app.rag.stores.in_memory_vector_store import InMemoryVectorStore
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from tests.conftest import FakeEmbeddingModel


def _service() -> VectorStoreService:
    return VectorStoreService(
        chunking_service=ChunkingService(document_service=DocumentService()),
        embedding_service=EmbeddingService(embedding_model=FakeEmbeddingModel()),
        vector_store=InMemoryVectorStore(),
    )


def test_index_text_returns_number_of_chunks_indexed():
    service = _service()

    chunk_count = asyncio.run(
        service.index_text(
            text="word " * 500,
            source="unit-test",
            chunk_size=200,
            chunk_overlap=20,
        )
    )

    assert chunk_count > 1


def test_search_finds_previously_indexed_text():
    service = _service()

    asyncio.run(
        service.index_text(
            text="Enterprise RAG systems retrieve relevant context.",
            source="unit-test",
        )
    )

    results = asyncio.run(service.search(query="Enterprise RAG systems", k=4))

    assert len(results) == 1
    assert "Enterprise RAG" in results[0].document.page_content


def test_search_rejects_empty_query():
    service = _service()

    with pytest.raises(ValueError):
        asyncio.run(service.search(query="   "))


def test_search_returns_empty_list_when_nothing_indexed():
    service = _service()

    results = asyncio.run(service.search(query="anything"))

    assert results == []

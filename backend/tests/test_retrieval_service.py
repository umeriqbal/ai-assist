import asyncio

import pytest

from app.rag.stores.in_memory_vector_store import InMemoryVectorStore
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.services.vector_store_service import VectorStoreService
from tests.conftest import FakeEmbeddingModel


def _services() -> tuple[VectorStoreService, RetrievalService]:
    embedding_service = EmbeddingService(embedding_model=FakeEmbeddingModel())
    vector_store = InMemoryVectorStore()

    indexer = VectorStoreService(
        chunking_service=ChunkingService(document_service=DocumentService()),
        embedding_service=embedding_service,
        vector_store=vector_store,
    )
    retriever = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    return indexer, retriever


def test_retrieve_finds_previously_indexed_text():
    indexer, retriever = _services()

    asyncio.run(
        indexer.index_text(
            text="Enterprise RAG systems retrieve relevant context.",
            source="unit-test",
        )
    )

    results = asyncio.run(retriever.retrieve(query="Enterprise RAG systems", k=4))

    assert len(results) == 1
    assert "Enterprise RAG" in results[0].document.page_content


def test_retrieve_filters_by_source():
    indexer, retriever = _services()

    asyncio.run(indexer.index_text(text="HR policy details.", source="hr.txt"))
    asyncio.run(indexer.index_text(text="Engineering runbook details.", source="eng.txt"))

    results = asyncio.run(retriever.retrieve(query="details", k=10, source="hr.txt"))

    assert len(results) == 1
    assert results[0].document.metadata["source"] == "hr.txt"


def test_retrieve_without_source_returns_all_matches():
    indexer, retriever = _services()

    asyncio.run(indexer.index_text(text="HR policy details.", source="hr.txt"))
    asyncio.run(indexer.index_text(text="Engineering runbook details.", source="eng.txt"))

    results = asyncio.run(retriever.retrieve(query="details", k=10))

    assert len(results) == 2


def test_retrieve_rejects_empty_query():
    _, retriever = _services()

    with pytest.raises(ValueError):
        asyncio.run(retriever.retrieve(query="   "))


def test_retrieve_returns_empty_list_when_nothing_indexed():
    _, retriever = _services()

    results = asyncio.run(retriever.retrieve(query="anything"))

    assert results == []

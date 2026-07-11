import asyncio

from langchain_core.documents import Document

from app.services.embedding_service import EmbeddingService
from tests.conftest import FakeEmbeddingModel


def test_embed_chunks_returns_one_vector_per_chunk():
    model = FakeEmbeddingModel(dimensions=8)
    service = EmbeddingService(embedding_model=model)

    chunks = [
        Document(page_content="first chunk", metadata={"chunk_index": 0}),
        Document(page_content="second chunk", metadata={"chunk_index": 1}),
    ]

    embedded = asyncio.run(service.embed_chunks(chunks))

    assert len(embedded) == 2
    assert all(len(item.vector) == 8 for item in embedded)
    assert embedded[0].document is chunks[0]
    assert embedded[1].document is chunks[1]


def test_embed_chunks_batches_all_texts_in_a_single_call():
    model = FakeEmbeddingModel()
    service = EmbeddingService(embedding_model=model)

    chunks = [
        Document(page_content="a"),
        Document(page_content="bb"),
        Document(page_content="ccc"),
    ]

    asyncio.run(service.embed_chunks(chunks))

    assert len(model.embed_documents_calls) == 1
    assert model.embed_documents_calls[0] == ["a", "bb", "ccc"]


def test_embed_chunks_returns_empty_list_for_no_chunks():
    model = FakeEmbeddingModel()
    service = EmbeddingService(embedding_model=model)

    embedded = asyncio.run(service.embed_chunks([]))

    assert embedded == []


def test_embed_query_returns_a_single_vector():
    model = FakeEmbeddingModel(dimensions=8)
    service = EmbeddingService(embedding_model=model)

    vector = asyncio.run(service.embed_query("hello"))

    assert len(vector) == 8

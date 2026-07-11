import asyncio

import pytest

from app.rag.stores.in_memory_vector_store import InMemoryVectorStore
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.question_answering_service import (
    QuestionAnsweringService,
    _snippet,
)
from app.services.retrieval_service import RetrievalService
from app.services.vector_store_service import VectorStoreService
from tests.conftest import FakeEmbeddingModel, FakeLLMProvider


def _services(response: str = "fake answer"):
    embedding_service = EmbeddingService(embedding_model=FakeEmbeddingModel())
    vector_store = InMemoryVectorStore()
    llm_provider = FakeLLMProvider(response=response)

    indexer = VectorStoreService(
        chunking_service=ChunkingService(document_service=DocumentService()),
        embedding_service=embedding_service,
        vector_store=vector_store,
    )
    retriever = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )
    qa_service = QuestionAnsweringService(
        retrieval_service=retriever,
        llm_provider=llm_provider,
    )

    return indexer, qa_service, llm_provider


def test_answer_returns_llm_response_when_context_is_found():
    indexer, qa_service, llm_provider = _services(response="25 days per year.")

    asyncio.run(
        indexer.index_text(
            text="Employees get 25 days of paid vacation per year.",
            source="hr-policy.txt",
        )
    )

    result = asyncio.run(qa_service.answer(question="How much vacation do I get?"))

    assert result.answer == "25 days per year."
    assert result.chunks_used == 1
    assert len(llm_provider.chat_calls) == 1

    assert len(result.citations) == 1
    citation = result.citations[0]
    assert citation.source == "hr-policy.txt"
    assert citation.snippet == "Employees get 25 days of paid vacation per year."
    assert isinstance(citation.score, float)

    assert result.context == ["Employees get 25 days of paid vacation per year."]


def test_answer_does_not_call_llm_when_nothing_indexed():
    _, qa_service, llm_provider = _services()

    result = asyncio.run(qa_service.answer(question="anything"))

    assert result.chunks_used == 0
    assert result.citations == []
    assert result.context == []
    assert llm_provider.chat_calls == []


def test_answer_applies_min_score_and_skips_llm_when_nothing_qualifies():
    indexer, qa_service, llm_provider = _services()

    asyncio.run(indexer.index_text(text="Some indexed content.", source="doc.txt"))

    result = asyncio.run(
        qa_service.answer(question="anything", min_score=2.0)
    )

    assert result.chunks_used == 0
    assert llm_provider.chat_calls == []


def test_answer_rejects_empty_question():
    _, qa_service, _ = _services()

    with pytest.raises(ValueError):
        asyncio.run(qa_service.answer(question="   "))


def test_snippet_passes_short_text_through_unchanged():
    text = "Short chunk content."

    assert _snippet(text, max_length=200) == text


def test_snippet_truncates_long_text_with_ellipsis():
    text = "word " * 100

    snippet = _snippet(text, max_length=50)

    assert len(snippet) <= 53
    assert snippet.endswith("...")
    assert text.startswith(snippet[:-3])

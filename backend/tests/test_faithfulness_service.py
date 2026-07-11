import asyncio

from app.rag.stores.in_memory_vector_store import InMemoryVectorStore
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.faithfulness_service import FaithfulnessService
from app.services.question_answering_service import QuestionAnsweringService
from app.services.retrieval_service import RetrievalService
from app.services.vector_store_service import VectorStoreService
from tests.conftest import FakeEmbeddingModel, FakeLLMProvider


def _setup(answer_response: str, judge_response: str):
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
    qa_service = QuestionAnsweringService(
        retrieval_service=retriever,
        llm_provider=FakeLLMProvider(response=answer_response),
    )
    judge_provider = FakeLLMProvider(response=judge_response)
    faithfulness_service = FaithfulnessService(
        question_answering_service=qa_service,
        llm_provider=judge_provider,
    )

    return indexer, faithfulness_service, judge_provider


def test_faithful_answer_is_reported_as_faithful():
    indexer, faithfulness_service, judge_provider = _setup(
        answer_response="Employees get 25 vacation days.",
        judge_response='{"faithful": true, "unsupported_claims": []}',
    )

    asyncio.run(
        indexer.index_text(
            text="Employees get 25 days of paid vacation per year.",
            source="hr-policy.txt",
        )
    )

    result = asyncio.run(
        faithfulness_service.evaluate(question="How much vacation do I get?")
    )

    assert result.is_faithful is True
    assert result.unsupported_claims == []
    assert len(judge_provider.chat_calls) == 1


def test_unfaithful_answer_lists_unsupported_claims():
    indexer, faithfulness_service, _ = _setup(
        answer_response="Employees get 25 vacation days and free parking.",
        judge_response=(
            '{"faithful": false, "unsupported_claims": '
            '["free parking"]}'
        ),
    )

    asyncio.run(
        indexer.index_text(
            text="Employees get 25 days of paid vacation per year.",
            source="hr-policy.txt",
        )
    )

    result = asyncio.run(
        faithfulness_service.evaluate(question="How much vacation do I get?")
    )

    assert result.is_faithful is False
    assert result.unsupported_claims == ["free parking"]


def test_malformed_judge_response_reports_unknown_not_a_crash():
    indexer, faithfulness_service, _ = _setup(
        answer_response="Employees get 25 vacation days.",
        judge_response="I cannot comply with that request.",
    )

    asyncio.run(
        indexer.index_text(
            text="Employees get 25 days of paid vacation per year.",
            source="hr-policy.txt",
        )
    )

    result = asyncio.run(
        faithfulness_service.evaluate(question="How much vacation do I get?")
    )

    assert result.is_faithful is None
    assert result.unsupported_claims == []
    assert result.raw_verdict == "I cannot comply with that request."


def test_judge_response_wrapped_in_code_fence_still_parses():
    indexer, faithfulness_service, _ = _setup(
        answer_response="Employees get 25 vacation days.",
        judge_response='```json\n{"faithful": true, "unsupported_claims": []}\n```',
    )

    asyncio.run(
        indexer.index_text(
            text="Employees get 25 days of paid vacation per year.",
            source="hr-policy.txt",
        )
    )

    result = asyncio.run(
        faithfulness_service.evaluate(question="How much vacation do I get?")
    )

    assert result.is_faithful is True


def test_no_context_short_circuits_without_calling_the_judge():
    _, faithfulness_service, judge_provider = _setup(
        answer_response="unused",
        judge_response="unused",
    )

    result = asyncio.run(faithfulness_service.evaluate(question="anything"))

    assert result.is_faithful is True
    assert result.unsupported_claims == []
    assert judge_provider.chat_calls == []

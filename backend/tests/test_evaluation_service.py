import asyncio

import pytest

from app.rag.stores.in_memory_vector_store import InMemoryVectorStore
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.evaluation_service import EvaluationCase, EvaluationService
from app.services.retrieval_service import RetrievalService
from app.services.vector_store_service import VectorStoreService
from tests.conftest import FakeEmbeddingModel


def _setup():
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
    evaluator = EvaluationService(retrieval_service=retriever)

    return indexer, evaluator


def test_perfect_retrieval_scores_full_recall_and_precision():
    indexer, evaluator = _setup()

    asyncio.run(indexer.index_text(text="HR policy content.", source="hr.txt"))

    report = asyncio.run(
        evaluator.evaluate_retrieval(
            cases=[
                EvaluationCase(question="anything", expected_sources=["hr.txt"]),
            ],
            k=1,
        )
    )

    assert report.results[0].recall == 1.0
    assert report.results[0].precision == 1.0
    assert report.mean_recall == 1.0
    assert report.mean_precision == 1.0


def test_missed_retrieval_scores_zero_recall():
    indexer, evaluator = _setup()

    asyncio.run(indexer.index_text(text="Engineering runbook.", source="eng.txt"))

    report = asyncio.run(
        evaluator.evaluate_retrieval(
            cases=[
                EvaluationCase(question="anything", expected_sources=["hr.txt"]),
            ],
            k=4,
        )
    )

    assert report.results[0].recall == 0.0
    assert report.results[0].precision == 0.0


def test_noisy_retrieval_lowers_precision_but_keeps_full_recall():
    indexer, evaluator = _setup()

    asyncio.run(indexer.index_text(text="HR policy content.", source="hr.txt"))
    asyncio.run(indexer.index_text(text="Engineering runbook.", source="eng.txt"))

    report = asyncio.run(
        evaluator.evaluate_retrieval(
            cases=[
                EvaluationCase(question="anything", expected_sources=["hr.txt"]),
            ],
            k=2,
        )
    )

    result = report.results[0]
    assert result.recall == 1.0
    assert result.precision == 0.5


def test_mean_metrics_average_across_multiple_cases():
    indexer, evaluator = _setup()

    asyncio.run(indexer.index_text(text="HR policy content.", source="hr.txt"))

    report = asyncio.run(
        evaluator.evaluate_retrieval(
            cases=[
                EvaluationCase(question="q1", expected_sources=["hr.txt"]),
                EvaluationCase(question="q2", expected_sources=["nonexistent.txt"]),
            ],
            k=1,
        )
    )

    assert report.mean_recall == 0.5
    assert report.mean_precision == 0.5


def test_no_retrieved_chunks_gives_zero_precision_not_an_error():
    _, evaluator = _setup()

    report = asyncio.run(
        evaluator.evaluate_retrieval(
            cases=[
                EvaluationCase(question="anything", expected_sources=["hr.txt"]),
            ],
        )
    )

    assert report.results[0].precision == 0.0
    assert report.results[0].recall == 0.0


def test_evaluate_retrieval_rejects_empty_case_list():
    _, evaluator = _setup()

    with pytest.raises(ValueError):
        asyncio.run(evaluator.evaluate_retrieval(cases=[]))

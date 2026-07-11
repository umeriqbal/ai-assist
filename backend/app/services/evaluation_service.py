from dataclasses import dataclass

from app.services.retrieval_service import RetrievalService


@dataclass
class EvaluationCase:
    """
    A labeled test case: a question and the sources that should be
    retrieved to answer it.
    """

    question: str
    expected_sources: list[str]


@dataclass
class EvaluationCaseResult:
    """
    The outcome of running one EvaluationCase through retrieval.
    """

    question: str
    expected_sources: list[str]
    retrieved_sources: list[str]
    recall: float
    precision: float


@dataclass
class RetrievalEvaluationReport:
    """
    Aggregate retrieval quality across a labeled evaluation set.
    """

    results: list[EvaluationCaseResult]
    mean_recall: float
    mean_precision: float


class EvaluationService:
    """
    Business service responsible for measuring RAG pipeline quality.
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
    ) -> None:
        self._retrieval_service = retrieval_service

    async def evaluate_retrieval(
        self,
        cases: list[EvaluationCase],
        k: int = 4,
    ) -> RetrievalEvaluationReport:

        if not cases:
            raise ValueError("At least one evaluation case is required.")

        results = [
            await self._evaluate_case(case, k)
            for case in cases
        ]

        mean_recall = sum(result.recall for result in results) / len(results)
        mean_precision = sum(result.precision for result in results) / len(results)

        return RetrievalEvaluationReport(
            results=results,
            mean_recall=mean_recall,
            mean_precision=mean_precision,
        )

    async def _evaluate_case(
        self,
        case: EvaluationCase,
        k: int,
    ) -> EvaluationCaseResult:

        scored_chunks = await self._retrieval_service.retrieve(
            query=case.question,
            k=k,
        )

        retrieved_sources = [
            chunk.document.metadata.get("source", "unknown")
            for chunk in scored_chunks
        ]

        expected = set(case.expected_sources)
        found = expected & set(retrieved_sources)

        recall = len(found) / len(expected) if expected else 0.0

        precision = (
            sum(1 for source in retrieved_sources if source in expected)
            / len(retrieved_sources)
            if retrieved_sources
            else 0.0
        )

        return EvaluationCaseResult(
            question=case.question,
            expected_sources=case.expected_sources,
            retrieved_sources=retrieved_sources,
            recall=recall,
            precision=precision,
        )

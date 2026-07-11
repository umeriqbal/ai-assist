from dataclasses import dataclass

from app.providers.base import LLMProvider
from app.rag.prompts.prompt_builder import PromptBuilder
from app.services.retrieval_service import RetrievalService

_NO_CONTEXT_ANSWER = (
    "I don't have enough information in the indexed documents to answer that."
)


@dataclass
class AnswerResult:
    """
    The result of a grounded question-answering request.
    """

    answer: str
    sources: list[str]
    chunks_used: int


class QuestionAnsweringService:
    """
    Business service responsible for grounded question answering.
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm_provider: LLMProvider,
    ) -> None:
        self._retrieval_service = retrieval_service
        self._llm_provider = llm_provider

    async def answer(
        self,
        question: str,
        k: int = 4,
        source: str | None = None,
        min_score: float | None = None,
    ) -> AnswerResult:

        results = await self._retrieval_service.retrieve(
            query=question,
            k=k,
            source=source,
        )

        if min_score is not None:
            results = [result for result in results if result.score >= min_score]

        if not results:
            return AnswerResult(
                answer=_NO_CONTEXT_ANSWER,
                sources=[],
                chunks_used=0,
            )

        documents = [result.document for result in results]

        prompt = PromptBuilder.build(
            question=question,
            documents=documents,
        )

        answer_text = await self._llm_provider.chat(prompt=prompt)

        sources = sorted(
            {
                document.metadata["source"]
                for document in documents
                if "source" in document.metadata
            }
        )

        return AnswerResult(
            answer=answer_text,
            sources=sources,
            chunks_used=len(results),
        )

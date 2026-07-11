from dataclasses import dataclass

from app.providers.base import LLMProvider
from app.rag.prompts.prompt_builder import PromptBuilder
from app.services.retrieval_service import RetrievalService

_NO_CONTEXT_ANSWER = (
    "I don't have enough information in the indexed documents to answer that."
)

_SNIPPET_MAX_LENGTH = 200


def _snippet(text: str, max_length: int = _SNIPPET_MAX_LENGTH) -> str:
    if len(text) <= max_length:
        return text

    return text[:max_length].rstrip() + "..."


@dataclass
class Citation:
    """
    Evidence for one chunk that contributed to an answer.

    `score` is the chunk's cosine similarity to the question — a
    relevance signal, not a measure of whether the answer itself is
    correct.
    """

    source: str
    score: float
    snippet: str


@dataclass
class AnswerResult:
    """
    The result of a grounded question-answering request.

    `context` holds the full, untruncated text of every chunk used to
    produce the answer — for internal use (e.g. faithfulness
    evaluation), since `citations` only carries a truncated snippet
    meant for display.
    """

    answer: str
    citations: list[Citation]
    chunks_used: int
    context: list[str]


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
                citations=[],
                chunks_used=0,
                context=[],
            )

        documents = [result.document for result in results]

        prompt = PromptBuilder.build(
            question=question,
            documents=documents,
        )

        answer_text = await self._llm_provider.chat(prompt=prompt)

        citations = [
            Citation(
                source=result.document.metadata.get("source", "unknown"),
                score=result.score,
                snippet=_snippet(result.document.page_content),
            )
            for result in results
        ]

        return AnswerResult(
            answer=answer_text,
            citations=citations,
            chunks_used=len(results),
            context=[document.page_content for document in documents],
        )

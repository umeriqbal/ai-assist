import json
import re
from dataclasses import dataclass

from app.providers.base import LLMProvider
from app.rag.prompts.faithfulness_prompt_builder import FaithfulnessPromptBuilder
from app.services.question_answering_service import QuestionAnsweringService

_NO_CONTEXT_VERDICT = (
    "No context was retrieved; the LLM was never called, so there is "
    "nothing to fact-check."
)

_CODE_FENCE_PATTERN = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


@dataclass
class FaithfulnessResult:
    """
    The outcome of judging whether a generated answer is fully
    supported by the context it was grounded in.

    `is_faithful` is `None` when the judge's response couldn't be
    parsed — that is reported explicitly rather than guessed.
    """

    question: str
    answer: str
    is_faithful: bool | None
    unsupported_claims: list[str]
    raw_verdict: str


class FaithfulnessService:
    """
    Business service responsible for judging answer faithfulness.
    """

    def __init__(
        self,
        question_answering_service: QuestionAnsweringService,
        llm_provider: LLMProvider,
    ) -> None:
        self._question_answering_service = question_answering_service
        self._llm_provider = llm_provider

    async def evaluate(
        self,
        question: str,
        k: int = 4,
        source: str | None = None,
        min_score: float | None = None,
    ) -> FaithfulnessResult:

        result = await self._question_answering_service.answer(
            question=question,
            k=k,
            source=source,
            min_score=min_score,
        )

        if result.chunks_used == 0:
            return FaithfulnessResult(
                question=question,
                answer=result.answer,
                is_faithful=True,
                unsupported_claims=[],
                raw_verdict=_NO_CONTEXT_VERDICT,
            )

        judge_prompt = FaithfulnessPromptBuilder.build(
            question=question,
            answer=result.answer,
            context=result.context,
        )

        raw_verdict = await self._llm_provider.chat(prompt=judge_prompt)

        return self._parse_verdict(
            question=question,
            answer=result.answer,
            raw_verdict=raw_verdict,
        )

    def _parse_verdict(
        self,
        question: str,
        answer: str,
        raw_verdict: str,
    ) -> FaithfulnessResult:

        cleaned = _CODE_FENCE_PATTERN.sub("", raw_verdict).strip()

        try:
            verdict = json.loads(cleaned)
            is_faithful = bool(verdict["faithful"])
            unsupported_claims = list(verdict.get("unsupported_claims", []))
        except (json.JSONDecodeError, KeyError, TypeError):
            is_faithful = None
            unsupported_claims = []

        return FaithfulnessResult(
            question=question,
            answer=answer,
            is_faithful=is_faithful,
            unsupported_claims=unsupported_claims,
            raw_verdict=raw_verdict,
        )

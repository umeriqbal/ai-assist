from dataclasses import dataclass

from app.agents.reflector import Reflector
from app.services.agent_service import AgentService


@dataclass
class Draft:
    """
    One iteration of an answer and the critique it received.
    """

    answer: str
    critique_feedback: str
    was_satisfactory: bool


@dataclass
class ReflectionResult:
    """
    The outcome of a reflect-and-revise loop: the final answer and
    every draft that led to it.
    """

    answer: str
    drafts: list[Draft]


def _revision_prompt(question: str, previous_answer: str, feedback: str) -> str:
    return (
        f"Question: {question}\n\n"
        f"Your previous answer: {previous_answer}\n\n"
        f"Feedback on that answer: {feedback}\n\n"
        "Revise your answer to address the feedback."
    )


class ReflectionService:
    """
    Business service that generates an answer, critiques it, and
    revises it until satisfactory or an iteration limit is reached.

    Unlike `AgentService`'s tool loop, hitting the iteration limit is
    not an error here: the last revision is returned as a best-effort
    answer rather than failing the request.
    """

    def __init__(
        self,
        agent_service: AgentService,
        reflector: Reflector,
        max_iterations: int = 3,
    ) -> None:
        self._agent_service = agent_service
        self._reflector = reflector
        self._max_iterations = max_iterations

    async def run(self, question: str) -> ReflectionResult:

        question = question.strip()

        if not question:
            raise ValueError("Question cannot be empty.")

        answer = await self._agent_service.chat(question)
        drafts: list[Draft] = []

        for _ in range(self._max_iterations):

            critique = await self._reflector.critique(question, answer)
            drafts.append(
                Draft(
                    answer=answer,
                    critique_feedback=critique.feedback,
                    was_satisfactory=critique.is_satisfactory,
                )
            )

            if critique.is_satisfactory:
                break

            answer = await self._agent_service.chat(
                _revision_prompt(question, answer, critique.feedback)
            )

        return ReflectionResult(answer=answer, drafts=drafts)

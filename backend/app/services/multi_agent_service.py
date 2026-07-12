from dataclasses import dataclass
from typing import Any

from langgraph.errors import GraphRecursionError

from app.agents.multi_agent_graph import build_multi_agent_graph
from app.agents.supervisor import Supervisor
from app.providers.base import LLMProvider
from app.services.agent_service import AgentService


@dataclass
class AgentTurn:
    """
    One specialist's contribution to a collaborative answer.
    """

    agent: str
    message: str


@dataclass
class MultiAgentResult:
    """
    The outcome of a multi-agent collaboration: the final answer and
    the full transcript of which specialist said what.
    """

    answer: str
    transcript: list[AgentTurn]


class MultiAgentService:
    """
    Business service that coordinates a Researcher and a Writer
    specialist through a Supervisor, until the task is done.
    """

    def __init__(
        self,
        provider: LLMProvider,
        researcher: AgentService,
        writer: AgentService,
        max_iterations: int = 6,
    ) -> None:
        self._graph = build_multi_agent_graph(
            supervisor=Supervisor(provider=provider),
            researcher=researcher,
            writer=writer,
        )
        self._recursion_limit = max_iterations * 2 + 1

    async def run(self, prompt: str) -> MultiAgentResult:

        prompt = prompt.strip()

        if not prompt:
            raise ValueError("Prompt cannot be empty.")

        config: dict[str, Any] = {"recursion_limit": self._recursion_limit}

        try:
            result = await self._graph.ainvoke(
                {
                    "messages": [{"role": "user", "content": prompt}],
                    "next": "",
                    "instructions": "",
                },
                config=config,
            )
        except GraphRecursionError as exc:
            raise RuntimeError(
                "Agents did not produce a final answer within the iteration limit."
            ) from exc

        transcript = [
            AgentTurn(
                agent=message.get("name", message["role"]),
                message=message["content"],
            )
            for message in result["messages"][1:]
        ]

        answer = transcript[-1].message if transcript else ""

        return MultiAgentResult(answer=answer, transcript=transcript)

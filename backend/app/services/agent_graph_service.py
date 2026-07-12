from typing import Any

from langgraph.errors import GraphRecursionError

from app.agents.agent_graph import build_agent_graph
from app.providers.base import LLMProvider
from app.tools.tool import Tool


class AgentGraphService:
    """
    Business service that runs the agent loop via a LangGraph graph
    instead of a hand-written loop, using the graph's checkpointer
    (keyed by `conversation_id`) for state management instead of
    `ConversationMemory`.
    """

    def __init__(
        self,
        provider: LLMProvider,
        tools: list[Tool],
        max_iterations: int = 5,
    ) -> None:
        self._graph = build_agent_graph(provider=provider, tools=tools)
        self._recursion_limit = max_iterations * 2 + 1

    async def chat(
        self,
        prompt: str,
        conversation_id: str,
    ) -> str:

        prompt = prompt.strip()

        config: dict[str, Any] = {
            "configurable": {"thread_id": conversation_id},
            "recursion_limit": self._recursion_limit,
        }

        try:
            result = await self._graph.ainvoke(
                {
                    "messages": [{"role": "user", "content": prompt}],
                    "pending_tool_calls": [],
                },
                config=config,
            )
        except GraphRecursionError as exc:
            raise RuntimeError(
                "Agent did not produce a final answer within the iteration limit."
            ) from exc

        return result["messages"][-1]["content"]

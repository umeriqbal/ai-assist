import operator
from typing import Annotated, Any, TypedDict

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.agents.supervisor import Supervisor
from app.services.agent_service import AgentService


class MultiAgentState(TypedDict):
    """
    State threaded through the graph. `messages` accumulates every
    specialist's contribution; `next`/`instructions` are the
    supervisor's routing decision for the current turn.
    """

    messages: Annotated[list[dict[str, Any]], operator.add]
    next: str
    instructions: str


def build_multi_agent_graph(
    supervisor: Supervisor,
    researcher: AgentService,
    writer: AgentService,
) -> CompiledStateGraph:
    """
    Build a graph where a Supervisor decides, turn by turn, whether the
    Researcher or the Writer specialist should act next, or whether the
    task is done. No checkpointer — this sprint deliberately doesn't
    add cross-call memory; Sprints 4/5 already demonstrated that.
    """

    async def supervisor_node(state: MultiAgentState) -> dict[str, Any]:
        decision = await supervisor.decide(state["messages"])
        return {"next": decision.next, "instructions": decision.instructions}

    async def researcher_node(state: MultiAgentState) -> dict[str, Any]:
        answer = await researcher.chat(state["instructions"])
        return {
            "messages": [
                {"role": "assistant", "name": "researcher", "content": answer}
            ]
        }

    async def writer_node(state: MultiAgentState) -> dict[str, Any]:
        answer = await writer.chat(state["instructions"])
        return {
            "messages": [{"role": "assistant", "name": "writer", "content": answer}]
        }

    def route_after_supervisor(state: MultiAgentState) -> str:
        return state["next"]

    graph = StateGraph(MultiAgentState)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)
    graph.set_entry_point("supervisor")
    graph.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {"researcher": "researcher", "writer": "writer", "finish": END},
    )
    graph.add_edge("researcher", "supervisor")
    graph.add_edge("writer", "supervisor")

    return graph.compile()

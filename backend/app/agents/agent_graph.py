import operator
from typing import Annotated, Any, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.providers.base import LLMProvider
from app.providers.tool_call import ToolCall
from app.tools.tool import Tool


class AgentGraphState(TypedDict):
    """
    State threaded through the graph. `messages` accumulates across
    nodes (and across calls, via the checkpointer); `pending_tool_calls`
    is scratch space for the current turn only.
    """

    messages: Annotated[list[dict[str, Any]], operator.add]
    pending_tool_calls: list[ToolCall]


def build_agent_graph(
    provider: LLMProvider,
    tools: list[Tool],
) -> CompiledStateGraph:
    """
    Build the Sprint 1 ReAct loop as a LangGraph graph: same
    `LLMProvider`/`Tool` calls `AgentService` makes, orchestrated by
    graph nodes and a conditional edge instead of a hand-written loop.

    Compiled with an in-memory checkpointer — process-local and
    non-persistent by design, same trade-off as `InMemoryVectorStore`
    and `InMemoryConversationMemory`.
    """

    tools_by_name = {tool.name: tool for tool in tools}

    async def call_model(state: AgentGraphState) -> dict[str, Any]:

        result = await provider.chat_with_tools(
            messages=state["messages"],
            tools=tools,
        )

        if result.has_tool_calls:
            return {"pending_tool_calls": result.tool_calls}

        return {
            "messages": [{"role": "assistant", "content": result.output_text or ""}],
            "pending_tool_calls": [],
        }

    async def call_tools(state: AgentGraphState) -> dict[str, Any]:

        new_messages: list[dict[str, Any]] = []

        for tool_call in state["pending_tool_calls"]:

            tool = tools_by_name.get(tool_call.name)

            output = (
                await tool.execute(**tool_call.arguments)
                if tool
                else f"Error: unknown tool '{tool_call.name}'"
            )

            new_messages += provider.tool_result_messages(
                tool_call=tool_call,
                result=output,
            )

        return {"messages": new_messages, "pending_tool_calls": []}

    def route_after_model(state: AgentGraphState) -> str:
        return "call_tools" if state["pending_tool_calls"] else END

    graph = StateGraph(AgentGraphState)
    graph.add_node("call_model", call_model)
    graph.add_node("call_tools", call_tools)
    graph.set_entry_point("call_model")
    graph.add_conditional_edges(
        "call_model",
        route_after_model,
        {"call_tools": "call_tools", END: END},
    )
    graph.add_edge("call_tools", "call_model")

    return graph.compile(checkpointer=MemorySaver())

from app.agents.memory import ConversationMemory
from app.providers.base import LLMProvider
from app.tools.tool import Tool


class AgentService:
    """
    Business service that runs the agent loop: ask the model, execute
    any requested tools, feed their results back, and repeat until the
    model produces a final answer.
    """

    def __init__(
        self,
        provider: LLMProvider,
        tools: list[Tool],
        memory: ConversationMemory | None = None,
        max_iterations: int = 5,
    ) -> None:
        self._provider = provider
        self._tools = {tool.name: tool for tool in tools}
        self._memory = memory
        self._max_iterations = max_iterations

    async def chat(
        self,
        prompt: str,
        conversation_id: str | None = None,
    ) -> str:

        prompt = prompt.strip()

        if conversation_id is not None and self._memory is None:
            raise ValueError("Conversation memory is not configured for this agent.")

        history: list[dict] = (
            await self._memory.get_history(conversation_id)
            if conversation_id is not None
            else []
        )

        messages: list[dict] = [*history, {"role": "user", "content": prompt}]

        for _ in range(self._max_iterations):

            result = await self._provider.chat_with_tools(
                messages=messages,
                tools=list(self._tools.values()),
            )

            if not result.has_tool_calls:
                answer = result.output_text or ""

                if conversation_id is not None:
                    await self._memory.append_turn(
                        conversation_id=conversation_id,
                        user_message=prompt,
                        assistant_message=answer,
                    )

                return answer

            for tool_call in result.tool_calls:

                tool = self._tools.get(tool_call.name)

                output = (
                    await tool.execute(**tool_call.arguments)
                    if tool
                    else f"Error: unknown tool '{tool_call.name}'"
                )

                messages += self._provider.tool_result_messages(
                    tool_call=tool_call,
                    result=output,
                )

        raise RuntimeError(
            "Agent did not produce a final answer within the iteration limit."
        )

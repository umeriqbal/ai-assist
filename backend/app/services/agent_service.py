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
        max_iterations: int = 5,
    ) -> None:
        self._provider = provider
        self._tools = {tool.name: tool for tool in tools}
        self._max_iterations = max_iterations

    async def chat(
        self,
        prompt: str,
    ) -> str:

        prompt = prompt.strip()

        messages: list[dict] = [{"role": "user", "content": prompt}]

        for _ in range(self._max_iterations):

            result = await self._provider.chat_with_tools(
                messages=messages,
                tools=list(self._tools.values()),
            )

            if not result.has_tool_calls:
                return result.output_text or ""

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

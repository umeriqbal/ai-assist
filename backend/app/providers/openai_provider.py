import json
from collections.abc import AsyncIterator
from typing import Any

from openai import AsyncOpenAI

from app.core.config import settings
from app.providers.base import LLMProvider
from app.providers.chat_result import ChatResult
from app.providers.tool_call import ToolCall
from app.tools.tool import Tool


class OpenAIProvider(LLMProvider):
    """
    OpenAI implementation of the LLM provider interface.
    """

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key=settings.openai_api_key,
        )

    async def health_check(self) -> bool:
        return self._client is not None

    async def chat(
        self,
        prompt: str,
    ) -> str:

        response = await self._client.responses.create(
            model=settings.openai_chat_model,
            input=prompt,
        )

        return response.output_text

    async def stream_chat(
        self,
        prompt: str,
    ) -> AsyncIterator[str]:
        """
        Stream tokens from the OpenAI Responses API.
        """

        stream = await self._client.responses.create(
            model=settings.openai_chat_model,
            input=prompt,
            stream=True,
        )

        async for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta

    async def chat_with_tools(
        self,
        messages: list[dict[str, Any]],
        tools: list[Tool],
    ) -> ChatResult:

        openai_tools = [
            {
                "type": "function",
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
            }
            for tool in tools
        ]

        response = await self._client.responses.create(
            model=settings.openai_chat_model,
            input=messages,
            tools=openai_tools,
        )

        tool_calls = [
            ToolCall(
                id=item.call_id,
                name=item.name,
                arguments=json.loads(item.arguments),
            )
            for item in response.output
            if item.type == "function_call"
        ]

        return ChatResult(
            output_text=response.output_text or None,
            tool_calls=tool_calls,
        )

    def tool_result_messages(
        self,
        tool_call: ToolCall,
        result: str,
    ) -> list[dict[str, Any]]:

        return [
            {
                "type": "function_call",
                "call_id": tool_call.id,
                "name": tool_call.name,
                "arguments": json.dumps(tool_call.arguments),
            },
            {
                "type": "function_call_output",
                "call_id": tool_call.id,
                "output": result,
            },
        ]

    async def generate_structured(
        self,
        prompt: str,
        schema: dict[str, Any],
        schema_name: str,
    ) -> dict[str, Any]:

        response = await self._client.responses.create(
            model=settings.openai_chat_model,
            input=prompt,
            text={
                "format": {
                    "type": "json_schema",
                    "name": schema_name,
                    "schema": schema,
                    "strict": True,
                }
            },
        )

        return json.loads(response.output_text)
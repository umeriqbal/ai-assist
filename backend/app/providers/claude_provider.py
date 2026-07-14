import json
from collections.abc import AsyncIterator
from typing import Any

from anthropic import AsyncAnthropic

from app.core.config import settings
from app.providers.base import LLMProvider
from app.providers.chat_result import ChatResult
from app.providers.tool_call import ToolCall
from app.tools.tool import Tool

_MAX_TOKENS = 4096


def _text_content(blocks: list[Any]) -> str:
    return "".join(block.text for block in blocks if block.type == "text")


class ClaudeProvider(LLMProvider):
    """
    Anthropic (Claude) implementation of the LLM provider interface.
    """

    def __init__(self) -> None:
        if not settings.anthropic_api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is not configured — set it in .env "
                "to use ClaudeProvider."
            )

        self._client = AsyncAnthropic(
            api_key=settings.anthropic_api_key,
        )

    async def health_check(self) -> bool:
        return self._client is not None

    async def chat(
        self,
        prompt: str,
    ) -> str:

        response = await self._client.messages.create(
            model=settings.anthropic_chat_model,
            max_tokens=_MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )

        return _text_content(response.content)

    async def stream_chat(
        self,
        prompt: str,
    ) -> AsyncIterator[str]:
        """
        Stream text deltas from the Messages API.
        """

        async with self._client.messages.stream(
            model=settings.anthropic_chat_model,
            max_tokens=_MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            async for event in stream:
                if (
                    event.type == "content_block_delta"
                    and event.delta.type == "text_delta"
                ):
                    yield event.delta.text

    async def chat_with_tools(
        self,
        messages: list[dict[str, Any]],
        tools: list[Tool],
    ) -> ChatResult:
        """
        Unlike OpenAI's Responses API, Claude's Messages API takes a
        system prompt as its own top-level `system` parameter rather
        than as a `{"role": "system", ...}` entry inside `messages` —
        so any such entries have to be pulled out here before the rest
        of the conversation is sent.
        """

        system_prompt = "\n\n".join(
            message["content"]
            for message in messages
            if message.get("role") == "system"
        )
        conversation = [
            message for message in messages if message.get("role") != "system"
        ]

        claude_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.parameters,
            }
            for tool in tools
        ]

        kwargs: dict[str, Any] = {
            "model": settings.anthropic_chat_model,
            "max_tokens": _MAX_TOKENS,
            "messages": conversation,
            "tools": claude_tools,
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = await self._client.messages.create(**kwargs)

        tool_calls = [
            ToolCall(id=block.id, name=block.name, arguments=block.input)
            for block in response.content
            if block.type == "tool_use"
        ]

        return ChatResult(
            output_text=_text_content(response.content) or None,
            tool_calls=tool_calls,
        )

    def tool_result_messages(
        self,
        tool_call: ToolCall,
        result: str,
    ) -> list[dict[str, Any]]:

        return [
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "tool_use",
                        "id": tool_call.id,
                        "name": tool_call.name,
                        "input": tool_call.arguments,
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": result,
                    }
                ],
            },
        ]

    async def generate_structured(
        self,
        prompt: str,
        schema: dict[str, Any],
        schema_name: str,
    ) -> dict[str, Any]:

        response = await self._client.messages.create(
            model=settings.anthropic_chat_model,
            max_tokens=_MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
            output_config={
                "format": {
                    "type": "json_schema",
                    "schema": schema,
                }
            },
        )

        return json.loads(_text_content(response.content))

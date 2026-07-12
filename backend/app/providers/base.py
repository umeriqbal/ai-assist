from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any

from app.providers.chat_result import ChatResult
from app.providers.tool_call import ToolCall
from app.tools.tool import Tool


class LLMProvider(ABC):
    """
    Abstract interface implemented by all LLM providers.
    """

    @abstractmethod
    async def health_check(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def chat(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def stream_chat(
        self,
        prompt: str,
    ) -> AsyncIterator[str]:
        """
        Stream a response token-by-token.
        """
        raise NotImplementedError

    @abstractmethod
    async def chat_with_tools(
        self,
        messages: list[dict[str, Any]],
        tools: list[Tool],
    ) -> ChatResult:
        """
        Send a conversation and the tools available to the model, and
        return either a final text answer, requested tool calls, or both.
        """
        raise NotImplementedError

    @abstractmethod
    def tool_result_messages(
        self,
        tool_call: ToolCall,
        result: str,
    ) -> list[dict[str, Any]]:
        """
        Build the provider-specific message item(s) representing a
        requested tool call and its result, ready to append to the
        conversation passed into the next `chat_with_tools` call.
        """
        raise NotImplementedError

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        schema: dict[str, Any],
        schema_name: str,
    ) -> dict[str, Any]:
        """
        Return a JSON object constrained to match `schema`, instead of
        free text. `schema_name` identifies the schema to the model
        (letters, digits, underscores, dashes only).
        """
        raise NotImplementedError
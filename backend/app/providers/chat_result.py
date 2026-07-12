from dataclasses import dataclass, field

from app.providers.tool_call import ToolCall


@dataclass
class ChatResult:
    """
    The outcome of a tool-aware chat turn: either a final text answer,
    one or more requested tool calls, or both.
    """

    output_text: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)

    @property
    def has_tool_calls(self) -> bool:
        return len(self.tool_calls) > 0

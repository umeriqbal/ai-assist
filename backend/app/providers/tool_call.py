from dataclasses import dataclass
from typing import Any


@dataclass
class ToolCall:
    """
    A request from the model to invoke a specific tool with specific
    arguments.
    """

    id: str
    name: str
    arguments: dict[str, Any]

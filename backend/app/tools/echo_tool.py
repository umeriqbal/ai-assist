from typing import Any

from app.tools.tool import Tool


class EchoTool(Tool):
    """
    Trivial tool that returns its input unchanged.

    Exists to validate the `Tool` contract before any real
    tool (or the agent loop that calls it) is built.
    """

    @property
    def name(self) -> str:
        return "echo"

    @property
    def description(self) -> str:
        return "Return the given text unchanged."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to echo back.",
                },
            },
            "required": ["text"],
        }

    async def execute(self, **kwargs: Any) -> str:
        return kwargs["text"]

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from app.tools.tool import Tool


class MCPToolAdapter(Tool):
    """
    Adapts a tool discovered on a remote MCP server into this
    project's own `Tool` interface, so it can be used by `AgentService`
    exactly like a local, in-process tool.
    """

    def __init__(
        self,
        session: ClientSession,
        name: str,
        description: str,
        parameters: dict[str, Any],
    ) -> None:
        self._session = session
        self._name = name
        self._description = description
        self._parameters = parameters

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def parameters(self) -> dict[str, Any]:
        return self._parameters

    async def execute(self, **kwargs: Any) -> str:
        result = await self._session.call_tool(self._name, kwargs)
        return "\n".join(
            block.text for block in result.content if hasattr(block, "text")
        )


async def discover_tools(session: ClientSession) -> list[Tool]:
    """
    List every tool a connected MCP server exposes and adapt each into
    a `Tool` — ready to use without knowing any remote tool names in
    advance.
    """

    tools_result = await session.list_tools()

    return [
        MCPToolAdapter(
            session=session,
            name=tool.name,
            description=tool.description or "",
            parameters=tool.inputSchema,
        )
        for tool in tools_result.tools
    ]


@asynccontextmanager
async def connect_stdio_mcp_server(
    command: str,
    args: list[str],
) -> AsyncIterator[ClientSession]:
    """
    Connect to an MCP server over stdio, spawning it as a subprocess.
    """

    params = StdioServerParameters(command=command, args=args)

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            yield session

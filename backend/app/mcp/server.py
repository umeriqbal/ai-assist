from typing import Any

import mcp.types as types
from mcp.server.lowlevel import Server

from app.tools.tool import Tool


def build_mcp_server(name: str, tools: list[Tool]) -> Server:
    """
    Build an MCP server exposing this project's own `Tool` instances.

    Uses the low-level `Server` API rather than `FastMCP`: `Tool.parameters`
    is already a hand-written JSON Schema, and the low-level API's
    `inputSchema` accepts that directly — no adaptation needed, and no
    fighting FastMCP's type-hint-driven schema inference.
    """

    tools_by_name = {tool.name: tool for tool in tools}

    server = Server(name)

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name=tool.name,
                description=tool.description,
                inputSchema=tool.parameters,
            )
            for tool in tools_by_name.values()
        ]

    @server.call_tool()
    async def call_tool(
        name: str,
        arguments: dict[str, Any],
    ) -> list[types.ContentBlock]:

        tool = tools_by_name.get(name)

        output = (
            await tool.execute(**arguments)
            if tool
            else f"Error: unknown tool '{name}'"
        )

        return [types.TextContent(type="text", text=output)]

    return server

import asyncio

from mcp.shared.memory import create_connected_server_and_client_session

from app.mcp.server import build_mcp_server
from app.tools.echo_tool import EchoTool


def test_list_tools_exposes_tool_name_description_and_schema():
    server = build_mcp_server(name="test-server", tools=[EchoTool()])

    async def scenario():
        async with create_connected_server_and_client_session(server) as client:
            return await client.list_tools()

    result = asyncio.run(scenario())

    assert len(result.tools) == 1
    assert result.tools[0].name == "echo"
    assert result.tools[0].description == EchoTool().description
    assert result.tools[0].inputSchema == EchoTool().parameters


def test_call_tool_executes_the_underlying_tool():
    server = build_mcp_server(name="test-server", tools=[EchoTool()])

    async def scenario():
        async with create_connected_server_and_client_session(server) as client:
            return await client.call_tool("echo", {"text": "hello mcp"})

    result = asyncio.run(scenario())

    assert len(result.content) == 1
    assert result.content[0].text == "hello mcp"


def test_call_tool_reports_unknown_tool_instead_of_crashing():
    server = build_mcp_server(name="test-server", tools=[EchoTool()])

    async def scenario():
        async with create_connected_server_and_client_session(server) as client:
            return await client.call_tool("does_not_exist", {})

    result = asyncio.run(scenario())

    assert "unknown tool" in result.content[0].text


def test_build_mcp_server_can_expose_multiple_tools():
    class SecondTool(EchoTool):
        @property
        def name(self) -> str:
            return "echo_two"

    server = build_mcp_server(name="test-server", tools=[EchoTool(), SecondTool()])

    async def scenario():
        async with create_connected_server_and_client_session(server) as client:
            return await client.list_tools()

    result = asyncio.run(scenario())

    assert {tool.name for tool in result.tools} == {"echo", "echo_two"}

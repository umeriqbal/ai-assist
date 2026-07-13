import asyncio

from mcp.shared.memory import create_connected_server_and_client_session

from app.mcp.client import MCPToolAdapter, discover_tools
from app.mcp.server import build_mcp_server
from app.tools.echo_tool import EchoTool


def test_discover_tools_returns_tool_instances_matching_remote_schema():
    server = build_mcp_server(name="test-server", tools=[EchoTool()])

    async def scenario():
        async with create_connected_server_and_client_session(server) as session:
            return await discover_tools(session)

    tools = asyncio.run(scenario())

    assert len(tools) == 1
    assert tools[0].name == "echo"
    assert tools[0].description == EchoTool().description
    assert tools[0].parameters == EchoTool().parameters


def test_discovered_tool_executes_against_the_remote_server():
    server = build_mcp_server(name="test-server", tools=[EchoTool()])

    async def scenario():
        async with create_connected_server_and_client_session(server) as session:
            tools = await discover_tools(session)
            return await tools[0].execute(text="hello over mcp")

    result = asyncio.run(scenario())

    assert result == "hello over mcp"


def test_discover_tools_returns_one_adapter_per_remote_tool():
    class SecondTool(EchoTool):
        @property
        def name(self) -> str:
            return "echo_two"

    server = build_mcp_server(name="test-server", tools=[EchoTool(), SecondTool()])

    async def scenario():
        async with create_connected_server_and_client_session(server) as session:
            return await discover_tools(session)

    tools = asyncio.run(scenario())

    assert {tool.name for tool in tools} == {"echo", "echo_two"}


def test_mcp_tool_adapter_surfaces_remote_error_text_without_raising():
    server = build_mcp_server(name="test-server", tools=[EchoTool()])

    async def scenario():
        async with create_connected_server_and_client_session(server) as session:
            adapter = MCPToolAdapter(
                session=session,
                name="does_not_exist",
                description="",
                parameters={},
            )
            return await adapter.execute()

    result = asyncio.run(scenario())

    assert "unknown tool" in result

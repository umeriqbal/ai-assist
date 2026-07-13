import anyio
from mcp.server.stdio import stdio_server

from app.dependencies.services import get_knowledge_base_search_tool
from app.mcp.server import build_mcp_server
from app.tools.echo_tool import EchoTool


async def main() -> None:

    server = build_mcp_server(
        name="enterprise-ai-assistant",
        tools=[EchoTool(), get_knowledge_base_search_tool()],
    )

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    anyio.run(main)

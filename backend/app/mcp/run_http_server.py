import uvicorn

from app.core.config import settings
from app.dependencies.services import get_knowledge_base_search_tool
from app.mcp.http_server import build_http_app
from app.mcp.server import build_mcp_server
from app.tools.echo_tool import EchoTool


def main() -> None:

    server = build_mcp_server(
        name="enterprise-ai-assistant",
        tools=[EchoTool(), get_knowledge_base_search_tool()],
    )

    app = build_http_app(server)

    uvicorn.run(app, host=settings.mcp_server_host, port=settings.mcp_server_port)


if __name__ == "__main__":
    main()

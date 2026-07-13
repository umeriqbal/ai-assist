import asyncio
import socket
import threading
import time

import uvicorn

from app.mcp.client import connect_http_mcp_server, discover_tools
from app.mcp.http_server import build_http_app
from app.mcp.server import build_mcp_server
from app.tools.echo_tool import EchoTool

_HOST = "127.0.0.1"
_PORT = 8798


def _wait_for_port(host: str, port: int, timeout: float = 5.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.2):
                return
        except OSError:
            time.sleep(0.05)
    raise TimeoutError(f"Server on {host}:{port} did not start in time")


def test_tools_are_discoverable_and_executable_over_real_http():
    """
    Genuine integration test: a real Starlette/uvicorn server on a real
    port, a real HTTP client connecting to it. No mocks — the whole
    point of this test is proving the network transport actually works,
    not just that the tool logic works (already covered by the
    in-memory-harness tests in test_mcp_server.py / test_mcp_client.py).
    """

    server = build_mcp_server(name="test-http-server", tools=[EchoTool()])
    app = build_http_app(server)

    config = uvicorn.Config(app, host=_HOST, port=_PORT, log_level="error")
    uvicorn_server = uvicorn.Server(config)

    thread = threading.Thread(target=uvicorn_server.run, daemon=True)
    thread.start()

    try:
        _wait_for_port(_HOST, _PORT)

        async def scenario():
            async with connect_http_mcp_server(f"http://{_HOST}:{_PORT}/mcp") as session:
                tools = await discover_tools(session)
                result = await tools[0].execute(text="hello over real http")
                return tools, result

        tools, result = asyncio.run(scenario())

        assert len(tools) == 1
        assert tools[0].name == "echo"
        assert result == "hello over real http"
    finally:
        uvicorn_server.should_exit = True
        thread.join(timeout=5)

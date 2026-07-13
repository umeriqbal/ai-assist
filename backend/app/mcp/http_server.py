from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.types import Receive, Scope, Send


class _StreamableHTTPASGIApp:
    """
    Minimal ASGI adapter around a `StreamableHTTPSessionManager`.

    Written directly rather than imported from `mcp.server.fastmcp` —
    that module's equivalent is an internal of `FastMCP`, which this
    project deliberately doesn't use (see `server.py`).
    """

    def __init__(self, session_manager: StreamableHTTPSessionManager) -> None:
        self._session_manager = session_manager

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self._session_manager.handle_request(scope, receive, send)


def build_http_app(server: Server, path: str = "/mcp") -> Starlette:
    """
    Wrap an MCP `Server` in a Starlette ASGI app served over the
    streamable-HTTP transport — a genuinely network-addressable MCP
    server, unlike `run_server.py`'s stdio subprocess transport.
    """

    session_manager = StreamableHTTPSessionManager(app=server, stateless=True)

    return Starlette(
        routes=[Mount(path, app=_StreamableHTTPASGIApp(session_manager))],
        lifespan=lambda app: session_manager.run(),
    )

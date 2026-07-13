from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers.agent import router as agent_router
from app.api.routers.chat import router as chat_router
from app.api.routers.document import router as document_router
from app.api.routers.evaluation import router as evaluation_router
from app.api.routers.health import router as health_router
from app.api.routers.qa import router as qa_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.dependencies.llm import get_conversation_memory, get_openai_provider
from app.mcp.client import connect_http_mcp_server, discover_tools
from app.services.agent_service import AgentService


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Connect to the MCP HTTP server once, at startup, and keep the
    connection open for the app's lifetime — discovering its tools
    and building an `AgentService` from them. Requires the MCP HTTP
    server (`python -m app.mcp.run_http_server`) to already be running;
    there's no sensible fallback for "the tools this agent needs don't
    exist yet," so startup fails clearly if it isn't reachable.
    """

    async with connect_http_mcp_server(settings.mcp_server_url) as session:
        tools = await discover_tools(session)
        app.state.mcp_agent_service = AgentService(
            provider=get_openai_provider(),
            tools=tools,
            memory=get_conversation_memory(),
        )
        yield


def create_app() -> FastAPI:

    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=_lifespan,
    )

    app.include_router(
        health_router,
        tags=["Health"],
    )

    app.include_router(
        chat_router,
    )

    app.include_router(
        document_router,
    )

    app.include_router(
        qa_router,
    )

    app.include_router(
        evaluation_router,
    )

    app.include_router(
        agent_router,
    )

    return app
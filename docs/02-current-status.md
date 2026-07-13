# Current Project Status

> This document provides a snapshot of the project at the current point in time.
>
> Update this file at the end of every sprint.

---

# Project

Enterprise AI Assistant

---

# Overall Progress

| Area | Status |
|------|--------|
| Project Setup | ✅ Complete |
| Architecture | ✅ Complete |
| AI Platform | ✅ Complete |
| Enterprise RAG | ✅ Complete |
| AI Agents | ✅ Complete |
| MCP | ✅ Complete |
| Infrastructure | ⏳ Pending |
| Evaluation | ⏳ Pending |
| Capstone | ⏳ Pending |

---

# Current Module

**Module 8 – Production Infrastructure**

Status:

⏳ Not Started

---

# Current Sprint

Not yet defined.

Module 8 hasn't been broken into sprints yet — that scoping happens the same way every prior module's did, at the start of the module rather than in advance. Per the roadmap, Module 8's topics are: Docker, Docker Compose, PostgreSQL, pgvector, Redis, Terraform, AWS, CI/CD, Monitoring, Secrets Management.

---

# Last Completed Module

## Module 7 – Model Context Protocol (MCP)

Completed Features

- **Sprint 1 – MCP Server Foundations:** `mcp==1.28.1` + explicit `starlette==0.47.3` pin (installing `mcp` alone conflicts with `fastapi`'s pin, same class of issue as Sprint 5's `langgraph`); `app/mcp/server.py` (`build_mcp_server()`) — low-level MCP `Server` API, not `FastMCP`, since `Tool.parameters` already maps directly onto MCP's `inputSchema`; `app/mcp/run_server.py` — standalone stdio server exposing `EchoTool` and the real `KnowledgeBaseSearchTool`
- **Sprint 2 – MCP Client + Tool Discovery:** `MCPToolAdapter` (`app/mcp/client.py`) — mirror image of Sprint 1's adapter, wrapping a remote MCP tool as this project's own `Tool`; `discover_tools()` (zero hard-coded tool names); `connect_stdio_mcp_server()`
- **Sprint 3 – Remote Execution / Agent Integration:** MCP server upgraded to streamable-HTTP (`app/mcp/http_server.py`/`run_http_server.py`) — a genuinely network-addressable service, not just a subprocess pipe; `connect_http_mcp_server()`; `create_app()` gained its first `lifespan` — connects to the MCP HTTP server at startup, discovers its tools, builds an `AgentService` from them; `POST /agents/mcp-chat` — an agent using tools it never knew about at compile time, discovered over a real network boundary

Every sprint above was unit-tested and live-verified across genuine process boundaries — Sprint 1/2 over stdio (a real subprocess), Sprint 3 over real HTTP with the MCP server and the FastAPI app running as two independent processes, a forced remote tool call round-tripping correctly end to end.

Status

✅ Complete

---

# Previously Completed Module

## Module 6 – AI Agents

Completed Features

- **Sprint 1 – Agent Architecture:** `Tool` interface, `AgentService` (ReAct-style loop), `KnowledgeBaseSearchTool`, `POST /agents/chat`
- **Sprint 2 – Planning:** `Plan`/`PlanStep`, `LLMProvider.generate_structured()`, `Planner`, `PlanningService`, `POST /agents/plan`
- **Sprint 3 – Reflection:** `Critique`, `Reflector`, `ReflectionService`, `POST /agents/reflect`
- **Sprint 4 – Memory:** `ConversationMemory` + `InMemoryConversationMemory`, `AgentService.chat()` gained `conversation_id`
- **Sprint 5 – LangGraph + State Management:** `langgraph==0.6.11`; the Sprint 1 loop rebuilt as a LangGraph graph; `AgentGraphService`, `POST /agents/graph-chat`
- **Sprint 6 – Multi-Agent Collaboration:** `Supervisor` + `MultiAgentService` coordinating a Researcher/Writer pair, `POST /agents/collaborate`

Every sprint above was unit-tested and live-verified against the real OpenAI API.

Status

✅ Complete

---

# Current Architecture

```
HTTP Request

↓

Router

↓

Service

↓

Provider

↓

OpenAI SDK

↓

OpenAI Responses API
```

Beginning in Module 5, a new RAG layer will be introduced:

```
Router

↓

Service

↓

RAG Layer

↓

LangChain

↓

Provider

↓

OpenAI
```

LangChain will remain isolated within the RAG layer.

---

# Completed Endpoints

| Endpoint | Status |
|-----------|--------|
| GET / | ✅ |
| GET /live | ✅ |
| GET /ready | ✅ |
| GET /health | ✅ |
| GET /chat/health | ✅ |
| POST /chat | ✅ |
| POST /chat/stream | ✅ |
| POST /documents | ✅ |
| POST /documents/chunks | ✅ |
| POST /documents/embeddings | ✅ |
| POST /documents/index | ✅ |
| POST /documents/search | ✅ |
| POST /documents/upload | ✅ |
| POST /ask | ✅ |
| POST /evaluate/retrieval | ✅ |
| POST /evaluate/faithfulness | ✅ |
| POST /agents/chat | ✅ |
| POST /agents/plan | ✅ |
| POST /agents/reflect | ✅ |
| POST /agents/chat (now with conversation_id) | ✅ |
| POST /agents/graph-chat | ✅ |
| POST /agents/collaborate | ✅ |
| POST /agents/mcp-chat | ✅ |

---

# Current Folder Structure

```
backend/

app/

api/
core/
providers/
services/
dependencies/
rag/
schemas/
models/
database/
agents/
tools/
mcp/
```

`mcp/` (Module 7) — `server.py`/`run_server.py` (Sprint 1, stdio), `client.py` (Sprint 2, `MCPToolAdapter`/`discover_tools()`/`connect_stdio_mcp_server()`; Sprint 3 added `connect_http_mcp_server()`), `http_server.py`/`run_http_server.py` (Sprint 3, streamable-HTTP — the genuinely network-addressable server `POST /agents/mcp-chat` connects to). The MCP servers themselves are not FastAPI endpoints — separate processes a client connects to — so only `POST /agents/mcp-chat` (the FastAPI side of the integration) has an entry in the endpoints table below. Confined the same way `rag/` and `agents/` confine their respective frameworks — the low-level `mcp` SDK never leaks outside this folder.

`agents/` grew across every sprint of Module 6: `plan.py`/`planner.py` (Sprint 2), `critique.py`/`reflector.py` (Sprint 3), `memory.py`/`in_memory_conversation_memory.py` (Sprint 4), `agent_graph.py` (Sprint 5), `supervisor_decision.py`/`supervisor.py`/`multi_agent_graph.py` (Sprint 6) — holds the planning/reflection/memory/graph building blocks, the same way `rag/` holds RAG building blocks. LangGraph is confined to this layer, same isolation principle as LangChain and `rag/`. The services that orchestrate them for DI/router use (`AgentService`, `PlanningService`, `ReflectionService`, `AgentGraphService`, `MultiAgentService`) still live in `services/`, consistent with Decision 003.

---

# Current Technology Stack

Backend

- Python 3.12
- FastAPI
- Pydantic
- OpenAI SDK
- LangChain (confined to `app/rag/`)
- LangGraph (confined to `app/agents/`, same isolation principle as LangChain)
- MCP (`mcp==1.28.1`, confined to `app/mcp/`, same isolation principle)
- Structlog

Upcoming

- SQLAlchemy
- PostgreSQL
- pgvector

---

# Current Design Principles

The project follows these principles throughout the codebase.

- Layered Architecture
- SOLID
- Dependency Injection
- Provider Pattern
- Thin Routers
- Service Layer
- Async First
- Strong Typing
- Pydantic Validation
- One Responsibility Per Class

---

# Current Backlog

## High Priority

- Module 8 – Production Infrastructure (scoping not yet started)

---

## Medium Priority

- DOCX Loader
- HTML Loader
- Markdown Loader

---

## Future

- PostgreSQL
- pgvector
- Hybrid Search
- Reranking
- Production Infrastructure

---

# Known Technical Debt

At the current stage there are no significant architectural concerns.

Planned improvements include:

- Repository layer for persistence.
- Request-scoped logging.
- Unified exception handling (currently handled per-router, e.g. `document.py` catches `ValueError`).
- `InMemoryVectorStore` is process-local and non-persistent by design — will be replaced by a `PostgreSQL` + `pgvector` implementation behind the same `VectorStore` interface once the RAG pipeline is otherwise proven out.
- `InMemoryConversationMemory` (Module 6, Sprint 4) carries the identical caveat — process-local, non-persistent, lost on restart — behind the same `ConversationMemory` interface, ready to be replaced by Redis or PostgreSQL (both already listed as "Future" in the tech stack).
- `POST /agents/chat` and `POST /agents/graph-chat` (Module 6, Sprint 5) use two separate, unrelated state stores (`ConversationMemory` vs. LangGraph's `MemorySaver`). A `conversation_id` from one endpoint means nothing to the other — reusing one across both is a no-op, not an error, so nothing will surface this if it happens. Intentional (they're two independent implementations of the same capability, kept deliberately separate for comparison), but worth knowing before assuming they interoperate.
- LangGraph's `MemorySaver` checkpointer persists the *entire* graph state per turn, including intermediate tool-call round-trip messages — unlike `ConversationMemory`, which deliberately stores only the human-visible exchange. More faithful context, but an uncurated and unboundedly growing state; not reconciled between the two paths.
- `POST /agents/collaborate` (Module 6, Sprint 6) has no cross-call memory at all — each request is a fresh collaboration with no `conversation_id`. Intentional scope decision (Sprints 4–5 already covered that capability), not an oversight, but worth knowing before assuming feature parity with the other `/agents/*` endpoints.
- `FaithfulnessService` parses the LLM judge's verdict from prompt-instructed JSON text, not a guaranteed schema. Malformed responses are reported as `is_faithful: null` rather than silently misreported, but this is best-effort parsing, not a guaranteed contract. `LLMProvider.generate_structured()` (added in Module 6, Sprint 2) now provides exactly the robust mechanism this needed — retrofitting `FaithfulnessService` to use it is an optional, non-blocking cleanup, not yet done.
- DOCX/HTML/Markdown loaders are not implemented — only PDF and raw text ingestion currently work.
- `mcp==1.28.1` required an explicit `starlette==0.47.3` pin in `requirements.txt` to avoid a conflict with `fastapi==0.116.1` (`mcp`'s own dependency has no upper bound on `starlette`, and a fresh `pip install -r requirements.txt` could otherwise drift to an incompatible version over time). Same class of issue as Sprint 5's `langgraph`/`langchain-core` conflict, resolved the same way.
- The MCP server (`app/mcp/run_server.py` and `run_http_server.py` alike) runs as a separate process — it shares no state with the FastAPI app's `KnowledgeBaseSearchTool`/vector store; each process gets its own in-memory instance. Confirmed live in Sprint 3: a question requiring a document indexed via `POST /documents/index` correctly got "no results" through `POST /agents/mcp-chat`, because the MCP server process's vector store is empty — the remote call itself worked correctly, it just had nothing to find. Will matter once the MCP-exposed tool needs to reflect data indexed through the API; not addressed yet.
- `create_app()`'s `lifespan` (Module 7, Sprint 3) requires the MCP HTTP server to already be running and reachable at `settings.mcp_server_url` — if it isn't, FastAPI app startup fails outright rather than degrading gracefully. Intentional (there's no sensible fallback for "the tools this agent needs don't exist yet"), but it does mean two processes must be started in order: `run_http_server.py` first, then the FastAPI app.

These are intentional future enhancements rather than defects.

---

# Git Status

Latest Completed Milestone

Module 7 – Model Context Protocol (all 3 sprints)

Recommended Tag

```
v0.7.0
```

---

# Next Development Task

Module 8 – Production Infrastructure

Not yet broken into sprints/increments.

Goal (module-level, per the roadmap):

Deploy the platform to production — Docker, Docker Compose, PostgreSQL, pgvector, Redis, Terraform, AWS, CI/CD, Monitoring, Secrets Management. Module 7 (MCP) is fully complete: server foundations, client + tool discovery, and remote execution/agent integration, all built and live-verified across genuine process boundaries (stdio and real HTTP). The first step when this resumes is scoping Module 8 into sprints the same way every prior module was — starting with a concept walkthrough and a plan for Sprint 1, before any code changes.

---

# Success Criteria

Module 8 is ready to scope when:

- Module 7's full MCP integration is confirmed stable (it is — 107/107 tests passing, every sprint live-verified across a genuine process boundary, including Sprint 3's real two-process HTTP round trip).
- A decision is made on whether to first close out the Medium Priority backlog (DOCX/HTML/Markdown loaders) or move straight into infrastructure.

---

# Resume Point

If continuing this project in a new conversation:

1. Read `PROJECT_CONTEXT.md`
2. Read `00-bootcamp-index.md`
3. Read this document (`02-current-status.md`)
4. Continue with:

**Module 8 – Production Infrastructure → scope Sprint 1 (not yet defined)**, or address the remaining Medium Priority backlog (DOCX/HTML/Markdown loaders) first if preferred.
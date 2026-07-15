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
| Evaluation | ⏸️ Deferred |
| Capstone | 🚧 In Progress |

---

# Current Module

**Module 10 – Enterprise AI Assistant**

Status:

🚧 In Progress

Taken up out of the original roadmap order, at the user's direction — Module 8 (Production Infrastructure) remains not-yet-started, and Module 9 (Evaluation & Observability) was scoped then deliberately deferred (see Known Technical Debt below).

Completed Sprints

- **Sprint 1 – Frontend Foundations:** stack decision made first — standalone static frontend, plain HTML/CSS/JS, no framework (React/Vue/Svelte all considered, declined), served independently from the backend over CORS, consistent with this project's "understand before framework" thread. `CORSMiddleware` added to `create_app()` — the first client in this project ever served from a different origin than the backend; every prior client (curl, Swagger, another Python process) was same-origin, so nothing needed this before. `FRONTEND_URL` setting (explicit allowed origin, not `*`). `frontend/index.html`, `css/styles.css`, `js/api.js` (shared `fetch()` wrapper every later sprint reuses), `js/main.js` — calls `GET /health` on load and renders the result. Live-verified in a real headless Chromium browser via Playwright (no `chromium-cli` or project run-skill existed yet, so a driver script was written ad hoc): real CORS negotiation, zero console errors, screenshot confirmed correct rendering. Also surfaced a real operational dependency: the FastAPI app's `lifespan` (Module 7, Sprint 3) requires the MCP HTTP server running first — `run_http_server.py`, then the backend, then the frontend.
- **Sprint 2 – Enterprise Chat UI:** scoping decision made first — wire the chat page to `POST /chat` + `POST /chat/stream` (Module 4's `ChatService`/`StreamingService`, live token-by-token streaming) rather than `POST /agents/chat` (Module 6's `AgentService`, real `conversation_id` memory but no streaming variant yet) — chose streaming, accepted no cross-turn memory rather than expand scope with a backend change. `frontend/chat.html` + `js/chat.js` — user/assistant message bubbles, a send form that renders the user's message immediately and streams the assistant's reply in chunk by chunk. `js/api.js` gained `apiPostStream(path, body, onChunk)`, reading `response.body.getReader()` directly since a streamed `text/plain` body can't reuse the existing `response.json()`-based helper. Both pages gained a small top-bar nav (`Status`/`Chat`, plain `<a href>`, no router). Live-verified in a real headless browser: sent a message, watched the assistant bubble fill in as chunks arrived, zero real console errors, screenshot confirmed both pages render correctly. Also confirmed by the user running all three processes locally end to end, which surfaced two real environment gotchas along the way — a bare `uvicorn` command resolving to a global install instead of the venv's, and `python -m http.server` needing to be launched from inside `frontend/` specifically — both now documented in [07-development-guide.md](07-development-guide.md)'s Common Issues.
- **Sprint 3 – Knowledge Base UI:** scoping decision made first — wire to `POST /documents/upload` (multipart file upload) and `POST /documents/search` (semantic search), Module 5's two end-user-facing endpoints, rather than the pipeline-stage endpoints (`/documents`, `/chunks`, `/embeddings`, `/index`) meant for testing the RAG pipeline itself. `frontend/kb.html` + `js/kb.js` — one page, two panels (upload with a `.pdf`-restricted file picker and optional source name; search with a query input), so the index → search round trip is visible together. `js/api.js` gained `apiPostForm(path, formData)` — sends `FormData` with no manually-set `Content-Type` (the browser sets the multipart boundary itself), a third distinct request shape after `apiPost`'s JSON and `apiPostStream`'s streamed-read. Knowledge Base nav link added to all three pages. Live-verified in a real headless browser: uploaded a real (minimal, hand-crafted) PDF fixture, confirmed the indexing confirmation card, searched for its content, confirmed real search results with real similarity scores rendered as cards. Also confirmed, via a direct API call first, that a non-PDF upload correctly surfaces the backend's existing `"No loader registered"` error through the UI — the file input's `accept=".pdf"` plus a visible hint steer users away from hitting it.

Per the roadmap, Module 10's remaining topics are: Website Crawling, Agents UI, Evaluation Dashboard, Admin Interface — to be scoped sprint by sprint the same way every prior module was.

---

# Current Sprint

**Sprint 4 – Website Crawling**

Not yet scoped into increments.

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

**`frontend/`** (repo root, sibling to `backend/`, Module 10) has real content for the first time:

```
frontend/
index.html
chat.html
kb.html
css/
  styles.css
js/
  api.js
  main.js
  chat.js
  kb.js
```

Plain HTML/CSS/JS, no build tooling, no framework — served independently (Python's built-in `http.server`) and calling the backend over CORS. `js/api.js` is the shared `fetch()` wrapper every page reuses — `apiGet`/`apiPost` (Sprint 1), `apiPostStream` (Sprint 2, reading a streamed response body chunk by chunk instead of parsing JSON), and `apiPostForm` (Sprint 3, sending `FormData` with no manually-set `Content-Type` for file uploads). `chat.html`/`chat.js` (Sprint 2) wire to `POST /chat/stream` for a live chat interface; `kb.html`/`kb.js` (Sprint 3) wire to `POST /documents/upload` + `POST /documents/search` for document upload and semantic search. All three pages share a small top-bar nav.

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
- Anthropic SDK (`anthropic==0.116.0`) — `ClaudeProvider` implements `LLMProvider` alongside `OpenAIProvider`; built standalone (not tied to a module's sprint sequence) to prove the Provider Pattern generalizes to a second vendor. Not wired into any active service — `get_openai_provider()` remains what every `get_*_service()` actually uses
- Structlog

Frontend

- Plain HTML/CSS/JS (`frontend/`) — no framework, no build tooling. React/Vue/Svelte all considered and declined at the start of Module 10.
- Native ES modules (`<script type="module">`) for splitting JS into files without a bundler — standard browser JS, not a framework.

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

- Module 10, Sprint 4 – Website Crawling (scoping not yet started)
- Module 8 – Production Infrastructure (scoping not yet started, taken up out of order)

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
- Module 9 – Evaluation & Observability (deliberately deferred, see Known Technical Debt below — not a priority item, revisit only once there's real production traffic)

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
- **Module 9 (Evaluation & Observability) is deliberately deferred, not built.** Scoped to a concrete Sprint 1 plan (`CostTracker` as an injected recorder, a new `app/observability/` layer) and then explicitly not implemented: every capability in it — cost tracking, latency monitoring, model comparison, prompt versioning — only has real value against ongoing real traffic, or when something automated acts on the data. Neither exists yet. Building it now would be speculative infrastructure with a real recurring cost (pricing tables go stale) and nothing observing it. Revisit once there's real production traffic (likely post-Module 8) or provider selection becomes a genuine runtime decision. Full reasoning in [01-roadmap.md](docs/01-roadmap.md)'s Module 9 section.
- `ClaudeProvider` (`app/providers/claude_provider.py`) exists and is fully tested against the `LLMProvider` contract, but isn't wired into any active service — `get_openai_provider()` remains what `dependencies/services.py` actually uses everywhere. Built standalone to prove the Provider Pattern generalizes to a second vendor, and to keep a config-driven provider switch (`LLM_PROVIDER=openai|claude`) available as a cheap future option without committing to it now.
- Running Module 10's frontend against the live backend requires **three processes started in a specific order**: `app.mcp.run_http_server`, then the FastAPI app, then the `frontend/` static server (e.g. `python -m http.server 5500` from inside `frontend/`). No orchestration script exists yet to start all three together — a real operational rough edge, not addressed in Sprint 1.
- No `chromium-cli` or project run-skill existed for driving this app in a browser — Sprint 1's live verification used an ad hoc Playwright script instead. Worth generating a proper project run-skill (`/run-skill-generator`) before Module 10 has many more UI sprints to verify the same way repeatedly.
- The chat UI (Sprint 2) has no cross-turn memory — it's wired to `POST /chat/stream`, which is stateless per call, not `POST /agents/chat` (which has real `conversation_id` memory but no streaming variant). A user asking a follow-up question gets no context from their previous message. Intentional scope decision (streaming was prioritized over memory for this sprint), not an oversight — would require adding a streaming variant to `AgentService` to fix, which is backend work beyond a frontend sprint.
- The knowledge base UI (Sprint 3) only accepts PDF uploads — `POST /documents/upload` has no loader registered for `.txt`/`.docx`/`.html`/`.md` (a pre-existing gap from Module 5, not new to this sprint). The file picker's `accept=".pdf"` plus a visible hint steer users away from hitting this, and the backend's real error surfaces correctly through the UI if they do anyway. Resolving it means implementing the missing loaders (Module 5's Medium Priority backlog item), not a frontend change.

These are intentional future enhancements rather than defects.

---

# Git Status

Latest Completed Milestone

Module 10, Sprint 3 – Knowledge Base UI

Recommended Tag

```
v1.0.0-sprint3
```

---

# Next Development Task

Module 10, Sprint 4 – Website Crawling

Not yet broken into increments.

Goal (module-level, per the roadmap):

Combine everything into one application — Enterprise Chat, Knowledge Base, Website Crawling, PDF Search, Agents, Tool Calling, MCP, Evaluation Dashboard, Admin Interface. Taken up out of the original roadmap order at the user's direction (Module 8 remains not-yet-started; Module 9 was scoped then deliberately deferred). Sprint 1 (Frontend Foundations), Sprint 2 (Enterprise Chat UI), and Sprint 3 (Knowledge Base UI) are complete: CORS enabled, the static site skeleton built, a real streaming chat interface, and a document upload + semantic search UI, all connectivity proven in a real browser. The next step is scoping Sprint 4 the same way — a UI for indexing content crawled from websites (the one genuinely new backend capability remaining in this module, not yet built at all).

---

# Success Criteria

Module 10, Sprint 4 is ready to scope when:

- Sprint 3's knowledge base UI is confirmed stable (it is — 107/107 backend tests passing, unaffected by the frontend-only change; upload and search verified in a real headless browser via Playwright with a real PDF fixture, real search results with real similarity scores rendered, zero real console errors, screenshot-confirmed correct rendering).

---

# Resume Point

If continuing this project in a new conversation:

1. Read `PROJECT_CONTEXT.md`
2. Read `00-bootcamp-index.md`
3. Read this document (`02-current-status.md`)
4. Continue with:

**Module 10, Sprint 4 – Website Crawling → scope into increments (not yet defined)**, or address Module 8 / the remaining Medium Priority backlog (DOCX/HTML/Markdown loaders) first if preferred.
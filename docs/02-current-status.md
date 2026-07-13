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
| MCP | 🚧 In Progress |
| Infrastructure | ⏳ Pending |
| Evaluation | ⏳ Pending |
| Capstone | ⏳ Pending |

---

# Current Module

**Module 7 – Model Context Protocol (MCP)**

Status:

🚧 In Progress

Completed Sprints

- **Sprint 1 – MCP Server Foundations:** `mcp==1.28.1` added (required an explicit `starlette==0.47.3` pin alongside it — installing `mcp` alone pulls in a `starlette` that conflicts with `fastapi==0.116.1`'s pin, same class of issue as Sprint 5's `langgraph`/`langchain-core` conflict); `app/mcp/server.py` (`build_mcp_server()`) — uses the low-level MCP `Server` API rather than `FastMCP`, because `Tool.parameters` is already a hand-written JSON Schema and maps directly onto MCP's `inputSchema` with zero adaptation, whereas `FastMCP`'s decorator infers schemas from Python type hints and would fight that; unknown tool names return an error `TextContent` rather than crashing, mirroring `AgentService`'s convention; `app/mcp/run_server.py` — standalone stdio-transport server exposing `EchoTool` and the real `KnowledgeBaseSearchTool`; live-verified by spawning it as an actual subprocess and connecting a real MCP client over stdio (not just the in-memory test harness) — both tools discovered correctly, `EchoTool` executed correctly, `KnowledgeBaseSearchTool` correctly hit the real embedding/retrieval pipeline
- **Sprint 2 – MCP Client + Tool Discovery:** `MCPToolAdapter` (`app/mcp/client.py`) — adapts a remote MCP tool into this project's own `Tool` interface (mirror image of Sprint 1's server-side adapter); `discover_tools()` — lists a connected session's tools and wraps each, with zero hard-coded tool names anywhere in the client; `connect_stdio_mcp_server()` — async context manager spawning an MCP server subprocess and returning an initialized `ClientSession`; remote tool errors surface as plain text (`isError` respected, no exception), consistent with how `AgentService` already treats tool errors as ordinary output, not a crash; live-verified against the real Sprint 1 server: both `echo` and `search_knowledge_base` discovered and executed correctly, completing the full `Tool` → MCP server → subprocess boundary → MCP client → `Tool` round trip

Per the roadmap, Module 7's remaining topic is: Remote Execution / Agent Integration — to be scoped the same way Sprints 1–2 were, at the start of the sprint rather than in advance.

---

# Current Sprint

**Sprint 3 – Remote Execution / Agent Integration**

Not yet scoped into increments.

---

# Last Completed Module

## Module 6 – AI Agents

Completed Features

- **Sprint 1 – Agent Architecture:** `Tool` interface (`app/tools/tool.py`), `EchoTool` (contract-proving), `LLMProvider.chat_with_tools()` / `tool_result_messages()` (OpenAI Responses API tool-calling, kept behind the provider boundary), `AgentService` (ReAct-style loop with a max-iteration guard and graceful unknown-tool handling), `KnowledgeBaseSearchTool` (wraps `RetrievalService`), `POST /agents/chat`
- **Sprint 2 – Planning:** `Plan` / `PlanStep` (first use of `app/agents/`), `LLMProvider.generate_structured()` (OpenAI JSON-Schema–constrained structured output), `Planner`, `PlanningService` (plan → execute each step via `AgentService` → synthesize), `POST /agents/plan`
- **Sprint 3 – Reflection:** `Critique`, `Reflector` (reuses `generate_structured()`, no new provider capability needed), `ReflectionService` (generate → critique → revise, best-effort answer at the iteration cap rather than raising), `POST /agents/reflect`
- **Sprint 4 – Memory:** `ConversationMemory` interface + `InMemoryConversationMemory` (process-local, non-persistent by design, same trade-off as `InMemoryVectorStore`), `AgentService.chat()` extended with an optional `conversation_id`, `POST /agents/chat` now generates/returns/accepts one for real multi-turn conversations
- **Sprint 5 – LangGraph + State Management:** `langgraph==0.6.11` (first new dependency since Module 5, deliberately pinned below the 1.x line to avoid a `langchain-core` conflict with the existing pinned LangChain stack); the Sprint 1 loop rebuilt as a LangGraph graph (`call_model`/`call_tools` nodes calling the exact same `LLMProvider`/`Tool` methods `AgentService` uses — LangGraph replaces only the control flow), compiled with a `MemorySaver` checkpointer for state management; `AgentGraphService`; `POST /agents/graph-chat` alongside (not replacing) `POST /agents/chat`
- **Sprint 6 – Multi-Agent Collaboration:** `AgentService` gained an optional `system_prompt` (agents can now have a role, not just a tool set); `SupervisorDecision` + `Supervisor` (routes via `generate_structured()`, reusing Sprint 2's mechanism a third time); `MultiAgentState` + `supervisor`/`researcher`/`writer` graph nodes (`app/agents/multi_agent_graph.py`) — a Researcher (`AgentService` with the knowledge-base tool) and a Writer (`AgentService` with no tools) coordinated by the Supervisor, built on Sprint 5's graph pattern; `MultiAgentService`; `POST /agents/collaborate` — returns the final answer plus the full per-specialist transcript. Deliberately out of scope: cross-call memory (Sprints 4–5 already demonstrated it)

Every sprint above was unit-tested (with external calls faked) and additionally live-verified against the real OpenAI API — including, in Sprint 6, watching the Supervisor correctly sequence Researcher → Writer → finish with each specialist producing genuinely distinct output.

Status

✅ Complete

---

# Previously Completed Module

## Module 5 – Enterprise RAG

Completed Features

- **Sprint 1 – LangChain Foundations:** `DocumentFactory`, `DocumentService`, `POST /documents`
- **Sprint 2 – Chunking:** `RecursiveDocumentSplitter`, `ChunkingService`, `POST /documents/chunks`
- **Sprint 3 – Embeddings:** `OpenAIEmbeddingModel`, `EmbeddingService`, `POST /documents/embeddings`
- **Sprint 4 – Vector Storage:** `InMemoryVectorStore`, `VectorStoreService`, `POST /documents/index`, `POST /documents/search`
- **Sprint 5 – Retrieval:** metadata-filtered search (filtered before ranking), `RetrievalService`
- **Sprint 6 – Question Answering:** `PromptBuilder`, `QuestionAnsweringService`, `POST /ask` — verified to refuse out-of-context questions rather than hallucinate
- **Sprint 7 – Citations:** structured `Citation` objects (source, score, snippet) replacing the flat source list
- **Sprint 8 – Evaluation:** `EvaluationService` (recall/precision against labeled cases), `FaithfulnessService` (LLM-as-judge hallucination detection), `POST /evaluate/retrieval`, `POST /evaluate/faithfulness`
- **Out of sequence:** fixed the long-broken PDF loader and wired a real file-upload pipeline (`POST /documents/upload`), tested via a real HTTP multipart request and Swagger's file picker

Every increment above was unit-tested (with external calls faked) and additionally live-verified against the real OpenAI API. Still open, non-blocking: DOCX/HTML/Markdown loaders (Medium Priority backlog, never built).

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

`mcp/` (Module 7) — `server.py`/`run_server.py` (Sprint 1) and `client.py` (Sprint 2, `MCPToolAdapter`/`discover_tools()`/`connect_stdio_mcp_server()`). Not a FastAPI endpoint: an MCP server is a separate process a client spawns/connects to, so it has no entry in the endpoints table below. Confined the same way `rag/` and `agents/` confine their respective frameworks — the low-level `mcp` SDK never leaks outside this folder.

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

- Module 7, Sprint 3 – Remote Execution / Agent Integration (scoping not yet started)

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
- The MCP server (`app/mcp/run_server.py`) runs as a separate process over stdio — it currently shares no state with the FastAPI app's `KnowledgeBaseSearchTool`/vector store; each process gets its own in-memory instance. Fine for the current foundational sprint; will matter once the MCP-exposed tool needs to reflect data indexed through the API.

These are intentional future enhancements rather than defects.

---

# Git Status

Latest Completed Milestone

Module 7, Sprint 2 – MCP Client + Tool Discovery

Recommended Tag

```
v0.7.0-sprint2
```

---

# Next Development Task

Module 7, Sprint 3 – Remote Execution / Agent Integration

Not yet broken into increments.

Goal (module-level, per the roadmap):

Build and consume MCP servers, covering the MCP specification, an MCP server, an MCP client, tool discovery, and remote execution. Sprints 1–2 are complete — our own tools are exposed over real MCP (Sprint 1), and a client can discover and execute remote MCP tools with zero hard-coded names (Sprint 2), both live-verified across a genuine subprocess boundary. The next step is scoping Sprint 3 the same way — wiring MCP-discovered tools into a running agent, and (per the roadmap's "Remote Execution" topic) likely upgrading from stdio to a genuinely networked transport.

---

# Success Criteria

Module 7, Sprint 3 is ready to scope when:

- Sprint 2's MCP client is confirmed stable (it is — 106/106 tests passing, live-verified against the real Sprint 1 server with zero hard-coded tool names in the client).

---

# Resume Point

If continuing this project in a new conversation:

1. Read `PROJECT_CONTEXT.md`
2. Read `00-bootcamp-index.md`
3. Read this document (`02-current-status.md`)
4. Continue with:

**Module 7, Sprint 3 – Remote Execution / Agent Integration → scope into increments (not yet defined)**, or address the remaining Medium Priority backlog (DOCX/HTML/Markdown loaders) first if preferred.
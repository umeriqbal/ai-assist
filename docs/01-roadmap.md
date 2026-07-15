# AI Engineer Bootcamp Roadmap

> Complete roadmap for the Enterprise AI Assistant project.

---

# Overview

The objective of this bootcamp is to become a production-ready AI Engineer by building a real Enterprise AI Assistant from scratch.

The project is intentionally cumulative. Every module builds upon the previous one until a complete enterprise-grade system is produced.

---

# Module 1 — LLM Fundamentals

**Status:** ✅ Complete

## Objectives

Understand how modern LLMs work.

### Topics

- Tokens
- Tokenization
- Context Windows
- Prompt Structure
- System/User/Assistant Roles
- Temperature
- Hallucinations
- API Costs
- Responses API
- Streaming Concepts

### Outcome

A solid understanding of how Large Language Models work internally and how they are consumed through APIs.

---

# Module 2 — Prompt Engineering

**Status:** ✅ Complete

## Objectives

Learn how to build reliable applications using prompts.

### Topics

- Prompt Templates
- Prompt Chaining
- Structured Outputs
- JSON Responses
- Pydantic Validation
- Error Handling
- FastAPI Integration

### Outcome

Built a Prompt Playground capable of generating structured AI responses.

---

# Module 3 — Semantic Search

**Status:** ✅ Complete

## Objectives

Understand semantic search from first principles.

### Topics

- Embeddings
- Vector Mathematics
- Cosine Similarity
- Chunking
- Context Management
- Search Ranking
- In-memory Vector Store

### Outcome

Built a complete semantic search engine without relying on external frameworks.

---

# Module 4 — Enterprise AI Platform

**Status:** ✅ Complete

## Objectives

Build a production-ready backend architecture.

### Topics

- Layered Architecture
- FastAPI Application Factory
- Configuration Management
- Dependency Injection
- Provider Pattern
- Service Layer
- Structured Logging
- Health Endpoints
- Chat API
- Streaming API
- OpenAI Provider

### Outcome

Created a reusable enterprise AI platform that will host all future capabilities.

---

# Module 5 — Enterprise RAG

**Status:** ✅ Complete

## Objectives

Build an enterprise Retrieval Augmented Generation platform.

### Sprint 1

LangChain Foundations

- LangChain Documents
- Document Metadata
- Document Service

---

### Sprint 2

Chunking

- RecursiveCharacterTextSplitter
- Chunk Strategies
- Metadata Preservation

---

### Sprint 3

Embeddings

- OpenAI Embeddings
- Embedding Service
- Batch Processing
- Cost Considerations

---

### Sprint 4

Vector Storage

Initially:

- In-memory

Later:

- PostgreSQL
- pgvector

---

### Sprint 5

Retrieval

- Similarity Search
- Top-K Retrieval
- Metadata Filtering
- Retrieval Pipeline

---

### Sprint 6

Question Answering

- Prompt Construction
- Context Injection
- Source Selection
- Grounded Answers

---

### Sprint 7

Citations

- Source Attribution
- Page Numbers
- Confidence

---

### Sprint 8

Evaluation

- Recall
- Precision
- Faithfulness
- Hallucination Detection

### Outcome

A complete enterprise document question-answering system.

---

# Module 6 — AI Agents

**Status:** ✅ Complete

## Objectives

Build production-quality AI agents.

### Sprint 1

Agent Architecture (foundations)

- `Tool` abstraction
- Provider tool-calling support
- Agent loop (ReAct-style)
- `POST /agents/chat`

**Status:** ✅ Complete

---

### Sprint 2

Planning

- `Plan` / `PlanStep` models
- Provider structured-output support
- `Planner`
- `PlanningService`
- `POST /agents/plan`

**Status:** ✅ Complete

---

### Sprint 3

Reflection

- `Critique` model
- `Reflector`
- `ReflectionService`
- `POST /agents/reflect`

**Status:** ✅ Complete

---

### Sprint 4

Memory

- `ConversationMemory` interface / `InMemoryConversationMemory`
- `AgentService.chat()` extended with `conversation_id`
- `POST /agents/chat` returns and accepts `conversation_id`

**Status:** ✅ Complete

---

### Sprint 5

LangGraph + State Management

- `AgentGraphState` + graph nodes (`call_model`, `call_tools`) rebuilding the Sprint 1 loop
- `MemorySaver` checkpointer for state management (replaces `ConversationMemory` for this path)
- `AgentGraphService`
- `POST /agents/graph-chat`

**Status:** ✅ Complete

---

### Sprint 6

Multi-Agent Collaboration

- `SupervisorDecision` model
- `Supervisor` (routes via `generate_structured()`)
- `MultiAgentState` + `supervisor`/`researcher`/`writer` graph nodes
- `MultiAgentService`
- `POST /agents/collaborate`

**Status:** ✅ Complete

### Outcome

A modular multi-agent system.

---

# Module 7 — Model Context Protocol (MCP)

**Status:** ✅ Complete

## Objectives

Build and consume MCP servers.

### Sprint 1

MCP Server Foundations

- `app/mcp/server.py` — `build_mcp_server()`, exposing existing `Tool` instances via the low-level MCP `Server` API (`Tool.parameters` maps directly onto `inputSchema`, no adaptation needed)
- `app/mcp/run_server.py` — standalone stdio-transport server, real tools (`EchoTool`, `KnowledgeBaseSearchTool`)

**Status:** ✅ Complete

---

### Sprint 2

MCP Client + Tool Discovery

- `app/mcp/client.py` — `MCPToolAdapter` (remote MCP tool → this project's `Tool` interface), `discover_tools()`, `connect_stdio_mcp_server()`
- Live-verified against the real Sprint 1 server: tools discovered with zero hard-coded names, executed correctly

**Status:** ✅ Complete

---

### Sprint 3

Remote Execution / Agent Integration

- `app/mcp/http_server.py` + `app/mcp/run_http_server.py` — MCP server over streamable-HTTP, a genuinely network-addressable service (not just a subprocess pipe like Sprints 1–2's stdio transport)
- `connect_http_mcp_server()` added to `app/mcp/client.py`
- `create_app()` gains a `lifespan` — connects to the MCP HTTP server at startup, discovers its tools, builds an `AgentService` from them
- `POST /agents/mcp-chat` — an agent using tools it never knew about at compile time, discovered over a real network boundary
- Live-verified with both servers running as separate real processes: a forced remote tool call round-tripped correctly end to end

**Status:** ✅ Complete

### Outcome

Enterprise-ready MCP integration.

---

# Module 8 — Production Infrastructure

**Status:** ⏳ Planned

## Objectives

Deploy the platform to production.

### Topics

- Docker
- Docker Compose
- PostgreSQL
- pgvector
- Redis
- Terraform
- AWS
- CI/CD
- Monitoring
- Secrets Management

### Outcome

Cloud-hosted production deployment.

---

# Module 9 — Evaluation & Observability

**Status:** ⏸️ Deferred — deliberately not building this yet

## Objectives

Measure AI system quality.

### Topics

- Offline Evaluation
- Online Evaluation
- Cost Tracking
- Latency Monitoring
- Token Usage
- Prompt Versioning
- Model Comparison

### Outcome

A measurable AI platform with production observability.

### Why deferred

Scoped down to a concrete Sprint 1 plan (`CostTracker` as an injected recorder, `app/observability/` as a new layer), then deliberately not built. Every capability in this module — cost tracking, latency monitoring, model comparison, prompt versioning — only has real value against *ongoing real traffic*, or when something *automated acts* on the data (e.g. routing requests to whichever provider is cheaper). Neither exists yet: this app has no production traffic, and provider selection is still a hard-coded constructor call, not a runtime decision anything could route against. Building the tracking apparatus now would be speculative infrastructure with a real, recurring cost (pricing tables alone go stale) and no offsetting benefit yet.

A single-prompt "compare OpenAI vs. Claude" endpoint was considered as a smaller alternative and rejected for the same reason: a comparison result that doesn't change what the system does next has no lasting effect — you'd look at it once, then nothing.

**Revisit when:** the app has real production traffic worth watching (likely after Module 8 deployment), or provider selection becomes a genuine runtime decision rather than a hard-coded one. If revisited, the leaner starting point is making the provider a config choice (`LLM_PROVIDER=openai|claude` deciding which `get_*_provider()` DI wiring uses) — `ClaudeProvider` already exists (built standalone, outside any module's sprint sequence, to prove the Provider Pattern generalizes) but isn't wired into any active service, precisely so that door stays open without committing to it now.

---

# Module 10 — Enterprise AI Assistant

**Status:** 🚧 Current

## Objectives

Combine everything into one application.

### Features

- Enterprise Chat
- Knowledge Base
- Website Crawling
- PDF Search
- Agents
- Tool Calling
- MCP
- Evaluation Dashboard
- Admin Interface

### Stack decision

Standalone static frontend — plain HTML/CSS/JS, no build tooling, no framework (React/Vue/Svelte all considered and declined), served independently from the backend and calling it over CORS. Consistent with this project's running theme of understanding a layer by hand before reaching for a framework (Module 3's semantic search, Module 6's hand-built ReAct loop before LangGraph).

### Sprint 1 — Frontend Foundations

- `CORSMiddleware` added to `create_app()` — the first request in this project to ever need permission to be called from a different origin; every prior client (curl, Swagger, another Python process) was same-origin
- `FRONTEND_URL` setting, explicit allowed origin (not `*`)
- `frontend/index.html`, `css/styles.css`, `js/api.js` (shared `fetch()` wrapper reused by every later sprint), `js/main.js` — calls `GET /health` on load and renders the result
- Live-verified in a real headless Chromium browser (Playwright, since no `chromium-cli`/project run-skill existed yet) — real fetch, real CORS negotiation, zero console errors, screenshot confirmed correct rendering

**Status:** ✅ Complete

### Sprint 2 — Enterprise Chat UI

- Scoping decision: wire the chat page to `POST /chat` + `POST /chat/stream` (Module 4's `ChatService`/`StreamingService`) for live token-by-token streaming, rather than `POST /agents/chat` (Module 6's `AgentService`, which has real `conversation_id` memory but no streaming variant yet) — chose streaming over cross-turn memory rather than expand scope with a backend change
- `frontend/chat.html` + `js/chat.js` — a new page (one page per feature, not a component tree), user/assistant message bubbles, a send form wired to the streaming endpoint
- `js/api.js` gained `apiPostStream()` — reads the response body as a stream (`getReader()`), since JSON parsing doesn't apply to a streamed `text/plain` body
- Small top-bar nav added to both pages (`Status` / `Chat`), plain `<a href>`, no router
- Live-verified in a real headless browser — sent a message, watched the reply stream in, zero real console errors, screenshot confirmed both pages render correctly

**Status:** ✅ Complete

### Sprint 3 — Knowledge Base UI

- Scoping decision: wire the page to `POST /documents/upload` (multipart file upload) and `POST /documents/search` (semantic search) — Module 5's end-user-facing endpoints — rather than the pipeline-stage endpoints (`/documents`, `/chunks`, `/embeddings`, `/index`) meant for testing the RAG pipeline itself
- `frontend/kb.html` + `js/kb.js` — one page, two panels: upload (file picker restricted to `.pdf`, optional source name) and search (query input), so the index → search round trip is visible together
- `js/api.js` gained `apiPostForm()` — sends `FormData` with no manually-set `Content-Type`, a third distinct request shape after JSON (`apiPost`) and streamed-read (`apiPostStream`)
- Knowledge Base nav link added to all three pages
- Live-verified in a real headless browser: uploaded a real (minimal, hand-crafted) PDF fixture, confirmed the indexing confirmation, searched for its content, confirmed real search results with real similarity scores rendered as cards. Also confirmed via a direct API call that a non-PDF upload correctly surfaces the backend's existing error through the UI

**Status:** ✅ Complete

### Outcome

A production-quality Enterprise AI Assistant suitable for portfolio demonstrations and real-world deployment.

---

# Progress Summary

| Module | Name | Status |
|---------|------|--------|
| 1 | LLM Fundamentals | ✅ Complete |
| 2 | Prompt Engineering | ✅ Complete |
| 3 | Semantic Search | ✅ Complete |
| 4 | Enterprise AI Platform | ✅ Complete |
| 5 | Enterprise RAG | ✅ Complete |
| 6 | AI Agents | ✅ Complete |
| 7 | Model Context Protocol | ✅ Complete |
| 8 | Production Infrastructure | ⏳ Planned |
| 9 | Evaluation & Observability | ⏸️ Deferred |
| 10 | Enterprise AI Assistant | 🚧 Current |

---

# Current Focus

**Module 10 – Enterprise AI Assistant**

Current Sprint:

**Sprint 4 – Website Crawling** *(not yet scoped)*

Last Completed Sprint:

**Sprint 3 – Knowledge Base UI** — `frontend/kb.html` + `js/kb.js` wired to `POST /documents/upload` and `POST /documents/search`. `js/api.js` gained `apiPostForm()`. Live-verified in a real headless browser — uploaded a real PDF, confirmed indexing, searched for its content, confirmed real search results rendered as cards.

Next milestone:

**Scope Sprint 4 (Website Crawling) into increments before writing any code.**

Module 8 (Production Infrastructure) and Module 9 (deferred — see its own section above) remain open, taken up out of the original order at the user's direction.
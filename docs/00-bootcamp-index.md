# Enterprise AI Assistant
# AI Engineer Bootcamp

> Master index for the entire project.

This document is the starting point for both developers and future ChatGPT sessions.

---

# Project

Enterprise AI Assistant

Purpose:

Build a production-quality AI platform while learning modern AI Engineering through hands-on development.

This project follows real software engineering practices including:

- Layered Architecture
- SOLID Principles
- Dependency Injection
- Provider Pattern
- Service Layer
- Production Logging
- Testing
- Documentation
- Git Workflow

---

# Current Status

| Item | Value |
|------|-------|
| Current Module | Module 10 – Enterprise AI Assistant (taken up out of order) |
| Current Sprint | Sprint 4 – Website Crawling (not yet scoped) |
| Current Increment | Not yet defined |
| Status | Module 7 (MCP) Complete — all 3 sprints. Module 8 not yet started; Module 9 scoped then deliberately deferred (see below). Module 10, Sprint 1 (Frontend Foundations), Sprint 2 (Enterprise Chat UI), and Sprint 3 (Knowledge Base UI) complete — 107/107 backend tests passing, all three pages live-verified in a real headless browser |

---

# Project Goals

The completed application will include:

- Enterprise Chat
- Retrieval Augmented Generation (RAG)
- PDF Knowledge Base
- Website Crawling
- Multi-Agent Workflows
- Model Context Protocol (MCP)
- Tool Calling
- PostgreSQL + pgvector
- Evaluation Framework
- AWS Deployment
- Production Monitoring

---

# Documentation Index

## Project

| File | Description |
|------|-------------|
| PROJECT_CONTEXT.md | Complete project context for continuing development |
| 01-roadmap.md | Full bootcamp roadmap |
| 02-current-status.md | Current progress snapshot |
| 03-architecture.md | System architecture |
| 04-folder-structure.md | Official project structure |
| 05-design-decisions.md | Architecture decisions |
| 06-tech-stack.md | Technology stack |
| 07-development-guide.md | Development setup |
| 08-learning-notes.md | AI Engineering notes |
| 09-interview-notes.md | Interview preparation |
| 10-changelog.md | Feature history |

---

## Module Documentation

| Module | Status |
|---------|--------|
| module-01.md | Complete |
| module-02.md | Complete |
| module-03.md | Complete |
| module-04.md | Complete |
| module-05.md | Complete |
| module-06.md | Complete |
| module-07.md | Complete |
| module-08.md | Pending (taken up out of order) |
| module-09.md | Deferred |
| module-10.md | Current |

---

# Completed Modules

## Module 1

LLM Fundamentals

Completed Topics

- Tokens
- Context Windows
- Hallucinations
- Prompt Structure
- Roles
- Temperature
- Cost

Status

Complete

---

## Module 2

Prompt Engineering

Completed Topics

- Structured Outputs
- JSON Responses
- Validation
- Prompt Templates
- FastAPI Integration
- OpenAI Responses API

Status

Complete

---

## Module 3

Semantic Search

Completed Topics

- Embeddings
- Cosine Similarity
- Chunking
- Vector Search
- Search Ranking
- In-memory Search Engine

Status

Complete

---

## Module 4

Enterprise AI Platform

Completed Topics

- Layered Architecture
- Configuration Management
- Application Factory
- Structured Logging
- Health Endpoints
- Dependency Injection
- Provider Pattern
- Service Layer
- Chat API
- Streaming Support

Status

Complete

---

## Module 5

Enterprise RAG

Completed Topics

- LangChain Documents
- Text Splitters
- Embeddings
- Vector Stores
- Retrieval (with metadata filtering)
- Question Answering (grounded, verified against hallucination)
- Source Citations
- Evaluation (recall/precision, faithfulness/hallucination detection)

Also fixed out of sequence: the PDF upload pipeline (loader was broken since before Module 5 began), so real files can be ingested, not just raw text.

Status

Complete

---

## Module 6

AI Agents

Completed Sprints

- **Sprint 1 – Agent Architecture:** `Tool` interface, `LLMProvider.chat_with_tools()` / `tool_result_messages()` (OpenAI tool-calling kept behind the provider boundary), `AgentService` (ReAct loop with iteration cap and graceful unknown-tool handling), `KnowledgeBaseSearchTool` (wraps `RetrievalService`), `POST /agents/chat`
- **Sprint 2 – Planning:** `app/agents/` layer created; `Plan`/`PlanStep`, `LLMProvider.generate_structured()` (OpenAI structured output), `Planner`, `PlanningService` (executes a plan step by step via `AgentService`, then synthesizes an answer), `POST /agents/plan`
- **Sprint 3 – Reflection:** `Critique`, `Reflector` (reuses `generate_structured()`, no new provider work needed), `ReflectionService` (generate → critique → revise loop, best-effort answer on hitting the iteration cap rather than raising), `POST /agents/reflect`
- **Sprint 4 – Memory:** `ConversationMemory` interface + `InMemoryConversationMemory` (process-local, non-persistent by design, same trade-off as `InMemoryVectorStore`), `AgentService.chat()` extended with an optional `conversation_id`, `POST /agents/chat` now generates/returns/accepts a `conversation_id` for real multi-turn conversations
- **Sprint 5 – LangGraph + State Management:** `langgraph==0.6.11` (first new dependency since Module 5); the Sprint 1 loop rebuilt as a LangGraph graph (`call_model`/`call_tools` nodes calling the same `LLMProvider`/`Tool` methods `AgentService` uses — LangGraph replaces only the loop's control flow), compiled with a `MemorySaver` checkpointer for state management; `AgentGraphService`; `POST /agents/graph-chat` alongside (not replacing) `POST /agents/chat`
- **Sprint 6 – Multi-Agent Collaboration:** `AgentService` gained an optional `system_prompt` (an agent can now have a role); `Supervisor` (routes via `generate_structured()`, reused a third time) coordinating a Researcher and a Writer specialist — both ordinary `AgentService` instances, differently configured — through a LangGraph graph built on Sprint 5's pattern; `MultiAgentService`; `POST /agents/collaborate`

Every sprint above unit-tested and live-verified against the real OpenAI API — Sprint 6's included watching the Supervisor correctly sequence Researcher → Writer → finish with two genuinely distinct specialist outputs.

Status

Complete

---

## Module 7

Model Context Protocol (MCP)

Completed Sprints

- **Sprint 1 – MCP Server Foundations:** `mcp==1.28.1` + an explicit `starlette==0.47.3` pin (same class of ecosystem conflict as Sprint 5's `langgraph`, resolved the same way); `app/mcp/` layer created (new top-level folder, reviewed before adding); `build_mcp_server()` — low-level MCP `Server` API, chosen over `FastMCP` because `Tool.parameters` already maps directly onto MCP's `inputSchema`, validated with a smoke test first; `run_server.py` — standalone stdio server exposing `EchoTool` and the real `KnowledgeBaseSearchTool`
- **Sprint 2 – MCP Client + Tool Discovery:** `MCPToolAdapter` (`app/mcp/client.py`) — the mirror image of Sprint 1's server-side adapter, wrapping a remote MCP tool as this project's own `Tool`; `discover_tools()` — zero hard-coded tool names anywhere in the client; `connect_stdio_mcp_server()` — spawns an MCP server subprocess and returns an initialized session
- **Sprint 3 – Remote Execution / Agent Integration:** MCP server upgraded to streamable-HTTP (`http_server.py`/`run_http_server.py`) — a genuinely network-addressable service, not a subprocess pipe; `connect_http_mcp_server()`; `create_app()` gained its first `lifespan` (connects to the MCP HTTP server at startup, discovers tools, builds an `AgentService`); `POST /agents/mcp-chat`

Live-verified across genuine process boundaries every sprint: stdio subprocess (Sprints 1–2), and real HTTP between two independently-running processes (Sprint 3) — a forced remote tool call round-tripped correctly end to end.

Status

Complete

---

## Module 10 (In Progress — taken up out of the original roadmap order)

Enterprise AI Assistant

Taken up next at the user's direction, ahead of Module 8 (Production Infrastructure, not yet started) and Module 9 (Evaluation & Observability, scoped then deliberately deferred — see [01-roadmap.md](docs/01-roadmap.md)).

Completed Sprints

- **Sprint 1 – Frontend Foundations:** stack decision first — standalone static frontend, plain HTML/CSS/JS, no framework (React/Vue/Svelte considered, declined), consistent with this project's "understand before framework" thread; `CORSMiddleware` added to `create_app()` — the first client in this project ever served from a different origin than the backend; `FRONTEND_URL` setting (explicit allowed origin, not `*`); `frontend/index.html`/`css/styles.css`/`js/api.js` (shared `fetch()` wrapper)/`js/main.js` — calls `GET /health` on load and renders the result
- **Sprint 2 – Enterprise Chat UI:** scoping decision first — wired to `POST /chat` + `POST /chat/stream` (live token-by-token streaming) rather than `POST /agents/chat` (real `conversation_id` memory, no streaming variant yet); `frontend/chat.html`/`js/chat.js` — message bubbles, a send form streaming the assistant's reply in chunk by chunk; `js/api.js` gained `apiPostStream()`; both pages gained a small top-bar nav
- **Sprint 3 – Knowledge Base UI:** scoping decision first — wired to `POST /documents/upload` + `POST /documents/search` (Module 5's end-user-facing endpoints) rather than the pipeline-stage endpoints; `frontend/kb.html`/`js/kb.js` — an upload panel (`.pdf`-restricted) and a search panel on one page; `js/api.js` gained `apiPostForm()` for `FormData` uploads; Knowledge Base nav link added to all three pages

Live-verified in a real headless Chromium browser via an ad hoc Playwright driver script (`chromium-cli` and a project run-skill both didn't exist yet): real CORS negotiation, zero console errors, screenshot confirmed correct rendering. Also surfaced a real operational dependency — three processes must start in order (`app.mcp.run_http_server`, then the backend, then the frontend server). Sprint 2 re-verified the same way: a sent message streamed a real assistant reply into the page. Sprint 3 re-verified with a real, hand-crafted PDF fixture (no PDF-generation dependency existed yet, so one was built the same way the backend's own test suite does): uploaded, indexed, then found again via search with a real similarity score.

Not yet scoped: Sprint 4 (Website Crawling) onward.

Status

🚧 In Progress

---

# Architecture

The project follows a layered architecture.

```
HTTP

↓

Routers

↓

Services

↓

Providers

↓

External Services
```

LangChain exists only inside the RAG layer.

Routers never communicate directly with external SDKs.

---

# Coding Standards

- Async first
- SOLID principles
- Strong typing
- Thin routers
- Service layer
- Provider abstraction
- Dependency Injection
- Pydantic validation
- Complete file replacements
- One responsibility per class
- Git commit after every increment

---

# Git Workflow

Every completed increment follows:

```
Implement

↓

Test

↓

Review

↓

Update Docs

↓

Commit

↓

Push
```

---

# Bootcamp Philosophy

This bootcamp focuses on building production-quality AI systems.

Libraries are used where appropriate.

Architecture is designed and owned by us.

The goal is to understand AI engineering patterns rather than becoming dependent on any single framework.

---

# Current Milestone

Module 10 – Enterprise AI Assistant (taken up out of the original roadmap order, at the user's direction)

Sprint 1 (Frontend Foundations), Sprint 2 (Enterprise Chat UI), and Sprint 3 (Knowledge Base UI) complete. Next step: a concept walkthrough and concrete increment plan for Sprint 4 (Website Crawling) — the one genuinely new backend capability remaining in this module, not yet built at all.

---

# Next Milestones

- Enterprise AI Assistant (Sprints 4+ — Website Crawling, Agents UI, Evaluation Dashboard, Admin Interface)
- Production Infrastructure (Docker, PostgreSQL, pgvector, Terraform, AWS, CI/CD) — not yet started, picked up after Module 10 or sooner if priorities change

**Evaluation & Observability (Module 9) — deliberately deferred, not on the near-term path.** Scoped to a concrete Sprint 1 plan, then explicitly not built: cost tracking, latency monitoring, model comparison, and prompt versioning only have real value against ongoing real traffic or an automated decision acting on the data — neither exists yet. A standalone `ClaudeProvider` was built alongside this discussion (proving the Provider Pattern generalizes) but isn't wired into any service. Revisit once there's real production traffic (likely post-Module 8) or provider selection becomes a genuine runtime decision.

Also still open, non-blocking: DOCX/HTML/Markdown loaders (Medium Priority backlog carried over from Module 5).

---

# How to Continue This Project

When starting a new ChatGPT conversation:

1. Read `PROJECT_CONTEXT.md`
2. Read `00-bootcamp-index.md`
3. Read `02-current-status.md`
4. Continue from the current module and sprint

No previous conversation should be required to continue development.
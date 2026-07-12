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
| AI Agents | 🚧 In Progress |
| MCP | ⏳ Pending |
| Infrastructure | ⏳ Pending |
| Evaluation | ⏳ Pending |
| Capstone | ⏳ Pending |

---

# Current Module

**Module 6 – AI Agents**

Status:

🚧 In Progress

Completed Sprints

- **Sprint 1 – Agent Architecture:** `Tool` interface (`app/tools/tool.py`), `EchoTool` (contract-proving), `LLMProvider.chat_with_tools()` / `tool_result_messages()` (OpenAI Responses API tool-calling, kept behind the provider boundary), `AgentService` (ReAct-style loop with a max-iteration guard and graceful unknown-tool handling), `KnowledgeBaseSearchTool` (wraps `RetrievalService`), `POST /agents/chat` — live-verified both without a tool (direct answer) and with one (correctly retrieved and grounded an answer in a freshly indexed document)
- **Sprint 2 – Planning:** `Plan` / `PlanStep` (`app/agents/plan.py`, first use of the `app/agents/` layer) — strict-schema Pydantic models; `LLMProvider.generate_structured()` (new) — OpenAI Responses API JSON-Schema–constrained structured output, a more robust alternative to `FaithfulnessService`'s prompt-instructed JSON parsing; `Planner` (`app/agents/planner.py`) — turns a goal into an ordered `Plan`, filling `goal` in from the caller rather than trusting the model to echo it back; `PlanningService` (new) — runs the plan step by step through `AgentService`, feeding each step the prior steps' results, then synthesizes one final answer; `POST /agents/plan` — live-verified against a real indexed policy document: the plan correctly decomposed the goal, each step retrieved/reused the right fact, and the final synthesized answer was accurate
- **Sprint 3 – Reflection:** `Critique` (`app/agents/critique.py`) — `is_satisfactory`/`feedback` strict-schema model; `Reflector` (`app/agents/reflector.py`) — critiques a candidate answer via `generate_structured()`, no new provider capability needed (pure reuse of Sprint 2's mechanism); `ReflectionService` (new) — generate → critique → revise loop built on `AgentService`, bounded by `max_iterations` but — unlike `AgentService`'s tool loop — returns a best-effort answer on hitting the cap instead of raising; `POST /agents/reflect` — returns the final answer plus every draft and its critique; live-verified against the real OpenAI API (both a general-knowledge question and a strict-format request were judged satisfactory on the first draft — the revision branch itself is deterministically covered by unit tests)

Per the roadmap, Module 6's remaining topics are: Memory, Multi-Agent Collaboration, LangGraph, State Management — each to be scoped into its own sprint the same way Sprints 1–3 were, at the start of the sprint rather than in advance.

---

# Current Sprint

**Sprint 4 – Memory**

Not yet scoped into increments.

---

# Last Completed Module

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

# Previously Completed Module

## Module 4 – Enterprise AI Platform

Completed Features

- Application Configuration
- Environment Variables
- Application Factory
- Structured Logging
- Health Endpoints
- Dependency Injection
- Provider Pattern
- Service Layer
- OpenAI Provider
- Chat API
- Streaming Support

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
```

`agents/` was created in Sprint 2 (`plan.py`, `planner.py`) and extended in Sprint 3 (`critique.py`, `reflector.py`) — holds the planning/reflection building blocks, the same way `rag/` holds RAG building blocks. The services that orchestrate them for DI/router use (`AgentService`, `PlanningService`, `ReflectionService`) still live in `services/`, consistent with Decision 003.

---

# Current Technology Stack

Backend

- Python 3.12
- FastAPI
- Pydantic
- OpenAI SDK
- LangChain (confined to `app/rag/`)
- Structlog

Upcoming

- SQLAlchemy
- PostgreSQL
- pgvector
- LangGraph

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

- Module 6, Sprint 4 – Memory (scoping not yet started)

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
- MCP
- Production Infrastructure

---

# Known Technical Debt

At the current stage there are no significant architectural concerns.

Planned improvements include:

- Repository layer for persistence.
- Request-scoped logging.
- Unified exception handling (currently handled per-router, e.g. `document.py` catches `ValueError`).
- `InMemoryVectorStore` is process-local and non-persistent by design — will be replaced by a `PostgreSQL` + `pgvector` implementation behind the same `VectorStore` interface once the RAG pipeline is otherwise proven out.
- `FaithfulnessService` parses the LLM judge's verdict from prompt-instructed JSON text, not a guaranteed schema. Malformed responses are reported as `is_faithful: null` rather than silently misreported, but this is best-effort parsing, not a guaranteed contract. `LLMProvider.generate_structured()` (added in Module 6, Sprint 2) now provides exactly the robust mechanism this needed — retrofitting `FaithfulnessService` to use it is an optional, non-blocking cleanup, not yet done.
- DOCX/HTML/Markdown loaders are not implemented — only PDF and raw text ingestion currently work.

These are intentional future enhancements rather than defects.

---

# Git Status

Latest Completed Milestone

Module 6, Sprint 3 – Reflection

Recommended Tag

```
v0.6.0-sprint3
```

---

# Next Development Task

Module 6, Sprint 4 – Memory

Not yet broken into increments.

Goal (module-level, per the roadmap):

Build a modular multi-agent system covering agent architecture, planning, reflection, memory, multi-agent collaboration, and state management, using LangGraph. Sprints 1 (Agent Architecture), 2 (Planning), and 3 (Reflection) are complete, all hand-built without LangGraph by design — LangGraph is introduced in Sprint 5 so it's recognizable as "the same loop, now framework-managed" rather than unexplained magic. The next step is scoping Sprint 4 the same way — a concept walkthrough and increment plan, before any code changes.

---

# Success Criteria

Module 6, Sprint 4 is ready to scope when:

- Sprint 3's reflect-and-revise loop is confirmed stable (it is — 81/81 tests passing, live-verified against the real OpenAI API).

---

# Resume Point

If continuing this project in a new conversation:

1. Read `PROJECT_CONTEXT.md`
2. Read `00-bootcamp-index.md`
3. Read this document (`02-current-status.md`)
4. Continue with:

**Module 6, Sprint 4 – Memory → scope into increments (not yet defined)**, or address the remaining Medium Priority backlog (DOCX/HTML/Markdown loaders) first if preferred.
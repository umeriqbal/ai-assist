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
| MCP | ⏳ Pending |
| Infrastructure | ⏳ Pending |
| Evaluation | ⏳ Pending |
| Capstone | ⏳ Pending |

---

# Current Module

**Module 7 – Model Context Protocol (MCP)**

Status:

⏳ Not Started

---

# Current Sprint

Not yet defined.

Module 7 hasn't been broken into sprints yet — that scoping happens the same way every prior module's did, at the start of the module rather than in advance. Per the roadmap, Module 7's topics are: MCP Specification, MCP Server, MCP Client, Tool Discovery, Remote Execution.

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
```

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

- Module 7 – Model Context Protocol (scoping not yet started)

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

These are intentional future enhancements rather than defects.

---

# Git Status

Latest Completed Milestone

Module 6 – AI Agents (all 6 sprints)

Recommended Tag

```
v0.6.0
```

---

# Next Development Task

Module 7 – Model Context Protocol (MCP)

Not yet broken into sprints/increments.

Goal (module-level, per the roadmap):

Build and consume MCP servers, covering the MCP specification, an MCP server, an MCP client, tool discovery, and remote execution. Module 6 (AI Agents) is fully complete: agent architecture, planning, reflection, memory, LangGraph/state management, and multi-agent collaboration, all built and live-verified. The first step when this resumes is scoping Module 7 into sprints the same way every prior module was — starting with a concept walkthrough and a plan for Sprint 1, before any code changes.

---

# Success Criteria

Module 7 is ready to scope when:

- Module 6's full agent system is confirmed stable (it is — 98/98 tests passing, every sprint live-verified against the real OpenAI API, including Sprint 6's multi-agent collaboration).
- A decision is made on whether to first close out the Medium Priority backlog (DOCX/HTML/Markdown loaders) or move straight into MCP.

---

# Resume Point

If continuing this project in a new conversation:

1. Read `PROJECT_CONTEXT.md`
2. Read `00-bootcamp-index.md`
3. Read this document (`02-current-status.md`)
4. Continue with:

**Module 7 – Model Context Protocol → scope Sprint 1 (not yet defined)**, or address the remaining Medium Priority backlog (DOCX/HTML/Markdown loaders) first if preferred.
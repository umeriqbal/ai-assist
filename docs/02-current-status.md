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
| Enterprise RAG | 🚧 In Progress |
| AI Agents | ⏳ Pending |
| MCP | ⏳ Pending |
| Infrastructure | ⏳ Pending |
| Evaluation | ⏳ Pending |
| Capstone | ⏳ Pending |

---

# Current Module

**Module 5 – Enterprise RAG**

Status:

🚧 In Progress

---

# Current Sprint

**Sprint 8 – Evaluation**

Status:

Ready to begin.

---

# Current Increment

**Increment 1 – Retrieval Metrics (Recall & Precision)**

Objective:

Build a small evaluation harness that measures whether retrieval actually returns the right chunks for a labeled set of questions, before moving on to faithfulness/hallucination checks on generated answers.

---

# Last Completed Sprint

## Module 5 / Sprint 7 – Citations

Completed Features

- `Citation` dataclass (`source`, `score`, `snippet`) — `score` explicitly documented as a relevance signal, not answer correctness
- `AnswerResult.sources: list[str]` replaced with `citations: list[Citation]`, one per chunk actually used (not deduplicated by source)
- `_snippet()` truncator (200 chars, ellipsis) so citations stay readable
- `AskResponse.citations` (breaking change from the old flat `sources` field — no compatibility shim, nothing else depended on the old shape)
- Unit tests for citation content and snippet truncation
- Live-verified against the real OpenAI API: citation carried a real similarity score and a correctly truncated snippet

Status

✅ Complete

---

# Additional Completed Work (Out of Sequence)

## PDF Upload Pipeline

Not a numbered sprint — a backlog fix (Medium Priority: "PDF Loader") pulled forward so real files could be tested end-to-end.

Completed Features

- Fixed `PDFLoader`: now properly implements the `DocumentLoader` interface (was previously not inheriting it at all, and exposed the wrong attribute name — `loader_factory.py` had been silently patched to check the wrong name instead of the loader being fixed)
- Fixed the sync/async mismatch that made `DocumentIngestionService.ingest()` crash on every real (non-empty) PDF; `PDFLoader.load()` is now properly async, using `asyncio.to_thread` for the blocking parse
- `ChunkingService.chunk_documents()` / `VectorStoreService.index_documents()` — generalized indexing to accept pre-loaded `Document`s (multi-page PDFs), not just raw text
- `DocumentUploadService` (new) — ingests a file, stamps `source`/`created_at`, indexes it; keeps PyPDFLoader's own `page`/`total_pages` metadata (unlocks page-level citations later)
- `POST /documents/upload` — real multipart file upload, testable directly through Swagger's auto-generated file picker
- Installed and declared the missing `python-multipart` dependency (required by FastAPI for file uploads)
- Unit tests using a hand-crafted minimal PDF fixture (no new test dependency)
- Live-verified via real HTTP multipart upload: a real PDF uploaded, ingested, indexed, and successfully queried through `/ask`

Status

✅ Complete

---

# Previously Completed Sprint

## Module 5 / Sprint 6 – Question Answering

Completed Features

- `PromptBuilder` (new, `app/rag/prompts/`) — pure formatting: grounding instruction + source-labeled context + question, no network calls
- `QuestionAnsweringService` (`answer`) — retrieves via `RetrievalService`, applies optional `min_score` filtering, skips the LLM call entirely when nothing qualifies (verified: no hallucinated answers on out-of-context questions)
- `POST /ask` endpoint
- `FakeLLMProvider` test double added alongside `FakeEmbeddingModel` — no real API calls in the automated suite
- Unit tests for prompt formatting and full answer orchestration (including the no-context short-circuit)
- Live-verified: a real indexed policy question answered correctly and grounded; an unrelated question correctly refused instead of guessed

Status

✅ Complete

---

# Last Completed Module

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

- Retrieval evaluation (recall, precision)
- Faithfulness / hallucination detection

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
- Evaluation
- Agents
- MCP

---

# Known Technical Debt

At the current stage there are no significant architectural concerns.

Planned improvements include:

- Repository layer for persistence.
- Request-scoped logging.
- Unified exception handling (currently handled per-router, e.g. `document.py` catches `ValueError`).
- `InMemoryVectorStore` is process-local and non-persistent by design — will be replaced by a `PostgreSQL` + `pgvector` implementation behind the same `VectorStore` interface once the RAG pipeline is otherwise proven out.

These are intentional future enhancements rather than defects.

---

# Git Status

Latest Completed Milestone

Module 4 – Enterprise AI Platform

Recommended Tag

```
v0.4.0
```

---

# Next Development Task

Module 5

Sprint 8

Increment 1

Title:

**Retrieval Metrics (Recall & Precision)**

Goal:

Build a small evaluation harness: a labeled set of (question, expected source) pairs, run each through `RetrievalService`, and compute recall/precision — did retrieval return the expected source within top-k? This establishes the measurement foundation before tackling the harder faithfulness/hallucination checks later in the sprint.

---

# Success Criteria

The next increment will be complete when:

- A small labeled evaluation set exists (question → expected source) covering the currently indexed test content.
- An `EvaluationService` (or similar) runs retrieval against each labeled case and reports recall/precision.
- The evaluation harness itself is testable without depending on live OpenAI calls (the embedding call can be faked, since recall/precision only care about which source came back, not the exact vector).
- Existing architecture remains unchanged.
- Results are presented in a way that's easy to re-run as the pipeline evolves (not a one-off script).

---

# Resume Point

If continuing this project in a new ChatGPT conversation:

1. Read `PROJECT_CONTEXT.md`
2. Read `00-bootcamp-index.md`
3. Read this document (`02-current-status.md`)
4. Continue with:

**Module 5 → Sprint 8 → Increment 1 → Retrieval Metrics (Recall & Precision)**
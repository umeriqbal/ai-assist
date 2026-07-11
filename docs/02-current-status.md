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

**Sprint 5 – Retrieval**

Status:

Ready to begin.

---

# Current Increment

**Increment 1 – Retrieval Service**

Objective:

Formalize query → search into a dedicated `RetrievalService` with metadata filtering, built on top of the Sprint 4 `VectorStoreService`, in preparation for grounded question answering.

---

# Last Completed Sprint

## Module 5 / Sprint 4 – Vector Storage

Completed Features

- `VectorStore` interface reworked to operate on `EmbeddedChunk` / query vectors, returning `ScoredChunk`
- `InMemoryVectorStore` — brute-force cosine similarity search, pure Python, no new dependency
- `VectorStoreService` (`index_text`, `search`), reusing `ChunkingService` and `EmbeddingService`
- `POST /documents/index` and `POST /documents/search` endpoints
- Removed the broken, docs-contradicting `ChromaVectorStore` and the `langchain-chroma` dependency
- Unit tests for cosine similarity correctness and full index→search orchestration

Status

✅ Complete

---

# Previously Completed Sprint

## Module 5 / Sprint 3 – Embeddings

Completed Features

- `EmbeddingModel` interface redefined as plain-Python async methods (no LangChain types leaking out of `rag/`)
- `OpenAIEmbeddingModel` (fixed from a broken, misnamed draft), batches all chunk texts into a single API call
- `EmbeddingService` (`embed_chunks`, `embed_query`), wired via Dependency Injection
- `POST /documents/embeddings` endpoint
- Unit tests using a fake embedding model (no real API calls in the test suite)

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

- Retrieval Service (metadata filtering)
- Question Answering
- Source Citations

---

## Medium Priority

- PDF Loader
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

Sprint 5

Increment 1

Title:

**Retrieval Service**

Goal:

Build a `RetrievalService` on top of `VectorStoreService.search`, adding metadata filtering (e.g. restrict by `source`) and a stable result shape that Sprint 6 (Question Answering) and Sprint 7 (Citations) can build on.

---

# Success Criteria

The next increment will be complete when:

- Search results can be filtered by document metadata (e.g. `source`), not just similarity score.
- The retrieval result shape carries everything a future citation needs (content, source, score).
- The RAG layer owns all LangChain interactions.
- No router communicates directly with LangChain or the OpenAI SDK.
- Existing architecture remains unchanged.
- The behaviour is covered by automated tests (with the embedding call faked, not live).

---

# Resume Point

If continuing this project in a new ChatGPT conversation:

1. Read `PROJECT_CONTEXT.md`
2. Read `00-bootcamp-index.md`
3. Read this document (`02-current-status.md`)
4. Continue with:

**Module 5 → Sprint 5 → Increment 1 → Retrieval Service**
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

**Sprint 6 – Question Answering**

Status:

Ready to begin.

---

# Current Increment

**Increment 1 – Grounded Answers**

Objective:

Build a `QuestionAnsweringService` that retrieves relevant chunks via `RetrievalService`, injects them into a prompt, and asks the `LLMProvider` to answer grounded only in that context.

---

# Last Completed Sprint

## Module 5 / Sprint 5 – Retrieval

Completed Features

- `VectorStore.similarity_search` gained `metadata_filter`, applied before ranking (not post-hoc), so filtered top-k is always correct
- `InMemoryVectorStore` filters candidates by metadata match prior to computing similarity
- `RetrievalService` (new) — owns the read path: validates query, embeds it, applies the filter
- `VectorStoreService` trimmed to indexing-only (`search()` removed — single responsibility restored)
- `POST /documents/search` gained an optional `source` filter (same endpoint, extended request)
- Unit tests for filter correctness (excludes non-matching, filters before ranking) and full retrieval orchestration

Status

✅ Complete

---

# Previously Completed Sprint

## Module 5 / Sprint 4 – Vector Storage

Completed Features

- `VectorStore` interface reworked to operate on `EmbeddedChunk` / query vectors, returning `ScoredChunk`
- `InMemoryVectorStore` — brute-force cosine similarity search, pure Python, no new dependency
- `VectorStoreService` (`index_text`), reusing `ChunkingService` and `EmbeddingService`
- `POST /documents/index` and `POST /documents/search` endpoints
- Removed the broken, docs-contradicting `ChromaVectorStore` and the `langchain-chroma` dependency
- Unit tests for cosine similarity correctness and full index→search orchestration

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

- Question Answering (grounded, prompt construction)
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

Sprint 6

Increment 1

Title:

**Grounded Answers**

Goal:

Build a `QuestionAnsweringService` that calls `RetrievalService.retrieve`, constructs a prompt that injects the retrieved chunks as context, and calls the existing `LLMProvider` to produce an answer grounded in that context rather than the model's own knowledge.

---

# Success Criteria

The next increment will be complete when:

- A question can be answered using only retrieved context (no unretrieved knowledge injected into the prompt by the service itself).
- The prompt construction step is isolated and testable independent of the LLM call.
- The RAG layer owns all LangChain interactions.
- No router communicates directly with LangChain or the OpenAI SDK.
- Existing architecture remains unchanged.
- The behaviour is covered by automated tests (with the embedding and chat calls faked, not live).

---

# Resume Point

If continuing this project in a new ChatGPT conversation:

1. Read `PROJECT_CONTEXT.md`
2. Read `00-bootcamp-index.md`
3. Read this document (`02-current-status.md`)
4. Continue with:

**Module 5 → Sprint 6 → Increment 1 → Grounded Answers**
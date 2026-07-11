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

**Sprint 2 – Chunking**

Status:

Ready to begin.

---

# Current Increment

**Increment 1 – Recursive Text Splitter**

Objective:

Split LangChain Documents into overlapping chunks sized for embedding, using `RecursiveCharacterTextSplitter`.

---

# Last Completed Sprint

## Module 5 / Sprint 1 – LangChain Foundations

Completed Features

- LangChain `Document` representation (`DocumentFactory`)
- Document metadata (`source`, `created_at`)
- `DocumentService` (business logic, wired via Dependency Injection)
- `POST /documents` endpoint
- Unit tests for document creation (valid text, whitespace stripping, empty-text rejection)

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
- Structlog

Upcoming

- LangChain
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

- RecursiveCharacterTextSplitter
- Embeddings
- Vector Store
- Retriever

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

- Provider interfaces for embeddings.
- Repository layer for persistence.
- Request-scoped logging.
- Broader automated test coverage (only `DocumentService` is currently tested).
- Unified exception handling (currently handled per-router, e.g. `document.py` catches `ValueError`).

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

Sprint 2

Increment 1

Title:

**Recursive Text Splitter**

Goal:

Split LangChain `Document` objects into overlapping chunks using `RecursiveCharacterTextSplitter`, wired through a tested `ChunkingService`, so downstream embedding/storage stages have appropriately sized input.

---

# Success Criteria

The next increment will be complete when:

- A `Document` can be split into multiple chunked `Document` objects.
- Chunk size and overlap are configurable.
- Original metadata is preserved (and extended with chunk position) on every chunk.
- The RAG layer owns all LangChain interactions.
- No router communicates directly with LangChain.
- Existing architecture remains unchanged.
- The behaviour is covered by automated tests.

---

# Resume Point

If continuing this project in a new ChatGPT conversation:

1. Read `PROJECT_CONTEXT.md`
2. Read `00-bootcamp-index.md`
3. Read this document (`02-current-status.md`)
4. Continue with:

**Module 5 → Sprint 2 → Increment 1 → Recursive Text Splitter**
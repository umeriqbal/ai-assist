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
| AI Agents | ⏳ Pending |
| MCP | ⏳ Pending |
| Infrastructure | ⏳ Pending |
| Evaluation | ⏳ Pending |
| Capstone | ⏳ Pending |

---

# Current Module

**Module 6 – AI Agents**

Status:

⏳ Not Started

---

# Current Sprint

Not yet defined.

Module 6 hasn't been broken into sprints yet — that scoping happens the same way Module 5's did, at the start of the module rather than in advance. Per the roadmap, Module 6's topics are: Agent Architecture, Planning, Reflection, Memory, Multi-Agent Collaboration, LangGraph, State Management.

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

- Agent Architecture (Module 6, Sprint scoping not yet started)

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
- `FaithfulnessService` parses the LLM judge's verdict from prompt-instructed JSON text, not a guaranteed schema (OpenAI's structured outputs / function calling would be more robust). Malformed responses are reported as `is_faithful: null` rather than silently misreported, but this is best-effort parsing, not a guaranteed contract.
- DOCX/HTML/Markdown loaders are not implemented — only PDF and raw text ingestion currently work.

These are intentional future enhancements rather than defects.

---

# Git Status

Latest Completed Milestone

Module 5 – Enterprise RAG

Recommended Tag

```
v0.5.0
```

---

# Next Development Task

Module 6 – AI Agents

Not yet broken into sprints/increments.

Goal (module-level, per the roadmap):

Build a modular multi-agent system covering agent architecture, planning, reflection, memory, multi-agent collaboration, and state management, using LangGraph. The first step when this resumes is scoping Module 6 into sprints the same way Module 5 was — starting with a concept walkthrough and a plan for Sprint 1, before any code changes.

---

# Success Criteria

Module 6 is ready to scope when:

- Module 5's full pipeline is confirmed stable (it is — 52/52 tests passing, every increment live-verified).
- A decision is made on whether to first close out the Medium Priority backlog (DOCX/HTML/Markdown loaders) or move straight into agents.

---

# Resume Point

If continuing this project in a new ChatGPT conversation:

1. Read `PROJECT_CONTEXT.md`
2. Read `00-bootcamp-index.md`
3. Read this document (`02-current-status.md`)
4. Continue with:

**Module 6 – AI Agents → scope Sprint 1 (not yet defined)**, or address the remaining Medium Priority backlog (DOCX/HTML/Markdown loaders) first if preferred.
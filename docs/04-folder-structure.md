# Project Folder Structure

> This document defines the official folder structure of the Enterprise AI Assistant.

This structure is considered the source of truth for the project. New components should fit into the existing architecture rather than creating new top-level folders.

---

# Repository Structure

```
enterprise-ai-assistant/
│
├── backend/
├── frontend/
├── infrastructure/
├── docs/
├── docker-compose.yml
├── .gitignore
├── LICENSE
└── README.md
```

---

# Backend

```
backend/
│
├── app/
├── tests/
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── .venv/
```

The backend contains the complete FastAPI application.

---

# Application Structure

```
app/
│
├── api/
├── core/
├── dependencies/
├── providers/
├── services/
├── rag/
├── database/
├── schemas/
├── models/
├── agents/
├── tools/
├── mcp/
├── static/
├── templates/
├── __init__.py
└── main.py
```

---

# API Layer

```
api/
│
├── routers/
│
├── __init__.py
```

Purpose

- HTTP Endpoints
- API Versioning (future)
- Authentication (future)

Example

```
routers/

chat.py

health.py

documents.py

agents.py

admin.py
```

---

# Core Layer

```
core/
│
├── application.py
├── config.py
├── logging.py
├── security.py          (future)
├── exceptions.py        (future)
└── __init__.py
```

Purpose

- Application startup
- Configuration
- Logging
- Shared infrastructure

---

# Dependency Layer

```
dependencies/
│
├── llm.py
├── services.py
├── database.py          (future)
├── auth.py              (future)
└── __init__.py
```

Purpose

Centralised Dependency Injection.

---

# Provider Layer

```
providers/
│
├── base.py
├── openai_provider.py
├── anthropic_provider.py    (future)
├── bedrock_provider.py      (future)
├── ollama_provider.py       (future)
└── __init__.py
```

Purpose

Wrappers around external SDKs.

Providers never contain business logic.

---

# Service Layer

```
services/
│
├── chat_service.py
├── streaming_service.py
├── embedding_service.py     (future)
├── retrieval_service.py     (future)
├── prompt_service.py        (future)
├── citation_service.py      (future)
├── evaluation_service.py    (future)
└── __init__.py
```

Purpose

Business logic.

---

# RAG Layer

```
rag/
│
├── document_service.py
├── document_loader.py
├── chunking_service.py
├── embedding_service.py
├── vector_store.py
├── retriever.py
├── prompt_builder.py
├── citation_service.py
└── __init__.py
```

Purpose

Everything related to Retrieval Augmented Generation.

LangChain exists only inside this layer.

---

# Database Layer

```
database/
│
├── connection.py
├── session.py
├── repositories/
├── migrations/
└── __init__.py
```

Future Technologies

- SQLAlchemy
- PostgreSQL
- pgvector

---

# Models

```
models/
│
├── document.py
├── conversation.py
├── user.py
└── __init__.py
```

Purpose

Database models.

---

# Schemas

```
schemas/
│
├── chat.py
├── document.py
├── health.py
├── common.py
└── __init__.py
```

Purpose

Pydantic request and response models.

---

# Agents

```
agents/
│
├── planner.py
├── researcher.py
├── reviewer.py
├── memory.py
├── coordinator.py
└── __init__.py
```

Purpose

Multi-agent orchestration.

---

# Tools

```
tools/
│
├── calculator.py
├── filesystem.py
├── github.py
├── weather.py
├── sql.py
├── search.py
└── __init__.py
```

Purpose

LLM tools — this project's own `Tool` implementations, protocol-agnostic.

---

# MCP

```
mcp/
│
├── server.py
├── run_server.py
├── client.py
├── http_server.py
├── run_http_server.py
└── __init__.py
```

Purpose

MCP server(s) and client(s). Confines the `mcp` SDK the same way `rag/` confines LangChain and `agents/` confines LangGraph — nothing outside this folder imports `mcp` directly. `server.py` adapts plain `Tool` instances (from `tools/`) onto the MCP protocol; `tools/` itself stays unaware that MCP exists.

---

# Static Files

```
static/
│
├── app.js
├── style.css
└── images/
```

Purpose

Frontend assets.

---

# Templates

```
templates/
│
├── index.html
└── components/
```

Purpose

Jinja2 templates.

---

# Tests

```
tests/
│
├── unit/
├── integration/
├── api/
├── fixtures/
└── conftest.py
```

Testing Strategy

- Unit Tests
- Integration Tests
- API Tests

---

# Documentation

```
docs/
│
├── PROJECT_CONTEXT.md
├── 00-bootcamp-index.md
├── 01-roadmap.md
├── 02-current-status.md
├── 03-architecture.md
├── 04-folder-structure.md
├── 05-design-decisions.md
├── 06-tech-stack.md
├── 07-development-guide.md
├── 08-learning-notes.md
├── 09-interview-notes.md
├── 10-changelog.md
│
├── modules/
├── adr/
├── diagrams/
└── api/
```

---

# Infrastructure

```
infrastructure/
│
├── terraform/
├── docker/
├── kubernetes/
└── aws/
```

Purpose

Infrastructure as Code.

---

# Frontend

```
frontend/
│
├── index.html
├── chat.html
├── kb.html
├── css/
│   └── styles.css
└── js/
    ├── api.js
    ├── main.js
    ├── chat.js
    └── kb.js
```

Introduced in Module 10, Sprint 1. No `package.json`, no `src/`/`public/` split, no build step — plain HTML/CSS/JS was chosen deliberately over React/Vue/Svelte (see [01-roadmap.md](01-roadmap.md)'s Module 10 section), so there's no npm dependency tree to scaffold. `js/api.js` is the shared `fetch()` wrapper every page reuses; served independently from the backend (e.g. `python -m http.server 5500`), calling it over CORS.

Sprint 2 (Enterprise Chat UI) added `chat.html` + `js/chat.js` — one HTML page + one JS file per feature, exactly as planned, rather than a component tree. `api.js` gained a second export, `apiPostStream()`, alongside `apiGet`/`apiPost` — needed because streaming a raw response body can't reuse the `response.json()`-based helper the other two share. Both pages now share a small top-bar nav linking between them (plain `<a href>`, no router).

Sprint 3 (Knowledge Base UI) added `kb.html` + `js/kb.js` — a document upload panel and a semantic search panel on one page. `api.js` gained a third export, `apiPostForm()`, for `FormData` uploads (no manually-set `Content-Type`, unlike the other two helpers) — three genuinely different request shapes now live behind three distinct, narrow functions rather than one branching helper. All three pages share the same top-bar nav.

Later sprints continue the same one-page-per-feature pattern (knowledge base, agents, evaluation, admin).

---

# Folder Responsibilities

| Folder | Responsibility |
|----------|----------------|
| api | HTTP Layer |
| core | Application Infrastructure |
| dependencies | Dependency Injection |
| providers | External SDKs |
| services | Business Logic |
| rag | Retrieval Augmented Generation |
| database | Persistence |
| schemas | Pydantic Models |
| models | Database Models |
| agents | AI Agents |
| tools | Tool Calling |
| mcp | Model Context Protocol (server/client) |
| static | Frontend Assets |
| templates | HTML Templates |
| tests | Automated Testing |
| docs | Project Documentation |

---

# Rules

The following rules apply throughout the project.

## Rule 1

Routers belong only inside

```
api/routers/
```

---

## Rule 2

Business logic belongs only inside

```
services/
```

---

## Rule 3

External SDKs belong only inside

```
providers/
```

---

## Rule 4

LangChain belongs only inside

```
rag/
```

---

## Rule 5

Database access belongs only inside

```
database/
```

---

## Rule 6

Pydantic models belong only inside

```
schemas/
```

---

## Rule 7

Application configuration belongs only inside

```
core/
```

---

# Architectural Principle

Every new feature should fit naturally into this folder structure.

If a new folder seems necessary, the architecture should be reviewed before introducing it.

The goal is to maintain a clean, consistent, and scalable project structure throughout the lifetime of the Enterprise AI Assistant.
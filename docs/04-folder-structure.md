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

LLM tools and MCP integrations.

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
├── src/
├── public/
├── package.json
└── README.md
```

The frontend will be introduced later in the bootcamp.

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
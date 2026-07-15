# Technology Stack

> This document describes every technology used in the Enterprise AI Assistant, why it was selected, and what role it plays within the architecture.

The goal is not to use as many technologies as possible, but to use mature, well-supported tools that solve real engineering problems.

---

# Technology Stack Overview

| Layer | Technology |
|---------|------------|
| Language | Python 3.12 |
| API | FastAPI |
| Validation | Pydantic |
| Configuration | pydantic-settings |
| AI Provider | OpenAI SDK |
| RAG | LangChain |
| Agents | LangGraph |
| Tool Integration | MCP |
| Frontend | Plain HTML/CSS/JS (no framework) |
| Database | PostgreSQL |
| Vector Search | pgvector |
| ORM | SQLAlchemy |
| Logging | Structlog |
| Testing | Pytest |
| Async HTTP | httpx |
| Containerisation | Docker |
| Infrastructure | Terraform |
| Cloud | AWS |
| Version Control | Git + GitHub |

---

# Programming Language

## Python 3.12

Purpose

The primary language used throughout the project.

Reason

- Excellent AI ecosystem
- Strong async support
- Mature web frameworks
- Excellent typing support
- Huge community

Used For

- API
- AI
- Services
- Agents
- Infrastructure scripts

---

# Web Framework

## FastAPI

Purpose

REST API Framework.

Responsibilities

- HTTP Endpoints
- Dependency Injection
- Validation
- OpenAPI Documentation
- Async Request Handling

Reason

- Excellent performance
- Automatic OpenAPI generation
- Native async support
- Strong typing
- Modern Python framework

---

# Validation

## Pydantic

Purpose

Data validation.

Used For

- Request Models
- Response Models
- Internal Data Objects

Benefits

- Automatic validation
- Type safety
- Excellent IDE support
- JSON serialization

---

# Configuration

## pydantic-settings

Purpose

Application configuration.

Responsibilities

- Environment variables
- Secrets
- Configuration validation

Example

```
.env

↓

Settings

↓

Application
```

---

# AI Provider

## OpenAI Python SDK

Purpose

Communication with OpenAI models.

Used For

- Chat
- Streaming
- Embeddings
- Structured Outputs

Reason

Official SDK.

Best compatibility.

---

## Anthropic Python SDK

Purpose

A second `LLMProvider` implementation (`ClaudeProvider`), proving the Provider Pattern generalizes beyond OpenAI.

Used For

- Chat, streaming, tool-calling, structured output — the same 6-method contract `OpenAIProvider` implements

Reason

Official SDK. Built standalone, not tied to a module's sprint sequence.

Status

Installed (`anthropic==0.116.0`) and implemented, but **not wired into any active service** — `get_openai_provider()` remains what every service actually uses. Exists so a provider switch is a future config change, not a rewrite. See [02-current-status.md](docs/02-current-status.md)'s Known Technical Debt and [01-roadmap.md](docs/01-roadmap.md)'s Module 9 section for the full reasoning.

---

# RAG Framework

## LangChain

Purpose

Retrieval Augmented Generation.

Used For

- Document Objects
- Document Loaders
- Text Splitters
- Embeddings
- Retrievers

Important Rule

LangChain is used only inside:

```
app/rag/
```

The rest of the application remains independent of LangChain.

---

# Agent Framework

## LangGraph

Purpose

Build production-quality AI agents.

Used For

- Agent orchestration
- Planning
- Reflection
- State management
- Multi-agent workflows

Reason

Production-ready architecture.

Status

Introduced in Module 6, Sprint 5, after the agent loop, planning, reflection, and memory (Sprints 1–4) were deliberately hand-built in plain Python first — so the underlying mechanics were understood before a framework managed them. Version pinned at `0.6.11` (not the 1.x line, which requires `langchain-core>=1.0` and conflicts with this project's pinned `langchain==0.3.27` stack). Confined to `app/rag/`'s sibling, `app/agents/` — same isolation principle as LangChain, applied to LangGraph.

Important detail: nodes in the graph call this project's own `LLMProvider`/`Tool` abstractions directly, not a LangChain chat model — see Decision 004 (Provider Pattern) and Decision 013 (LangChain Boundary). LangGraph orchestrates; it doesn't own the LLM call.

Extended in Sprint 6 to a multi-worker graph (`supervisor`/`researcher`/`writer` nodes) for multi-agent collaboration — same pattern, more worker nodes behind the conditional edge, routed by a structured decision instead of a boolean.

---

# Model Context Protocol

## MCP (Anthropic's official Python SDK)

Purpose

Connect AI applications to external tools and data sources via an open, vendor-neutral standard.

Used For

- Exposing this project's own tools to any MCP-compatible client (server side)
- Consuming tools from external MCP servers (client side, Sprint 2+)

Reason

Official SDK (Decision 014). Tool interfaces built for one AI application become reusable across any MCP-compatible one.

Status

Introduced in Module 7, Sprint 1. Version pinned at `1.28.1`, with an explicit `starlette==0.47.3` pin alongside it — `mcp` has no upper bound on its own `starlette` dependency, and installing it alone pulls in a release that conflicts with `fastapi==0.116.1`'s pin (same class of ecosystem conflict as `langgraph`/`langchain-core` in Sprint 5, resolved the same way and this time pinned explicitly to prevent future drift). Confined to `app/mcp/` — same isolation principle as LangChain in `app/rag/` and LangGraph in `app/agents/`.

Important detail: uses the SDK's low-level `Server` API, not the higher-level `FastMCP`. This project's `Tool.parameters` is already a hand-written JSON Schema; `FastMCP`'s decorator infers schemas from Python type hints instead, which would fight an already-explicit schema rather than reuse it. The low-level API accepts the schema directly via `types.Tool(inputSchema=...)` — confirmed with a smoke test before any production code was written.

Extended in Sprint 2 with the client side (`app/mcp/client.py`): `MCPToolAdapter`, `discover_tools()`, `connect_stdio_mcp_server()` — the mirror image of Sprint 1's server-side adapter, wrapping a remote MCP tool as this project's own `Tool` rather than the reverse. Live-verified against the real Sprint 1 server with zero hard-coded tool names anywhere in the client.

Extended again in Sprint 3 with a genuinely networked transport: `app/mcp/http_server.py`/`run_http_server.py` serve the same tools over MCP's streamable-HTTP transport (a standing service on its own port, not a subprocess pipe), and `connect_http_mcp_server()` mirrors the stdio connector using `streamable_http_client`. `create_app()` gained its first `lifespan` — connecting to the MCP HTTP server at startup, discovering its tools, and building an `AgentService` from them (`POST /agents/mcp-chat`) — the first dependency in this project needing real async setup/teardown rather than a lazy `@lru_cache` constructor. **Module 7 (MCP) is now fully complete**, live-verified with the MCP server and the FastAPI app running as two independent, real processes.

---

# Frontend

## Plain HTML/CSS/JS (no framework)

Purpose

Serve a real browser-based UI for this project's own API, as a standalone static site — independent of the FastAPI backend, not Jinja2-rendered by it.

Used For

- `frontend/index.html` + `css/styles.css` — page structure and styling
- `js/api.js` — a shared `fetch()` wrapper (`apiGet`/`apiPost`) every page reuses
- `js/main.js` — page-specific logic (Sprint 1: calls `GET /health` on load, renders backend status)

Reason

React/Vue/Svelte were considered and declined (Decision recorded in [01-roadmap.md](01-roadmap.md)'s Module 10 section) — consistent with this project's recurring "understand the mechanics before adopting a framework" pattern (the same reasoning that delayed LangGraph to Sprint 5 and FastMCP was never adopted at all). No npm dependency tree, no build step, nothing to scaffold for a project this size.

Status

Introduced in Module 10, Sprint 1. Requires `CORSMiddleware` on the backend (`app/core/application.py`) plus a `FRONTEND_URL` setting — an explicit allowed origin, not `*` — since this is the first client in the project ever served from a different origin than the backend. Live-verified in a real headless Chromium browser via an ad hoc Playwright driver script.

Extended in Sprint 2 with `chat.html`/`js/chat.js` — a real streaming chat interface wired to `POST /chat/stream`, chosen over `POST /agents/chat` to get live token-by-token streaming (accepting no cross-turn memory as the trade-off). `js/api.js` gained a second helper, `apiPostStream()`, reading the response body via `getReader()` since a streamed body isn't `response.json()`-shaped.

Extended again in Sprint 3 with `kb.html`/`js/kb.js` — a document upload panel (`POST /documents/upload`) and semantic search panel (`POST /documents/search`) on one page. `js/api.js` gained a third helper, `apiPostForm()`, sending `FormData` with no manually-set `Content-Type` — three genuinely different request shapes (JSON, streamed text, multipart form) now each get their own narrow function. Live-verified with a real, hand-crafted minimal PDF fixture (no PDF library or fixture file existed yet, so one was generated the same way `tests/conftest.py`'s `write_minimal_pdf()` does for backend tests). Later sprints continue adding one HTML page + one JS file per feature (agents, evaluation, admin) rather than a component tree.

---

# Database

## PostgreSQL

Purpose

Primary relational database.

Stores

- Users
- Documents
- Conversations
- Metadata
- Configuration

Reason

- Mature
- Reliable
- Excellent ecosystem
- Enterprise standard

---

# Vector Search

## pgvector

Purpose

Store embeddings inside PostgreSQL.

Reason

Avoid introducing another database unless necessary.

Benefits

- Simpler deployment
- ACID transactions
- SQL support
- Production ready

---

# ORM

## SQLAlchemy

Purpose

Database abstraction.

Responsibilities

- Models
- Queries
- Relationships
- Transactions

Reason

Most widely used Python ORM.

---

# Logging

## Structlog

Purpose

Structured logging.

Used For

- API logs
- AI logs
- Error tracking
- Performance metrics

Reason

Machine-readable logs.

Cloud friendly.

---

# Async HTTP

## httpx

Purpose

Async HTTP client.

Future Uses

- Calling APIs
- Tool integrations
- Webhooks

---

# Testing

## Pytest

Purpose

Testing framework.

Test Types

- Unit Tests
- Integration Tests
- API Tests

Future

Coverage reports.

---

# Containerisation

## Docker

Purpose

Application packaging.

Future

- Local development
- Deployment
- CI/CD
- Production

---

# Infrastructure

## Terraform

Purpose

Infrastructure as Code.

Future Resources

- AWS
- Networking
- Databases
- Secrets
- Compute

---

# Cloud

## Amazon Web Services

Deployment Platform.

Planned Services

- EC2
- ECS
- ECR
- RDS
- S3
- IAM
- CloudWatch
- Secrets Manager
- Application Load Balancer

---

# Version Control

## Git

Purpose

Source control.

Workflow

```
Feature

↓

Commit

↓

Push

↓

Merge
```

---

# Documentation

## Markdown

Purpose

Project documentation.

Stored In

```
docs/
```

Documentation evolves alongside the project.

---

# Architecture Diagram

```
Browser

↓

FastAPI

↓

Services

↓

Providers

↓

OpenAI

↓

LangChain

↓

PostgreSQL

↓

pgvector
```

---

# Future Technologies

The following technologies will be introduced later.

| Technology | Purpose |
|------------|---------|
| Redis | Caching |
| Celery / Background Tasks | Long-running jobs |
| Playwright | Website crawling |
| BeautifulSoup | HTML parsing |
| Alembic | Database migrations |
| Prometheus | Metrics |
| Grafana | Dashboards |
| GitHub Actions | CI/CD |

---

# Technologies We Intentionally Do Not Use

The following technologies are intentionally excluded.

## ChromaDB

Reason

We will use PostgreSQL + pgvector instead.

---

## Pinecone

Reason

Avoid vendor lock-in.

---

## Weaviate

Reason

Unnecessary operational complexity for this project.

---

## FAISS

Reason

Useful for experimentation, but not our production architecture.

---

# Technology Selection Principles

Every technology included in this project must satisfy one or more of the following:

- Industry standard
- Production proven
- Well documented
- Actively maintained
- Solves a real engineering problem

Technologies are chosen to support long-term maintainability rather than following trends.

---

# Summary

The Enterprise AI Assistant is built using a modern, production-oriented technology stack focused on scalability, maintainability, and practical AI engineering.

The architecture remains framework-independent wherever possible, ensuring that external libraries can evolve without forcing major changes to the overall system design.
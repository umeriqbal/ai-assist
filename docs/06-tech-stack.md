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
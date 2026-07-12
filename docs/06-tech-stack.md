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

Not yet introduced. Module 6's agent loop, planning, and reflection (Sprints 1–3) were deliberately hand-built in plain Python first, without LangGraph — so the underlying mechanics are understood before a framework manages them. LangGraph is scoped for Sprint 5.

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
- MCP
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
# Enterprise AI Assistant
# AI Engineer Bootcamp

> Master index for the entire project.

This document is the starting point for both developers and future ChatGPT sessions.

---

# Project

Enterprise AI Assistant

Purpose:

Build a production-quality AI platform while learning modern AI Engineering through hands-on development.

This project follows real software engineering practices including:

- Layered Architecture
- SOLID Principles
- Dependency Injection
- Provider Pattern
- Service Layer
- Production Logging
- Testing
- Documentation
- Git Workflow

---

# Current Status

| Item | Value |
|------|-------|
| Current Module | Module 6 – AI Agents |
| Current Sprint | Not yet defined |
| Current Increment | Not yet defined |
| Status | Module 5 (Enterprise RAG) Complete. Module 6 not yet scoped into sprints |

---

# Project Goals

The completed application will include:

- Enterprise Chat
- Retrieval Augmented Generation (RAG)
- PDF Knowledge Base
- Website Crawling
- Multi-Agent Workflows
- Model Context Protocol (MCP)
- Tool Calling
- PostgreSQL + pgvector
- Evaluation Framework
- AWS Deployment
- Production Monitoring

---

# Documentation Index

## Project

| File | Description |
|------|-------------|
| PROJECT_CONTEXT.md | Complete project context for continuing development |
| 01-roadmap.md | Full bootcamp roadmap |
| 02-current-status.md | Current progress snapshot |
| 03-architecture.md | System architecture |
| 04-folder-structure.md | Official project structure |
| 05-design-decisions.md | Architecture decisions |
| 06-tech-stack.md | Technology stack |
| 07-development-guide.md | Development setup |
| 08-learning-notes.md | AI Engineering notes |
| 09-interview-notes.md | Interview preparation |
| 10-changelog.md | Feature history |

---

## Module Documentation

| Module | Status |
|---------|--------|
| module-01.md | Complete |
| module-02.md | Complete |
| module-03.md | Complete |
| module-04.md | Complete |
| module-05.md | Complete |
| module-06.md | Current |
| module-07.md | Pending |
| module-08.md | Pending |
| module-09.md | Pending |
| module-10.md | Pending |

---

# Completed Modules

## Module 1

LLM Fundamentals

Completed Topics

- Tokens
- Context Windows
- Hallucinations
- Prompt Structure
- Roles
- Temperature
- Cost

Status

Complete

---

## Module 2

Prompt Engineering

Completed Topics

- Structured Outputs
- JSON Responses
- Validation
- Prompt Templates
- FastAPI Integration
- OpenAI Responses API

Status

Complete

---

## Module 3

Semantic Search

Completed Topics

- Embeddings
- Cosine Similarity
- Chunking
- Vector Search
- Search Ranking
- In-memory Search Engine

Status

Complete

---

## Module 4

Enterprise AI Platform

Completed Topics

- Layered Architecture
- Configuration Management
- Application Factory
- Structured Logging
- Health Endpoints
- Dependency Injection
- Provider Pattern
- Service Layer
- Chat API
- Streaming Support

Status

Complete

---

## Module 5

Enterprise RAG

Completed Topics

- LangChain Documents
- Text Splitters
- Embeddings
- Vector Stores
- Retrieval (with metadata filtering)
- Question Answering (grounded, verified against hallucination)
- Source Citations
- Evaluation (recall/precision, faithfulness/hallucination detection)

Also fixed out of sequence: the PDF upload pipeline (loader was broken since before Module 5 began), so real files can be ingested, not just raw text.

Status

Complete

---

# Architecture

The project follows a layered architecture.

```
HTTP

↓

Routers

↓

Services

↓

Providers

↓

External Services
```

LangChain exists only inside the RAG layer.

Routers never communicate directly with external SDKs.

---

# Coding Standards

- Async first
- SOLID principles
- Strong typing
- Thin routers
- Service layer
- Provider abstraction
- Dependency Injection
- Pydantic validation
- Complete file replacements
- One responsibility per class
- Git commit after every increment

---

# Git Workflow

Every completed increment follows:

```
Implement

↓

Test

↓

Review

↓

Update Docs

↓

Commit

↓

Push
```

---

# Bootcamp Philosophy

This bootcamp focuses on building production-quality AI systems.

Libraries are used where appropriate.

Architecture is designed and owned by us.

The goal is to understand AI engineering patterns rather than becoming dependent on any single framework.

---

# Current Milestone

Module 6 – AI Agents

Not yet scoped into sprints. First step when work resumes: a concept walkthrough and a concrete plan for Sprint 1, same approach used to start Module 5.

---

# Next Milestones

- AI Agents (Agent Architecture, Planning, Reflection, Memory, Multi-Agent Collaboration, LangGraph, State Management)
- Model Context Protocol (MCP)
- Production Infrastructure (Docker, PostgreSQL, pgvector, Terraform, AWS, CI/CD)
- Evaluation & Observability (cost/latency/prompt versioning — system-wide, distinct from Module 5's RAG-quality evaluation)
- Enterprise AI Assistant (final integration)

Also still open, non-blocking: DOCX/HTML/Markdown loaders (Medium Priority backlog carried over from Module 5).

---

# How to Continue This Project

When starting a new ChatGPT conversation:

1. Read `PROJECT_CONTEXT.md`
2. Read `00-bootcamp-index.md`
3. Read `02-current-status.md`
4. Continue from the current module and sprint

No previous conversation should be required to continue development.
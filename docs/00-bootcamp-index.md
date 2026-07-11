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
| Current Module | Module 5 – Enterprise RAG |
| Current Sprint | Sprint 5 – Retrieval |
| Current Increment | Increment 1 – Retrieval Service |
| Status | Sprint 4 Complete. Ready to Begin Sprint 5 |

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
| module-05.md | Current |
| module-06.md | Pending |
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

Current Topics

- LangChain Documents
- Text Splitters
- Embeddings
- Vector Stores
- Retrieval
- Source Citations

Status

In Progress

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

Module 5

Sprint 5

Increment 1

Objective:

Build a Retrieval Service on top of the Sprint 4 vector store search, adding metadata filtering, integrated into the existing layered architecture.

---

# Next Milestones

- Semantic Retrieval
- Question Answering
- Source Citations
- PostgreSQL + pgvector
- Hybrid Search
- Evaluation

---

# How to Continue This Project

When starting a new ChatGPT conversation:

1. Read `PROJECT_CONTEXT.md`
2. Read `00-bootcamp-index.md`
3. Read `02-current-status.md`
4. Continue from the current module and sprint

No previous conversation should be required to continue development.
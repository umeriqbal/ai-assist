# AI Engineer Bootcamp Roadmap

> Complete roadmap for the Enterprise AI Assistant project.

---

# Overview

The objective of this bootcamp is to become a production-ready AI Engineer by building a real Enterprise AI Assistant from scratch.

The project is intentionally cumulative. Every module builds upon the previous one until a complete enterprise-grade system is produced.

---

# Module 1 — LLM Fundamentals

**Status:** ✅ Complete

## Objectives

Understand how modern LLMs work.

### Topics

- Tokens
- Tokenization
- Context Windows
- Prompt Structure
- System/User/Assistant Roles
- Temperature
- Hallucinations
- API Costs
- Responses API
- Streaming Concepts

### Outcome

A solid understanding of how Large Language Models work internally and how they are consumed through APIs.

---

# Module 2 — Prompt Engineering

**Status:** ✅ Complete

## Objectives

Learn how to build reliable applications using prompts.

### Topics

- Prompt Templates
- Prompt Chaining
- Structured Outputs
- JSON Responses
- Pydantic Validation
- Error Handling
- FastAPI Integration

### Outcome

Built a Prompt Playground capable of generating structured AI responses.

---

# Module 3 — Semantic Search

**Status:** ✅ Complete

## Objectives

Understand semantic search from first principles.

### Topics

- Embeddings
- Vector Mathematics
- Cosine Similarity
- Chunking
- Context Management
- Search Ranking
- In-memory Vector Store

### Outcome

Built a complete semantic search engine without relying on external frameworks.

---

# Module 4 — Enterprise AI Platform

**Status:** ✅ Complete

## Objectives

Build a production-ready backend architecture.

### Topics

- Layered Architecture
- FastAPI Application Factory
- Configuration Management
- Dependency Injection
- Provider Pattern
- Service Layer
- Structured Logging
- Health Endpoints
- Chat API
- Streaming API
- OpenAI Provider

### Outcome

Created a reusable enterprise AI platform that will host all future capabilities.

---

# Module 5 — Enterprise RAG

**Status:** ✅ Complete

## Objectives

Build an enterprise Retrieval Augmented Generation platform.

### Sprint 1

LangChain Foundations

- LangChain Documents
- Document Metadata
- Document Service

---

### Sprint 2

Chunking

- RecursiveCharacterTextSplitter
- Chunk Strategies
- Metadata Preservation

---

### Sprint 3

Embeddings

- OpenAI Embeddings
- Embedding Service
- Batch Processing
- Cost Considerations

---

### Sprint 4

Vector Storage

Initially:

- In-memory

Later:

- PostgreSQL
- pgvector

---

### Sprint 5

Retrieval

- Similarity Search
- Top-K Retrieval
- Metadata Filtering
- Retrieval Pipeline

---

### Sprint 6

Question Answering

- Prompt Construction
- Context Injection
- Source Selection
- Grounded Answers

---

### Sprint 7

Citations

- Source Attribution
- Page Numbers
- Confidence

---

### Sprint 8

Evaluation

- Recall
- Precision
- Faithfulness
- Hallucination Detection

### Outcome

A complete enterprise document question-answering system.

---

# Module 6 — AI Agents

**Status:** ✅ Complete

## Objectives

Build production-quality AI agents.

### Sprint 1

Agent Architecture (foundations)

- `Tool` abstraction
- Provider tool-calling support
- Agent loop (ReAct-style)
- `POST /agents/chat`

**Status:** ✅ Complete

---

### Sprint 2

Planning

- `Plan` / `PlanStep` models
- Provider structured-output support
- `Planner`
- `PlanningService`
- `POST /agents/plan`

**Status:** ✅ Complete

---

### Sprint 3

Reflection

- `Critique` model
- `Reflector`
- `ReflectionService`
- `POST /agents/reflect`

**Status:** ✅ Complete

---

### Sprint 4

Memory

- `ConversationMemory` interface / `InMemoryConversationMemory`
- `AgentService.chat()` extended with `conversation_id`
- `POST /agents/chat` returns and accepts `conversation_id`

**Status:** ✅ Complete

---

### Sprint 5

LangGraph + State Management

- `AgentGraphState` + graph nodes (`call_model`, `call_tools`) rebuilding the Sprint 1 loop
- `MemorySaver` checkpointer for state management (replaces `ConversationMemory` for this path)
- `AgentGraphService`
- `POST /agents/graph-chat`

**Status:** ✅ Complete

---

### Sprint 6

Multi-Agent Collaboration

- `SupervisorDecision` model
- `Supervisor` (routes via `generate_structured()`)
- `MultiAgentState` + `supervisor`/`researcher`/`writer` graph nodes
- `MultiAgentService`
- `POST /agents/collaborate`

**Status:** ✅ Complete

### Outcome

A modular multi-agent system.

---

# Module 7 — Model Context Protocol (MCP)

**Status:** ⏳ Planned

## Objectives

Build and consume MCP servers.

### Topics

- MCP Specification
- MCP Server
- MCP Client
- Tool Discovery
- Remote Execution

### Outcome

Enterprise-ready MCP integration.

---

# Module 8 — Production Infrastructure

**Status:** ⏳ Planned

## Objectives

Deploy the platform to production.

### Topics

- Docker
- Docker Compose
- PostgreSQL
- pgvector
- Redis
- Terraform
- AWS
- CI/CD
- Monitoring
- Secrets Management

### Outcome

Cloud-hosted production deployment.

---

# Module 9 — Evaluation & Observability

**Status:** ⏳ Planned

## Objectives

Measure AI system quality.

### Topics

- Offline Evaluation
- Online Evaluation
- Cost Tracking
- Latency Monitoring
- Token Usage
- Prompt Versioning
- Model Comparison

### Outcome

A measurable AI platform with production observability.

---

# Module 10 — Enterprise AI Assistant

**Status:** ⏳ Planned

## Objectives

Combine everything into one application.

### Features

- Enterprise Chat
- Knowledge Base
- Website Crawling
- PDF Search
- Agents
- Tool Calling
- MCP
- Evaluation Dashboard
- Admin Interface

### Outcome

A production-quality Enterprise AI Assistant suitable for portfolio demonstrations and real-world deployment.

---

# Progress Summary

| Module | Name | Status |
|---------|------|--------|
| 1 | LLM Fundamentals | ✅ Complete |
| 2 | Prompt Engineering | ✅ Complete |
| 3 | Semantic Search | ✅ Complete |
| 4 | Enterprise AI Platform | ✅ Complete |
| 5 | Enterprise RAG | ✅ Complete |
| 6 | AI Agents | ✅ Complete |
| 7 | Model Context Protocol | ⏳ Planned |
| 8 | Production Infrastructure | ⏳ Planned |
| 9 | Evaluation & Observability | ⏳ Planned |
| 10 | Enterprise AI Assistant | ⏳ Planned |

---

# Current Focus

**Module 6 – AI Agents: Complete**

Last Completed Sprint:

**Sprint 6 – Multi-Agent Collaboration** — `Supervisor` (routes via Sprint 2's `generate_structured()`) coordinating two specialist `AgentService` instances (Researcher: knowledge-base tool; Writer: no tools, synthesis only) through a LangGraph graph, exposed as `POST /agents/collaborate`. Live-verified: the supervisor correctly sequenced researcher → writer → finish, each specialist producing genuinely distinct output.

Next milestone:

**Module 7 – Model Context Protocol (MCP)**, not yet scoped into sprints. First step when this resumes: a concept walkthrough and concrete Sprint 1 plan, the same process used to start every prior module.
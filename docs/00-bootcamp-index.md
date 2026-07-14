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
| Current Module | Module 8 – Production Infrastructure |
| Current Sprint | Not yet defined |
| Current Increment | Not yet defined |
| Status | Module 7 (MCP) Complete — all 3 sprints, 107/107 tests passing, live-verified across genuine process boundaries (stdio and real HTTP, two independent processes). Module 8 not yet scoped into sprints. Module 9 scoped then deliberately deferred (see below) |

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
| module-06.md | Complete |
| module-07.md | Complete |
| module-08.md | Current |
| module-09.md | Deferred |
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

## Module 6

AI Agents

Completed Sprints

- **Sprint 1 – Agent Architecture:** `Tool` interface, `LLMProvider.chat_with_tools()` / `tool_result_messages()` (OpenAI tool-calling kept behind the provider boundary), `AgentService` (ReAct loop with iteration cap and graceful unknown-tool handling), `KnowledgeBaseSearchTool` (wraps `RetrievalService`), `POST /agents/chat`
- **Sprint 2 – Planning:** `app/agents/` layer created; `Plan`/`PlanStep`, `LLMProvider.generate_structured()` (OpenAI structured output), `Planner`, `PlanningService` (executes a plan step by step via `AgentService`, then synthesizes an answer), `POST /agents/plan`
- **Sprint 3 – Reflection:** `Critique`, `Reflector` (reuses `generate_structured()`, no new provider work needed), `ReflectionService` (generate → critique → revise loop, best-effort answer on hitting the iteration cap rather than raising), `POST /agents/reflect`
- **Sprint 4 – Memory:** `ConversationMemory` interface + `InMemoryConversationMemory` (process-local, non-persistent by design, same trade-off as `InMemoryVectorStore`), `AgentService.chat()` extended with an optional `conversation_id`, `POST /agents/chat` now generates/returns/accepts a `conversation_id` for real multi-turn conversations
- **Sprint 5 – LangGraph + State Management:** `langgraph==0.6.11` (first new dependency since Module 5); the Sprint 1 loop rebuilt as a LangGraph graph (`call_model`/`call_tools` nodes calling the same `LLMProvider`/`Tool` methods `AgentService` uses — LangGraph replaces only the loop's control flow), compiled with a `MemorySaver` checkpointer for state management; `AgentGraphService`; `POST /agents/graph-chat` alongside (not replacing) `POST /agents/chat`
- **Sprint 6 – Multi-Agent Collaboration:** `AgentService` gained an optional `system_prompt` (an agent can now have a role); `Supervisor` (routes via `generate_structured()`, reused a third time) coordinating a Researcher and a Writer specialist — both ordinary `AgentService` instances, differently configured — through a LangGraph graph built on Sprint 5's pattern; `MultiAgentService`; `POST /agents/collaborate`

Every sprint above unit-tested and live-verified against the real OpenAI API — Sprint 6's included watching the Supervisor correctly sequence Researcher → Writer → finish with two genuinely distinct specialist outputs.

Status

Complete

---

## Module 7

Model Context Protocol (MCP)

Completed Sprints

- **Sprint 1 – MCP Server Foundations:** `mcp==1.28.1` + an explicit `starlette==0.47.3` pin (same class of ecosystem conflict as Sprint 5's `langgraph`, resolved the same way); `app/mcp/` layer created (new top-level folder, reviewed before adding); `build_mcp_server()` — low-level MCP `Server` API, chosen over `FastMCP` because `Tool.parameters` already maps directly onto MCP's `inputSchema`, validated with a smoke test first; `run_server.py` — standalone stdio server exposing `EchoTool` and the real `KnowledgeBaseSearchTool`
- **Sprint 2 – MCP Client + Tool Discovery:** `MCPToolAdapter` (`app/mcp/client.py`) — the mirror image of Sprint 1's server-side adapter, wrapping a remote MCP tool as this project's own `Tool`; `discover_tools()` — zero hard-coded tool names anywhere in the client; `connect_stdio_mcp_server()` — spawns an MCP server subprocess and returns an initialized session
- **Sprint 3 – Remote Execution / Agent Integration:** MCP server upgraded to streamable-HTTP (`http_server.py`/`run_http_server.py`) — a genuinely network-addressable service, not a subprocess pipe; `connect_http_mcp_server()`; `create_app()` gained its first `lifespan` (connects to the MCP HTTP server at startup, discovers tools, builds an `AgentService`); `POST /agents/mcp-chat`

Live-verified across genuine process boundaries every sprint: stdio subprocess (Sprints 1–2), and real HTTP between two independently-running processes (Sprint 3) — a forced remote tool call round-tripped correctly end to end.

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

Module 8 – Production Infrastructure

Module 7 (MCP) is fully complete — all 3 sprints. Not yet scoped into sprints. First step when work resumes: a concept walkthrough and a concrete plan for Sprint 1, same approach used to start every prior module.

---

# Next Milestones

- Production Infrastructure (Docker, PostgreSQL, pgvector, Terraform, AWS, CI/CD)
- Enterprise AI Assistant (final integration)

**Evaluation & Observability (Module 9) — deliberately deferred, not on the near-term path.** Scoped to a concrete Sprint 1 plan, then explicitly not built: cost tracking, latency monitoring, model comparison, and prompt versioning only have real value against ongoing real traffic or an automated decision acting on the data — neither exists yet. A standalone `ClaudeProvider` was built alongside this discussion (proving the Provider Pattern generalizes) but isn't wired into any service. Revisit once there's real production traffic (likely post-Module 8) or provider selection becomes a genuine runtime decision.

Also still open, non-blocking: DOCX/HTML/Markdown loaders (Medium Priority backlog carried over from Module 5).

---

# How to Continue This Project

When starting a new ChatGPT conversation:

1. Read `PROJECT_CONTEXT.md`
2. Read `00-bootcamp-index.md`
3. Read `02-current-status.md`
4. Continue from the current module and sprint

No previous conversation should be required to continue development.
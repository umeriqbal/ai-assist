# Enterprise AI Assistant
## Project Context

> This file is the primary source of context for continuing the AI Engineer Bootcamp in a new ChatGPT conversation.

---

# Project Goal

Build a production-quality Enterprise AI Assistant while learning modern AI Engineering through hands-on development.

The emphasis is on architecture, maintainability, scalability and production practices rather than toy examples.

The completed project should demonstrate the skills expected of an AI Engineer.

---

# Current Status

Current Module:

Module 6 – AI Agents

Current Sprint:

Sprint 4 – Memory (not yet scoped into increments)

Status:

Module 5 (Enterprise RAG) is complete: all 8 sprints delivered, unit-tested, and live-verified against the real OpenAI API. Module 6, Sprints 1–3 (Agent Architecture, Planning, Reflection) are complete — 81/81 tests passing, live-verified against the real OpenAI API. Sprint 4 (Memory) scoping has not started.

---

# Bootcamp Modules

| Module | Status |
|---------|--------|
| Module 1 - LLM Fundamentals | Complete |
| Module 2 - Prompt Engineering | Complete |
| Module 3 - Semantic Search | Complete |
| Module 4 - Enterprise AI Platform | Complete |
| Module 5 - Enterprise RAG | Complete |
| Module 6 - AI Agents | Current |
| Module 7 - Model Context Protocol (MCP) | Pending |
| Module 8 - Production Infrastructure | Pending |
| Module 9 - Evaluation & Observability | Pending |
| Module 10 - Enterprise AI Assistant | Pending |

---

# Architecture Principles

The project follows Layer-Based Architecture.

```
API
    ↓
Services
    ↓
Providers
    ↓
External APIs
```

LangChain is used only inside the RAG layer.

Routers never communicate directly with providers.

Business logic belongs in Services.

External SDKs are wrapped by Providers.

---

# Coding Standards

- Python 3.12+
- FastAPI
- Async first
- SOLID principles
- Strong typing
- Pydantic validation
- Thin routers
- Service layer
- Provider abstraction
- Dependency Injection
- Complete file replacements during implementation
- Git commit after every completed increment

---

# Current Folder Structure

```
enterprise-ai-assistant/

backend/
    app/
        api/
        core/
        providers/
        services/
        dependencies/
        rag/
        database/
        schemas/
        models/
        agents/
        tools/
        main.py

frontend/

infrastructure/

docs/
```

---

# Technologies

Backend

- FastAPI
- Pydantic
- OpenAI SDK
- LangChain (confined to `app/rag/`)
- Structlog

Future

- LangGraph
- PostgreSQL
- pgvector
- SQLAlchemy
- Docker
- Terraform
- AWS

---

# Completed Features

Application configuration

- Environment variables
- Typed configuration
- Pydantic Settings

Application Factory

- create_app()

Logging

- Structured logging
- Configurable log levels

Health Endpoints

- /
- /live
- /ready
- /health

Dependency Injection

- FastAPI Depends
- Provider injection

Provider Pattern

- LLMProvider interface
- OpenAIProvider implementation

Service Layer

- ChatService
- StreamingService

Chat API

- POST /chat

Streaming

- Provider streaming
- StreamingService
- Streaming endpoint

Document Service (Module 5, Sprint 1)

- LangChain `Document` representation (`DocumentFactory`)
- Document metadata (`source`, `created_at`)
- `DocumentService`, injected via `Depends`
- `POST /documents`
- Unit tests

Chunking Service (Module 5, Sprint 2)

- `RecursiveDocumentSplitter` with `chunk_index` / `chunk_count` / `start_index` metadata
- `ChunkingService`, reusing `DocumentService`, injected via `Depends`
- `POST /documents/chunks` (configurable `chunk_size` / `chunk_overlap`)
- Unit tests

Embedding Service (Module 5, Sprint 3)

- `EmbeddingModel` interface (plain-Python async methods, no LangChain leak)
- `OpenAIEmbeddingModel`, batches all chunk texts into a single API call
- `EmbeddingService` (`embed_chunks`, `embed_query`), injected via `Depends`
- `POST /documents/embeddings`
- Unit tests using a fake embedding model (no live API calls in the suite)

Vector Storage (Module 5, Sprint 4)

- `VectorStore` interface operating on `EmbeddedChunk` / query vectors, returning `ScoredChunk`
- `InMemoryVectorStore` — brute-force cosine similarity, no new dependency
- `VectorStoreService` (`index_text`), injected via `Depends`
- `POST /documents/index`, `POST /documents/search`
- Removed the broken, docs-contradicting Chroma implementation and dependency
- Unit tests for similarity correctness and index→search orchestration

Retrieval Service (Module 5, Sprint 5)

- `VectorStore.similarity_search` gained `metadata_filter`, applied before ranking
- `InMemoryVectorStore` filters candidates by metadata prior to scoring
- `RetrievalService` (`retrieve`), owns the read path, injected via `Depends`
- `VectorStoreService` trimmed to indexing-only (single responsibility)
- `POST /documents/search` gained an optional `source` filter
- Unit tests for filter correctness and full retrieval orchestration

Question Answering (Module 5, Sprint 6)

- `PromptBuilder` (`app/rag/prompts/`) — grounding instruction + source-labeled context + question, pure formatting
- `QuestionAnsweringService` (`answer`) — retrieves, applies `min_score` source selection, skips the LLM entirely when nothing qualifies
- `POST /ask` endpoint
- `FakeLLMProvider` test double, no real API calls in the suite
- Unit tests including the no-context short-circuit; live-verified against real OpenAI (grounded answer + correct refusal on an unrelated question)

Citations (Module 5, Sprint 7)

- `Citation` dataclass (source, score, snippet) — one per chunk used, not deduplicated by source
- `AskResponse.sources` replaced with `AskResponse.citations` (breaking change, no compatibility shim)
- `_snippet()` truncator; score explicitly documented as relevance, not correctness
- Live-verified: real similarity score and correctly truncated snippet in the API response

PDF Upload Pipeline (Out of Sequence — Medium Priority backlog fix)

- Fixed `PDFLoader` to properly implement `DocumentLoader` (previously didn't inherit it and used the wrong attribute name)
- Fixed the sync/async mismatch that crashed ingestion on every real PDF
- `ChunkingService.chunk_documents()` / `VectorStoreService.index_documents()` — indexing generalized to accept pre-loaded Documents, not just raw text
- `DocumentUploadService` (new) + `POST /documents/upload` — real multipart upload, testable via Swagger's file picker
- Live-verified: real PDF uploaded via HTTP, ingested, indexed, and successfully queried through `/ask`

Evaluation (Module 5, Sprint 8 — final sprint of Module 5)

- `EvaluationService.evaluate_retrieval()` — recall/precision against labeled (question, expected source) pairs, `POST /evaluate/retrieval`
- `AnswerResult.context` (new) — full untruncated chunk text kept alongside the truncated display citations, needed for faithfulness judging
- `FaithfulnessPromptBuilder` + `FaithfulnessService.evaluate()` — LLM-as-judge hallucination detection, `POST /evaluate/faithfulness`; reuses `QuestionAnsweringService`'s no-context short-circuit (trivially faithful if the LLM was never called)
- Defensive JSON parsing of the judge's verdict (strips code fences; reports `is_faithful: null` rather than guessing on malformed output) — an explicitly documented limitation, not a guaranteed schema
- Live-verified: real retrieval evaluation correctly flagged a deliberately mislabeled test case; real faithfulness judging correctly passed a genuinely grounded answer

Agent Architecture (Module 6, Sprint 1)

- `Tool` interface (`app/tools/tool.py`) — name, description, JSON-Schema parameters, async `execute()`
- `LLMProvider.chat_with_tools()` / `tool_result_messages()` — OpenAI Responses API tool-calling, kept behind the provider boundary so business logic never sees OpenAI's wire format
- `AgentService` — ReAct-style loop (call model → execute requested tool → feed result back → repeat), bounded by a `max_iterations` guard; unknown tool names fed back as a recoverable error instead of crashing
- `KnowledgeBaseSearchTool` — wraps `RetrievalService` as the agent's first real tool
- `POST /agents/chat`
- Live-verified: a direct question answered without a tool call; a question about a freshly indexed document correctly triggered the knowledge-base tool and produced a grounded answer

Planning (Module 6, Sprint 2)

- `app/agents/` layer created (first use) — `Plan` / `PlanStep`, strict-schema Pydantic models
- `LLMProvider.generate_structured()` — OpenAI JSON-Schema–constrained structured output; a more robust alternative to `FaithfulnessService`'s prompt-instructed JSON parsing
- `Planner` — turns a goal into an ordered `Plan`, filling `goal` in from the caller rather than trusting the model to echo it back
- `PlanningService` — runs the plan step by step through `AgentService` (each step keeps tool access, and sees prior steps' results), then synthesizes one final answer
- `POST /agents/plan`
- Live-verified against a real indexed document: correct step decomposition, correct per-step retrieval, accurate synthesized answer

Reflection (Module 6, Sprint 3)

- `Critique` — `is_satisfactory` / `feedback`, strict-schema model
- `Reflector` — critiques a candidate answer via `generate_structured()` (no new provider capability needed)
- `ReflectionService` — generate → critique → revise loop on `AgentService`, bounded by `max_iterations`; unlike the tool loop, hitting the cap returns a best-effort answer instead of raising
- `POST /agents/reflect` — returns the final answer plus every draft and its critique
- Live-verified against the real OpenAI API (both test questions were judged satisfactory on the first draft; the revision branch is deterministically covered by unit tests)

---

# Design Decisions

Layer-based architecture.

LangChain is isolated within the RAG layer.

Use official OpenAI SDK.

Use FastAPI Dependency Injection.

One responsibility per class.

Thin routers.

Async throughout.

No framework-specific code inside routers.

---

# Current Objective

Continue Module 6 – AI Agents.

Sprints 1–3 (Agent Architecture, Planning, Reflection) are complete. Next step: scope Sprint 4 (Memory) the same way every prior sprint was — a concept walkthrough and a concrete increment plan before any code changes.

Not yet decided: whether to close out the remaining Medium Priority backlog (DOCX/HTML/Markdown loaders) first.

---

# Upcoming Milestones

## Module 5 (Complete)

1. ~~LangChain Documents~~ ✅
2. ~~Recursive Text Splitter~~ ✅
3. ~~Embeddings~~ ✅
4. ~~Vector Store~~ ✅
5. ~~Retriever~~ ✅
6. ~~Question Answering~~ ✅
7. ~~Source Citations~~ ✅
8. ~~Evaluation~~ ✅

## Module 6 (Current — Sprints 1–3 complete)

- ~~Agent Architecture~~ ✅
- ~~Planning~~ ✅
- ~~Reflection~~ ✅
- Memory (not yet scoped)
- Multi-Agent Collaboration (not yet scoped)
- LangGraph (deliberately deferred to Sprint 5)
- State Management (folded into the LangGraph sprint)

---

# Long-Term Goal

Deliver a production-ready Enterprise AI Assistant capable of:

- Chat
- Enterprise RAG
- Agents
- Tool Calling
- MCP
- Evaluation
- AWS Deployment

This repository should represent production-quality AI Engineering work suitable for a professional portfolio.

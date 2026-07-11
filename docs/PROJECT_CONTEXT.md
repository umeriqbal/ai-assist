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

Module 5 – Enterprise RAG

Current Sprint:

Sprint 7 – Citations

Current Increment:

Increment 1 – Structured Citations

Status:

Sprint 6 (Question Answering) complete. Ready to begin citations.

---

# Bootcamp Modules

| Module | Status |
|---------|--------|
| Module 1 - LLM Fundamentals | Complete |
| Module 2 - Prompt Engineering | Complete |
| Module 3 - Semantic Search | Complete |
| Module 4 - Enterprise AI Platform | Complete |
| Module 5 - Enterprise RAG | Current |
| Module 6 - AI Agents | Pending |
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

Continue Module 5, Sprint 7.

Implement structured citations: replace `AskResponse.sources: list[str]` with per-chunk `Citation` objects (source, score, snippet), derived from the same `ScoredChunk`s already used to answer.

---

# Upcoming Milestones

1. ~~LangChain Documents~~ ✅ Complete
2. ~~Recursive Text Splitter~~ ✅ Complete
3. ~~Embeddings~~ ✅ Complete
4. ~~Vector Store~~ ✅ Complete
5. ~~Retriever~~ ✅ Complete
6. ~~Question Answering~~ ✅ Complete
7. Source Citations ← current
8. PostgreSQL + pgvector
9. Hybrid Search
10. Evaluation

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

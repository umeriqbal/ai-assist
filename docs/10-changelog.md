# Changelog

All notable changes to the Enterprise AI Assistant project are documented in this file.

The format follows the principles of Keep a Changelog.

---

# [0.5.0] - Current Development

## Module 5 - Enterprise RAG

**Status:** 🚧 In Progress

### Added — Sprint 6: Question Answering (Complete)

- `PromptBuilder` (new, `app/rag/prompts/prompt_builder.py`) — pure formatting: grounding instruction, source-labeled context, and question, no network calls
- `QuestionAnsweringService` (`answer`) — retrieves via `RetrievalService`, applies optional `min_score` source selection, skips the LLM call entirely when no chunk qualifies
- `POST /ask` endpoint
- `FakeLLMProvider` test double added alongside `FakeEmbeddingModel` — no real API calls in the automated suite
- Unit tests for prompt formatting and full answer orchestration, including an explicit assertion that the LLM is never called without sufficient context
- Live-verified against the real OpenAI API: a real indexed policy question answered correctly and grounded; an unrelated question correctly refused instead of hallucinated

### Added — Sprint 5: Retrieval (Complete)

- `VectorStore.similarity_search` gained `metadata_filter`, applied before ranking so filtered top-k is always correct (`app/rag/stores/vector_store.py`, `in_memory_vector_store.py`)
- `RetrievalService` (new) — owns the read path: validates query, embeds it, applies the metadata filter
- `VectorStoreService` trimmed to indexing-only; `search()` removed (single responsibility restored)
- `POST /documents/search` gained an optional `source` field to filter results (same endpoint, extended request)
- Unit tests for filter correctness (excludes non-matching sources, filters before ranking rather than after) and full retrieval orchestration

### Added — Sprint 4: Vector Storage (Complete)

- `VectorStore` interface reworked to operate on `EmbeddedChunk` / query vectors, returning `ScoredChunk` (`app/rag/stores/vector_store.py`)
- `InMemoryVectorStore` — brute-force cosine similarity search, pure Python, no new dependency
- `VectorStoreService` (`index_text`, `search`), reusing `ChunkingService` and `EmbeddingService`
- `POST /documents/index` and `POST /documents/search` endpoints
- Removed the broken, docs-contradicting `ChromaVectorStore` and the `langchain-chroma` dependency (Decision 015 reaffirmed: no dedicated vector DB, pgvector later)
- Unit tests for cosine similarity correctness (identical/orthogonal vectors, top-k ordering) and full index→search orchestration

### Added — Sprint 3: Embeddings (Complete)

- `EmbeddingModel` interface redefined as plain-Python async methods, so no LangChain type leaks out of `app/rag/`
- `OpenAIEmbeddingModel` (fixed from a broken, misnamed draft — `OpenAIEmbeddingProvider` didn't match what its own factory imported), batches all chunk texts into a single API call
- `EmbeddingService` (`embed_chunks`, `embed_query`), wired into Dependency Injection
- `POST /documents/embeddings` endpoint
- Unit tests using a fake embedding model — no real API calls in the automated suite

### Added — Sprint 2: Chunking (Complete)

- `RecursiveDocumentSplitter` extended with `add_start_index` and `chunk_index` / `chunk_count` metadata (`app/rag/splitters/recursive_splitter.py`)
- `ChunkingService`, reusing `DocumentService` to build the base `Document` before splitting
- `ChunkingService` wired into Dependency Injection (`get_chunking_service`)
- `POST /documents/chunks` endpoint (configurable `chunk_size` / `chunk_overlap`, thin router, converts `ValueError` to `400`)
- Unit tests for `ChunkingService` (multi-chunk splitting, single-chunk short text, empty-text rejection, invalid overlap rejection)

### Added — Sprint 1: LangChain Foundations (Complete)

- `DocumentFactory`, producing LangChain `Document` objects (`app/rag/document_factory.py`)
- `DocumentService`, validating and enriching text with metadata (`source`, `created_at`)
- `DocumentService` wired into Dependency Injection (`get_document_service`)
- `POST /documents` endpoint (thin router, converts `ValueError` to `400`)
- Unit tests for `DocumentService` (valid text, whitespace stripping, empty-text rejection) — first test suite in the repository

### Planned

- Structured source citations (score, snippet)

---

# [0.4.0] - Enterprise AI Platform

**Status:** ✅ Complete

## Added

### Architecture

- Layer-based architecture
- Application factory
- Dependency Injection
- Provider pattern
- Service layer
- Async architecture

### Configuration

- Environment configuration
- Pydantic Settings
- Structured configuration management

### Logging

- Structured logging
- Configurable log levels

### Health

Added health endpoints

```
GET /
GET /health
GET /live
GET /ready
GET /chat/health
```

### AI

Implemented

- ChatService
- StreamingService
- LLMProvider
- OpenAIProvider

### API

Added

```
POST /chat
POST /chat/stream
```

### Streaming

Implemented

- Provider streaming
- Streaming service
- Streaming API endpoint

---

# [0.3.0] - Semantic Search

**Status:** ✅ Complete

## Added

### Embeddings

Implemented semantic embeddings.

### Vector Search

Implemented

- In-memory vector store
- Cosine similarity
- Ranking
- Search pipeline

### Chunking

Implemented

- Chunk creation
- Chunk overlap
- Context management

### Search

Built a semantic search engine from first principles without external frameworks.

---

# [0.2.0] - Prompt Engineering

**Status:** ✅ Complete

## Added

### Prompt Playground

Implemented

- Prompt templates
- Prompt chaining
- Structured prompts

### Responses API

Integrated OpenAI Responses API.

### Structured Outputs

Added

- JSON responses
- Pydantic validation
- Reliable parsing

### FastAPI

Integrated prompts into FastAPI endpoints.

---

# [0.1.0] - LLM Fundamentals

**Status:** ✅ Complete

## Added

Studied

- Tokens
- Context windows
- Prompt structure
- Temperature
- Hallucinations
- Cost calculation
- Roles
- Responses API basics

Built the first OpenAI-powered application.

---

# Upcoming Releases

## Version 0.6.0

### Planned

Enterprise RAG

Expected features

- PDF upload
- DOCX upload
- HTML ingestion
- Markdown ingestion
- Structured source citations

---

## Version 0.7.0

### Planned

AI Agents

Expected features

- Planning
- Reflection
- Memory
- Multi-agent workflows
- LangGraph

---

## Version 0.8.0

### Planned

MCP

Expected features

- MCP Server
- MCP Client
- Tool discovery
- Remote tools

---

## Version 0.9.0

### Planned

Production Infrastructure

Expected features

- Docker
- PostgreSQL
- pgvector
- Terraform
- AWS deployment
- CI/CD

---

## Version 1.0.0

### Planned

Enterprise AI Assistant

Expected features

- Enterprise Chat
- Knowledge Base
- Website Crawling
- AI Agents
- MCP
- Tool Calling
- Evaluation Dashboard
- Production Deployment

---

# Milestones

| Version | Milestone | Status |
|----------|-----------|--------|
| 0.1.0 | LLM Fundamentals | ✅ |
| 0.2.0 | Prompt Engineering | ✅ |
| 0.3.0 | Semantic Search | ✅ |
| 0.4.0 | Enterprise AI Platform | ✅ |
| 0.5.0 | Enterprise RAG | 🚧 |
| 0.6.0 | AI Agents | ⏳ |
| 0.7.0 | MCP | ⏳ |
| 0.8.0 | Infrastructure | ⏳ |
| 0.9.0 | Evaluation | ⏳ |
| 1.0.0 | Enterprise AI Assistant | ⏳ |

---

# Project Statistics

Current Status

- Modules Completed: 4 / 10
- Current Module: 5
- Architecture: Stable
- Documentation: Complete
- Production Readiness: Strong foundation established

---

# Documentation Policy

At the end of every completed sprint:

- Update this changelog.
- Record new features.
- Record architectural changes.
- Record breaking changes (if any).
- Increment the project version where appropriate.

This file provides a historical record of the project's evolution and should always reflect the current state of the codebase.
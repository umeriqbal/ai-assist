# Changelog

All notable changes to the Enterprise AI Assistant project are documented in this file.

The format follows the principles of Keep a Changelog.

---

# [0.6.0] - AI Agents

**Status:** 🚧 In Progress

### Added — Sprint 2: Planning (Complete)

- `app/agents/` layer created (first use) — planning building blocks, mirroring how `rag/` holds RAG building blocks
- `Plan` / `PlanStep` (new, `app/agents/plan.py`) — Pydantic models with `extra="forbid"`, so their generated JSON Schema includes `additionalProperties: false` at every level, required for OpenAI's strict structured-output mode
- `LLMProvider.generate_structured()` (new abstract method) — returns a JSON object constrained to a given JSON Schema instead of free text; `OpenAIProvider` implements it via the Responses API's `text.format` (`type: json_schema`, `strict: true`). A more robust alternative to `FaithfulnessService`'s prompt-instructed JSON parsing (flagged in Known Technical Debt) — retrofitting `FaithfulnessService` onto it is optional, not done here
- `Planner` (new, `app/agents/planner.py`) — turns a goal into an ordered `Plan` via `generate_structured()`; only asks the model for `steps`, fills `goal` in from the caller's input rather than trusting the model to echo it back verbatim
- `PlanningService` (new, `app/services/planning_service.py`) — runs a plan step by step through the Sprint 1 `AgentService` (each step still has tool access), passing prior steps' results into each subsequent step's prompt, then makes one final `LLMProvider.chat()` call to synthesize a coherent answer from all step results; short-circuits to a direct answer when the model decides a goal needs no steps
- `POST /agents/plan` endpoint — returns the plan, each step's raw result, and the final answer
- `FakeLLMProvider` extended with a scriptable `generate_structured()`, without changing behavior for tests using only `chat()` / `chat_with_tools()`
- Unit tests: structured-output contract via the fake, `Planner` (goal/steps parsing, goal preserved over model divergence, empty-goal rejection), `PlanningService` (multi-step execution + synthesis, no-steps shortcut, later steps see earlier results)
- Live-verified against the real OpenAI API and a real indexed document: the plan correctly decomposed a two-part question into steps, each step correctly retrieved/reused the relevant fact via the knowledge-base tool, and the synthesized final answer was accurate

### Added — Sprint 1: Agent Architecture (Complete)

- `Tool` interface (`app/tools/tool.py`) — `name`, `description`, JSON-Schema `parameters`, async `execute()`
- `EchoTool` (new) — trivial concrete implementation, exists purely to validate the `Tool` contract before anything depends on it
- `LLMProvider.chat_with_tools()` (new abstract method) — sends a conversation + available tools, returns a `ChatResult` (final text, requested tool calls, or both); additive, `chat()`/`stream_chat()` untouched
- `LLMProvider.tool_result_messages()` (new abstract method) — translates a tool call + its result into provider-specific wire format, keeping OpenAI's Responses API `function_call`/`function_call_output` item shape out of business logic (Provider Pattern boundary, Decision 004)
- `ChatResult` / `ToolCall` dataclasses (`app/providers/`)
- `OpenAIProvider.chat_with_tools()` / `.tool_result_messages()` — implemented via the Responses API's `tools` parameter, same API already used by `chat`/`stream_chat`
- `AgentService` (new, `app/services/agent_service.py`) — the ReAct-style loop: call the model, execute any requested tool, feed the result back, repeat; bounded by a `max_iterations` guard (default 5, raises rather than looping forever); an unrecognized tool name is fed back to the model as an error string instead of crashing the request
- `KnowledgeBaseSearchTool` (new, `app/tools/`) — wraps `RetrievalService` as the agent's first real tool, reusing Module 5's retrieval pipeline instead of a toy example
- `POST /agents/chat` endpoint
- `FakeLLMProvider` test double extended with a scriptable `chat_with_tools()` (queued `ChatResult`s) and `tool_result_messages()`, without changing behavior for any test still using only `chat()`
- Unit tests: `Tool`/`EchoTool` contract, provider tool-calling contract via the fake, agent loop (no-tool path, tool round-trip, unknown-tool fallback, iteration-limit guard), `KnowledgeBaseSearchTool` (declared schema, matching-query retrieval, no-results case)
- Live-verified against the real OpenAI API: a plain question answered directly with no tool call; a question about a freshly indexed document correctly triggered `search_knowledge_base` and produced a grounded answer
- Removed a stray, empty `app/agents/tools/` scaffold folder that duplicated `app/tools/`; `app/agents/` itself intentionally left uncreated until planning/memory/multi-agent orchestration (Sprints 2+) needs a home distinct from a plain service

### Not Included

- Reflection, Memory, LangGraph/State Management, Multi-Agent Collaboration (Sprints 3–6, not yet scoped) — LangGraph is deliberately deferred to Sprint 5 rather than introduced in Sprint 1, so the hand-built loop above is understood before a framework manages it

---

# [0.5.0] - Enterprise RAG

**Status:** ✅ Complete

### Added — Sprint 8: Evaluation (Complete)

- `EvaluationService.evaluate_retrieval()` — recall/precision against labeled (question, expected source) pairs, run through `RetrievalService` with no retrieval logic duplicated
- `POST /evaluate/retrieval` endpoint
- `AnswerResult.context` (new) — full untruncated chunk text kept alongside the truncated display citations, needed for faithfulness judging without risking false negatives from truncation
- `FaithfulnessPromptBuilder` (new, `app/rag/prompts/`) — pure formatting, instructs an LLM judge to respond with strict JSON
- `FaithfulnessService.evaluate()` — LLM-as-judge hallucination detection; reuses `QuestionAnsweringService`'s no-context short-circuit (trivially faithful when the LLM was never called); defensive JSON parsing (strips code fences, reports `is_faithful: null` rather than guessing on malformed output — an explicitly documented limitation, not a guaranteed schema)
- `POST /evaluate/faithfulness` endpoint
- Unit tests: perfect/missed/noisy retrieval scoring, mean aggregation, zero-division edge case; faithful/unfaithful/malformed/code-fenced judge responses, no-context short-circuit
- Live-verified: real retrieval evaluation correctly flagged a deliberately mislabeled test case (not just confirmed correct ones); real faithfulness judging correctly passed a genuinely grounded answer end to end

### Added — Sprint 7: Citations (Complete)

- `Citation` dataclass (`source`, `score`, `snippet`) — score explicitly documented as a relevance signal, not a measure of answer correctness
- `AnswerResult.sources: list[str]` replaced with `citations: list[Citation]`, one per chunk actually used (not deduplicated by source, so multiple passages from the same document each get their own citation)
- `_snippet()` truncator (200 chars, ellipsis) for readable citation previews
- `AskResponse.citations` — breaking change from the old flat `sources` field (no compatibility shim; nothing else depended on the old shape)
- Unit tests for citation content and snippet truncation
- Live-verified against the real OpenAI API: citation carried a real similarity score and a correctly truncated snippet

### Fixed — PDF Upload Pipeline (Out of Sequence)

Pulled forward from the Medium Priority backlog ("PDF Loader") so real files could be tested end-to-end, ahead of Sprint 8.

- `PDFLoader` now properly implements the `DocumentLoader` interface — it previously didn't inherit it at all and exposed the wrong attribute name (`SUPPORTED_EXTENSIONS` instead of `supported_extensions`); `loader_factory.py` had been silently patched at some point to check the wrong name rather than the loader being fixed
- Fixed the sync/async mismatch that made `DocumentIngestionService.ingest()` raise `TypeError` on every real (non-empty) PDF; `PDFLoader.load()` is now async, using `asyncio.to_thread` for the blocking parse
- `ChunkingService.chunk_documents()` and `VectorStoreService.index_documents()` (new) — generalized indexing to accept pre-loaded `Document`s, not just raw text, reusable by future DOCX/HTML/Markdown loaders
- `DocumentUploadService` (new) — ingests a file, stamps `source`/`created_at`, indexes it, while preserving PyPDFLoader's own `page`/`total_pages` metadata (unlocks page-level citations later)
- `POST /documents/upload` — real multipart file upload endpoint, testable directly through Swagger's auto-generated file picker
- Installed and declared the missing `python-multipart` dependency (required by FastAPI for file uploads)
- Unit tests using a hand-crafted minimal PDF fixture (no new test dependency required)
- Live-verified via real HTTP multipart upload: a real PDF uploaded, ingested, indexed, and successfully queried through `/ask`

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

### Not Included

- DOCX/HTML/Markdown loaders (Medium Priority backlog, never built — only PDF and raw text ingestion work)
- PostgreSQL + pgvector (the in-memory vector store remains process-local and non-persistent by design; deferred to a later milestone per Decision 015)

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

## Remainder of 0.6.0 - AI Agents

### Planned (Sprints 3–6, not yet scoped)

- Reflection
- Memory
- LangGraph + State Management
- Multi-Agent Collaboration

### Carried over from 0.5.0 (not blocking)

- DOCX upload
- HTML ingestion
- Markdown ingestion

---

## Version 0.7.0

### Planned

Model Context Protocol (MCP)

Expected features

- MCP Server
- MCP Client
- Tool discovery
- Remote tools

---

## Version 0.8.0

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

## Version 0.9.0

### Planned

Evaluation & Observability

Expected features

- Offline/online evaluation
- Cost tracking
- Latency monitoring
- Token usage
- Prompt versioning
- Model comparison

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
| 0.5.0 | Enterprise RAG | ✅ |
| 0.6.0 | AI Agents | 🚧 |
| 0.7.0 | MCP | ⏳ |
| 0.8.0 | Infrastructure | ⏳ |
| 0.9.0 | Evaluation | ⏳ |
| 1.0.0 | Enterprise AI Assistant | ⏳ |

---

# Project Statistics

Current Status

- Modules Completed: 5 / 10
- Current Module: 6 (Sprints 1–2 of ~6 complete)
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
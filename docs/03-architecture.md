# System Architecture

> This document defines the official architecture of the Enterprise AI Assistant.

This architecture is the single source of truth for the project.

---

# Architecture Goals

The architecture is designed to be:

- Maintainable
- Testable
- Extensible
- Production Ready
- Framework Independent where possible

The application follows a layered architecture with clear separation of responsibilities.

---

# High-Level Architecture

```
                    Client
                       │
                       ▼
                 FastAPI Router
                       │
                       ▼
                   Service Layer
                       │
                       ▼
                 Provider Layer
                       │
                       ▼
               External AI Services
```

Each layer has exactly one responsibility.

---

# Layer Responsibilities

## API Layer

Location

```
app/api/
```

Responsibilities

- HTTP endpoints
- Request validation
- Response formatting
- Status codes
- Authentication (future)

Must NOT contain

- Business logic
- OpenAI SDK
- LangChain
- Database queries

---

## Service Layer

Location

```
app/services/
```

Responsibilities

- Business logic
- Orchestration
- Validation
- Workflows
- AI coordination

Must NOT contain

- HTTP
- SQL
- FastAPI routing

---

## Provider Layer

Location

```
app/providers/
```

Responsibilities

- External SDK communication
- OpenAI
- Anthropic
- Bedrock
- Ollama

Must NOT contain

- Business logic
- HTTP
- Prompt construction

---

## Core Layer

Location

```
app/core/
```

Responsibilities

- Configuration
- Logging
- Application Factory
- Security
- Startup configuration

---

## Dependency Layer

Location

```
app/dependencies/
```

Responsibilities

- FastAPI dependency injection
- Object creation
- Singleton management

---

## Schema Layer

Location

```
app/schemas/
```

Responsibilities

- Request models
- Response models
- Validation
- API contracts

---

## Database Layer

Location

```
app/database/
```

Responsibilities

- Persistence
- SQLAlchemy
- PostgreSQL
- pgvector
- Repositories (future)

---

## RAG Layer

Location

```
app/rag/
```

Responsibilities

- Document loading
- Chunking
- Embeddings
- Retrieval
- Prompt construction
- Citations

LangChain exists only inside this layer.

---

## Agent Layer

Location

```
app/agents/
```

Responsibilities

- Planning
- Memory
- Reflection
- Multi-agent orchestration
- LangGraph

---

## Tools Layer

Location

```
app/tools/
```

Responsibilities

- Tool calling
- MCP integration
- External systems
- Search
- Calculator
- GitHub
- Filesystem

---

# Request Flow

Every HTTP request follows this path.

```
Client

↓

FastAPI Router

↓

Service

↓

Provider

↓

External SDK

↓

LLM

↓

Provider

↓

Service

↓

Router

↓

Client
```

No layer may skip another.

For example:

❌ Router → OpenAI

❌ Router → Database

❌ Router → LangChain

These are architecture violations.

---

# Current Chat Flow

```
POST /chat

↓

Chat Router

↓

ChatService

↓

LLMProvider

↓

OpenAIProvider

↓

OpenAI Responses API

↓

Response
```

---

# Streaming Flow

```
POST /chat/stream

↓

Streaming Router

↓

StreamingService

↓

LLMProvider

↓

OpenAI Stream

↓

StreamingResponse

↓

Browser
```

---

# Future RAG Flow

```
Upload PDF

↓

Document Loader

↓

LangChain Document

↓

Text Splitter

↓

Chunks

↓

Embeddings

↓

Vector Store

↓

Retriever

↓

Prompt Builder

↓

LLM Provider

↓

Answer

↓

Citation Service

↓

Client
```

---

# Current Agent Flow

```
POST /agents/chat

↓

Agent Router

↓

AgentService (ReAct loop)

↓

LLMProvider.chat_with_tools()

↓

Has tool calls? ── no ──→ Final Answer
       │
      yes
       ↓
   Tool.execute()
       │
       ↓
LLMProvider.tool_result_messages()
       │
       └──→ back into the loop
```

Single agent, one tool so far (`KnowledgeBaseSearchTool`, wrapping `RetrievalService`). Bounded by a max-iteration guard; an unrecognized tool name is fed back to the model as an error instead of crashing the request.

---

# Current Plan-and-Execute Flow

```
POST /agents/plan

↓

Agent Router

↓

PlanningService

↓

Planner ──→ LLMProvider.generate_structured() ──→ Plan (goal + ordered steps)

↓

for each step:

   AgentService.chat(step + prior results)   (Current Agent Flow, above)

       ↓

   step result

↓

LLMProvider.chat()  (synthesis: goal + all step results → final answer)

↓

Plan + step results + final answer
```

Steps execute sequentially, not in parallel — each step's prompt includes every prior step's result, so later steps can build on earlier ones. If the model decides a goal needs no steps, `PlanningService` short-circuits straight to a direct answer instead of running an empty plan through a pointless synthesis call.

`Planner` lives in `app/agents/` (the first component in that layer) since it's a planning building block; `PlanningService` lives in `app/services/` since it's the orchestrating business service that composes `Planner` + `AgentService` for router/DI use — the same split as `rag/` (building blocks) vs. `services/` (orchestration) in the RAG layer.

---

# Current Reflection Flow

```
POST /agents/reflect

↓

Agent Router

↓

ReflectionService

↓

AgentService.chat()  (initial answer — Current Agent Flow, above)

↓

┌──────────────────────────────────┐
│  Reflector.critique()            │
│  (LLMProvider.generate_structured)│
└──────────────────────────────────┘

↓

Satisfactory? ── yes ──→ Final Answer + Drafts
       │
       no
       ↓
AgentService.chat()  (revise, using the critique feedback)
       │
       └──→ back into the loop (bounded by max_iterations)
```

`Reflector` lives in `app/agents/`, alongside `Planner` — another planning/reasoning building block, not a business service. `ReflectionService` composes it with `AgentService`, same split as `PlanningService`. No new provider capability was needed: `generate_structured()` (Sprint 2) already covers the critique step.

---

# Current Memory Flow

```
POST /agents/chat  { prompt, conversation_id? }

↓

Agent Router  (generates a conversation_id if the caller omitted one)

↓

AgentService.chat(prompt, conversation_id)

↓

ConversationMemory.get_history(conversation_id)  ──→  prior turns

↓

messages = prior turns + new user message

↓

(Current Agent Flow, above — unchanged)

↓

final answer

↓

ConversationMemory.append_turn(conversation_id, prompt, answer)

↓

response + conversation_id
```

Only the human-visible exchange (user message, final answer) is stored — not the tool-call round-trips that happen mid-turn inside the ReAct loop. `ConversationMemory` lives in `app/agents/` (a building block, like `Planner`/`Reflector`); `InMemoryConversationMemory` is process-local and non-persistent by design, the same trade-off `InMemoryVectorStore` made, behind an interface ready to swap for Redis or PostgreSQL later.

---

# Future Agent Flow

```
User Request

↓

Planner Agent

↓

Task Breakdown

↓

Specialist Agents

↓

Tool Calls

↓

Results

↓

Reviewer Agent

↓

Final Answer
```

Introduced across Sprints 2–6 (Planning, Reflection, Memory, LangGraph/State Management, Multi-Agent Collaboration), building on the Current Agent Flow above rather than replacing it.

---

# Dependency Injection

Object creation is centralised.

```
Router

↓

Depends()

↓

Service

↓

Provider

↓

SDK
```

Objects are never instantiated directly inside routers.

Example

Correct

```
ChatService

↓

Depends(get_chat_service)
```

Incorrect

```
service = ChatService(...)
```

inside a router.

---

# Provider Pattern

Business logic depends on abstractions.

```
ChatService

↓

LLMProvider

↓

OpenAIProvider
```

Future providers

```
LLMProvider

├── OpenAIProvider

├── AnthropicProvider

├── BedrockProvider

├── OllamaProvider
```

No service should know which provider is being used.

---

# Service Pattern

Every service has one responsibility.

Current

- ChatService
- StreamingService
- DocumentService
- ChunkingService
- EmbeddingService
- VectorStoreService
- RetrievalService
- QuestionAnsweringService
- EvaluationService
- FaithfulnessService
- AgentService
- PlanningService
- ReflectionService

Future

- PromptService
- CitationService

Services collaborate rather than becoming large monolithic classes.

---

# Design Principles

The project follows:

- SOLID
- DRY
- Separation of Concerns
- Dependency Injection
- Composition over Inheritance
- Async First
- Strong Typing
- Explicit Interfaces

---

# Architecture Rules

The following rules are mandatory.

1. Routers remain thin.
2. Business logic belongs in services.
3. Providers wrap external SDKs.
4. LangChain stays inside the RAG layer.
5. OpenAI SDK is never used outside providers.
6. Services communicate through abstractions.
7. Configuration comes from `Settings`.
8. Pydantic validates all external input.
9. No hard-coded secrets.
10. One responsibility per class.

---

# Future Evolution

The architecture is expected to grow without major restructuring.

Upcoming additions include:

```
RAG

↓

Document Processing

↓

Embeddings

↓

Vector Database

↓

Hybrid Search

↓

Re-ranking

↓

Agents

↓

Tool Calling

↓

MCP

↓

Evaluation

↓

Deployment
```

The layered architecture should remain unchanged throughout the project.

---

# Architectural Success Criteria

A new feature is considered well-designed if:

- It fits into an existing layer.
- It does not introduce unnecessary coupling.
- It follows dependency inversion.
- It is independently testable.
- It can be replaced without affecting higher layers.

These principles guide every implementation throughout the bootcamp.
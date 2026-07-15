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
- External systems
- Search
- Calculator
- GitHub
- Filesystem

---

## MCP Layer

Location

```
app/mcp/
```

Responsibilities

- MCP server(s) — exposing this project's own `Tool` instances over the Model Context Protocol
- MCP client(s) — discovering and consuming tools from external MCP servers

The `mcp` SDK exists only inside this layer, the same isolation principle Decision 013 gives LangChain in `app/rag/` and that was extended to LangGraph in `app/agents/`. Nothing outside `app/mcp/` imports `mcp` directly — `build_mcp_server()` takes plain `Tool` instances and adapts them, so `app/tools/` stays protocol-agnostic.

---

## Frontend Layer

Location

```
frontend/
```

(Repo root, sibling to `backend/` — not inside the backend app at all.)

Responsibilities

- Everything a user or admin directly sees and interacts with: chat UI (Sprint 2, live), knowledge base management, agent screens, evaluation dashboard (later sprints)
- Calls the backend exclusively over HTTP (`fetch()`), same as any external API consumer — no shared code, no shared process, no privileged access

Plain HTML/CSS/JS, no framework, no build tooling — a deliberate Module 10 decision (React/Vue/Svelte all considered), consistent with this project's habit of understanding a layer by hand before reaching for a framework. Talks to the backend across a real origin boundary, enforced by `CORSMiddleware` naming the frontend's exact origin — the first place in this project where that boundary exists at all.

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

# Current LangGraph Flow

```
POST /agents/graph-chat  { prompt, conversation_id? }

↓

Agent Router  (generates a conversation_id if omitted)

↓

AgentGraphService.chat(prompt, conversation_id)

↓

compiled StateGraph.ainvoke(..., thread_id=conversation_id)

↓

┌─────────────────────────────────────────────┐
│  call_model node                             │
│    → LLMProvider.chat_with_tools()           │  same calls
│                                               │  AgentService
│  call_tools node                             │  already makes
│    → Tool.execute()                          │
│    → LLMProvider.tool_result_messages()      │
└─────────────────────────────────────────────┘

↓  (conditional edge: tool calls pending? loop back : end)

MemorySaver checkpointer persists/reloads `messages`
keyed by conversation_id — replaces ConversationMemory
for this path

↓

final answer + conversation_id
```

This is a direct re-expression of the Current Agent Flow above: the same `LLMProvider`/`Tool` calls, the same conditional "loop or stop" logic — just as graph nodes and a conditional edge instead of a hand-written `for` loop, and a checkpointer instead of a hand-rolled memory store. `AgentGraphService`/`agent_graph.py` are entirely separate from `AgentService`/`ConversationMemory` — `POST /agents/chat` (hand-built) and `POST /agents/graph-chat` (LangGraph) are two independent implementations of the same capability, kept side by side for comparison rather than one replacing the other. LangGraph is confined to `app/agents/`, the same isolation Decision 013 already applies to LangChain in `app/rag/` — nodes never use a LangChain chat model or LangChain message types, only the project's own provider/tool abstractions.

Known asymmetry, not yet reconciled: `MemorySaver` persists the *entire* graph state per turn (including intermediate tool-call round-trips), while `ConversationMemory` deliberately stores only the human-visible exchange. A `conversation_id` from one endpoint is meaningless to the other.

---

# Current Multi-Agent Flow

```
POST /agents/collaborate  { prompt }

↓

Agent Router

↓

MultiAgentService.run(prompt)

↓

compiled StateGraph.ainvoke(...)

↓

┌──────────────────────────────────────────┐
│  supervisor node                          │
│    → Supervisor.decide(messages)          │
│    → LLMProvider.generate_structured()    │
│    → { next, instructions }               │
└──────────────────────────────────────────┘

↓  conditional edge on `next`

  ┌─────────────┐         ┌─────────────┐
  │ researcher  │         │   writer    │
  │ (AgentService│        │ (AgentService│
  │  + KB tool)  │        │  no tools)   │
  └─────────────┘         └─────────────┘
        │                        │
        └──────────┬─────────────┘
                    ↓
             back to supervisor
                    │
              next == "finish"
                    ↓
      final answer + full transcript
```

This is the "Planner/Supervisor → Specialist Agents → Final Answer" idea this document sketched before Module 6 began — realized with two concrete specialists (Researcher, Writer) rather than an open-ended set, and no separate "Reviewer Agent": self-critique already exists as its own capability (`ReflectionService`, Sprint 3) and wasn't duplicated here. Each specialist is an ordinary `AgentService` instance — Sprint 6 added an optional `system_prompt` so an agent can have a role, not a new "specialist" class. The Supervisor routes via `generate_structured()` (Sprint 2's mechanism, reused a third time), and orchestration follows the exact graph pattern `agent_graph.py` established in Sprint 5 — a conditional edge and node-per-worker, just with more than one worker node this time. No checkpointer: this endpoint deliberately has no cross-call memory (Sprints 4–5 already covered that ground).

---

# Current MCP Server Flow

```
MCP Client (e.g. our own Sprint 2 client, or Claude Desktop)

↓  spawns / connects over stdio

app/mcp/run_server.py

↓

build_mcp_server(name, tools=[EchoTool(), KnowledgeBaseSearchTool()])

↓

low-level mcp.server.lowlevel.Server

├── list_tools()  →  [types.Tool(name, description, inputSchema=Tool.parameters)]
│
└── call_tool(name, arguments)  →  Tool.execute(**arguments)  →  types.TextContent
```

`Tool.parameters` (a hand-written JSON Schema, built in Module 6 Sprint 1) maps directly onto MCP's `inputSchema` — no adapter logic needed, confirmed with a smoke test before writing any production code. This is why the low-level `Server` API was used instead of `FastMCP`: `FastMCP`'s decorator infers a tool's schema from Python type hints, which would fight an already-explicit schema rather than reuse it. Live-verified by spawning `run_server.py` as a genuine subprocess and connecting a real client over stdio — not just an in-memory test harness.

---

# Current MCP Client Flow

```
connect_stdio_mcp_server(command="python", args=["-m", "app.mcp.run_server"])

↓  spawns the Sprint 1 server as a subprocess, over stdio

ClientSession (initialized)

↓

discover_tools(session)

↓

session.list_tools()  →  [types.Tool(name, description, inputSchema), ...]

↓  for each remote tool, with no names hard-coded anywhere in this code

MCPToolAdapter(session, name, description, parameters)  →  a plain `Tool`

↓

adapter.execute(**kwargs)  →  session.call_tool(name, kwargs)  →  joined text content
```

`MCPToolAdapter` is the mirror image of Sprint 1's server-side adaptation: instead of wrapping a local `Tool` to look like an MCP tool, it wraps a remote MCP tool to look like a local `Tool`. This is why the round trip works end to end without either side needing to know about the other's internals — `AgentService` can receive a list of `MCPToolAdapter` instances and use them exactly like `KnowledgeBaseSearchTool`, never knowing (or needing to know) that execution happens on another process. Remote tool errors surface as plain text (`CallToolResult.content`), not exceptions — consistent with how `AgentService` already treats "Error: ..." tool output as ordinary text, not a crash. Live-verified against the real Sprint 1 server: both tools discovered and executed correctly.

---

# Current Remote Execution Flow

```
Process 1: python -m app.mcp.run_http_server
    build_mcp_server(tools=[EchoTool(), KnowledgeBaseSearchTool()])
    → wrapped in a Starlette app (StreamableHTTPSessionManager)
    → served on its own port — a real network service, not a subprocess pipe

Process 2: uvicorn app.main:create_app --factory
    create_app()'s lifespan (new in Sprint 3):
        connect_http_mcp_server(settings.mcp_server_url)  →  ClientSession
        discover_tools(session)  →  list[Tool]  (no names hard-coded)
        app.state.mcp_agent_service = AgentService(provider, tools, memory)
        ── held open for the app's entire lifetime ──

    POST /agents/mcp-chat
        → get_mcp_agent_service(request)  →  request.app.state.mcp_agent_service
        → AgentService.chat(prompt, conversation_id)
        → (Current Agent Flow, as always) ── except a tool call now means
          a real HTTP request from Process 2 to Process 1 and back
```

The only thing that changed from the Current Agent Flow already documented above: some of `AgentService`'s tools now execute on a completely different process, reached over a real network boundary, instead of in-process. `AgentService` itself needed zero changes — it was never written to know or care where a tool's `execute()` actually runs.

**Why a `lifespan`, when nothing before this needed one:** every other DI singleton (`@lru_cache` functions in `dependencies/`) constructs lazily and synchronously on first access. Connecting to a network service and discovering its tools is genuine async setup that must happen once, at startup, and be torn down at shutdown — the first dependency in this project with a real connection lifecycle, not just a constructor call.

**Two independent processes, deliberately not merged:** the MCP server (tool provider) and the FastAPI app (agent) are separate services, mirroring a real remote-tool-provider architecture rather than embedding everything in one process. If the MCP server isn't running when the FastAPI app starts, startup fails clearly — there's no sensible fallback for "the tools this agent needs don't exist yet."

**Known limitation, confirmed live rather than just assumed:** the MCP server process and the FastAPI app process each hold their own in-memory vector store. A question requiring a document indexed via `POST /documents/index` correctly returned "no results" through `POST /agents/mcp-chat` — the remote call itself worked, the data just wasn't there. Not fixed in this sprint.

---

# Current Frontend Flow

```
frontend/  (plain HTML/CSS/JS, no build tooling, no framework)
    served independently — e.g. `python -m http.server 5500` from inside frontend/
    on its own origin (http://127.0.0.1:5500)

        js/main.js
            → apiGet("/health")   (js/api.js — shared fetch() wrapper)
            → fetch("http://127.0.0.1:8000/health")   ── cross-origin request ──

Backend (uvicorn, port 8000)
    CORSMiddleware(allow_origins=[settings.frontend_url])
        → request accepted only because the Origin header matches FRONTEND_URL
    GET /health  →  {status, timestamp, environment, version}

        ← response carries Access-Control-Allow-Origin: http://127.0.0.1:5500
    js/main.js renders the result into the DOM
```

This is the first client in the entire project that isn't same-origin with the backend. Every previous caller — curl, Swagger's UI (served by the backend itself), another Python process via `connect_http_mcp_server`/`connect_stdio_mcp_server` — never triggered a browser's CORS check, because CORS is a browser-enforced rule, not a server-side one; a server can be called from anywhere by curl or Python, but a browser refuses to expose a cross-origin response to page JavaScript unless the server explicitly allows it. `CORSMiddleware` is that explicit allowance — and it names one specific origin (`settings.frontend_url`), not `*`, matching this project's habit of not defaulting to permissive-because-it's-only-dev-for-now settings.

**Verification note:** no browser automation tool was available at first (`chromium-cli` doesn't exist in this environment, and no project run-skill covered launching this app yet). Playwright was already cached locally, so Sprint 1's verification used an ad hoc driver script — real headless Chromium, real `fetch()`, real CORS negotiation — rather than a curl-only simulation, which can only prove the server's headers are correct, not that a browser actually accepts them.

**Operational dependency worth naming:** getting this flow running requires three processes started in a specific order — `app.mcp.run_http_server` (Module 7's dependency, since `create_app()`'s `lifespan` requires it), then the FastAPI app, then the `frontend/` static server. No single command starts all three yet.

---

# Current Chat Flow (Module 10, Sprint 2)

```
frontend/chat.html
    user types a prompt, submits the form

        js/chat.js
            renders the user's message immediately (own bubble)
            → apiPostStream("/chat/stream", {prompt}, onChunk)   (js/api.js)
            → fetch(..., {method: "POST", body: JSON.stringify({prompt})})
            ← response.body.getReader()  — read in a loop, not response.json()

Backend (uvicorn, port 8000)
    POST /chat/stream  (app/api/routers/chat.py)
        → StreamingService.stream(prompt)   ── same service Module 4 built ──
        → StreamingResponse(event_stream(), media_type="text/plain")
        ← chunks flow back over the same HTTP response as they're generated

        js/chat.js appends each chunk into the assistant's bubble as it arrives
```

Deliberately wired to `POST /chat/stream` (Module 4's `ChatService`/`StreamingService`), not `POST /agents/chat` (Module 6's `AgentService`) — the scoping trade-off made before writing any code: live token-by-token streaming, at the cost of cross-turn memory. `/chat/stream` takes only `{prompt}` — no `conversation_id`, no history — so a follow-up message gets zero context from the previous one. `/agents/chat` has real memory via `conversation_id` but no streaming variant today; adding one would be a backend change, out of scope for a frontend sprint. Nothing here required a backend change — the endpoint already existed, unmodified, since Module 4.

**Verification note:** live-verified the same way as Sprint 1 — a real headless browser, not a curl simulation — since curl can confirm the endpoint streams correctly but says nothing about whether `chat.js` actually renders the chunks into the right DOM node as they arrive.

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
- AgentGraphService
- MultiAgentService

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
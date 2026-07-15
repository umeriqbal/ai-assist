# AI Engineering Learning Notes

> This document contains the important concepts learned throughout the AI Engineer Bootcamp.

Unlike the module notes, this document is organised by topic rather than by time. It should become your personal AI Engineering handbook.

---

# Large Language Models (LLMs)

## What is an LLM?

A Large Language Model is a neural network trained to predict the next token in a sequence.

It does not "think" or "reason" in the human sense. It predicts the most probable continuation based on its training data and the context provided.

Examples:

- GPT-4.1
- GPT-4o
- Claude
- Gemini
- Llama

---

## Tokens

LLMs process text as tokens rather than words.

Example

```
Hello world
```

might become

```
["Hello", " world"]
```

The exact tokenisation depends on the model.

Tokens affect:

- Cost
- Context window usage
- Latency

---

## Context Window

The context window is the maximum number of tokens the model can process in a single request.

The context includes:

- System Prompt
- User Prompt
- Conversation History
- Retrieved Documents
- Tool Results

If the limit is exceeded, older information must be removed or summarised.

---

## Temperature

Controls randomness.

```
Temperature = 0
```

Predictable output.

Best for:

- APIs
- JSON
- RAG
- Code

---

```
Temperature = 1
```

More creative output.

Best for:

- Brainstorming
- Stories
- Marketing

---

## Hallucinations

Hallucinations occur when an LLM generates information that is incorrect or unsupported.

Common causes:

- Missing context
- Ambiguous prompts
- Lack of factual grounding

Mitigation:

- RAG
- Better prompts
- Structured outputs
- Evaluation

---

# Prompt Engineering

## Prompt Structure

A well-designed prompt usually contains:

- Role
- Task
- Context
- Constraints
- Output Format

Example

```
You are an AI architect.

Analyse the uploaded document.

Return JSON.

Do not invent information.
```

---

## System Prompt

Defines long-term behaviour.

Example

```
You are an experienced AI Engineer.
```

---

## User Prompt

Contains the specific task.

Example

```
Summarise this document.
```

---

## Structured Output

Instead of requesting free text, ask for structured data.

Example

```json
{
  "summary": "",
  "risks": [],
  "recommendations": []
}
```

Advantages:

- Reliable parsing
- Validation
- API integration

---

# Embeddings

## What is an Embedding?

An embedding is a numerical representation of text.

Similar text produces similar vectors.

Example

```
"Dog"

↓

[0.12, -0.44, ...]
```

Embeddings allow semantic comparison rather than keyword matching.

---

## Semantic Search

Instead of searching for identical words, semantic search compares meaning.

Example

Query

```
How many vacation days do employees receive?
```

can match

```
Annual Leave Policy
```

without containing the same words.

---

## Cosine Similarity

Measures the angle between two vectors.

Range

```
1.0
```

Very similar.

```
0.0
```

Unrelated.

```
-1.0
```

Opposite direction.

Higher similarity indicates more relevant documents.

---

# Chunking

Large documents must be split before embedding.

Reasons:

- Token limits
- Better retrieval
- Improved relevance

---

## Chunk Size

Typical values

```
500 tokens

750 tokens

1000 tokens
```

Trade-off

Small chunks

- More precise retrieval

Large chunks

- More context

---

## Chunk Overlap

Overlap preserves context between chunks.

Example

```
Chunk 1

Sentence A

Sentence B

Sentence C

----------------

Chunk 2

Sentence C

Sentence D

Sentence E
```

This reduces the chance of splitting important ideas.

---

# Retrieval Augmented Generation (RAG)

## Definition

RAG combines retrieved knowledge with an LLM.

Pipeline

```
Question

↓

Retriever

↓

Relevant Documents

↓

Prompt

↓

LLM

↓

Answer
```

Advantages

- More accurate
- Uses private knowledge
- Reduces hallucinations

---

## Retriever

Retrieves the most relevant chunks.

Future implementation

- Similarity Search
- Metadata Filters
- Hybrid Search
- Re-ranking

---

## Citations

Answers should include sources.

Example

```
Employee Handbook

Page 12
```

Benefits

- Transparency
- Trust
- Easier verification

---

# FastAPI

## Routers

Responsibilities

- HTTP
- Validation
- Status Codes

Routers remain thin.

---

## Services

Contain business logic.

Examples

```
ChatService

StreamingService

DocumentService
```

---

## Providers

Wrap external SDKs.

Examples

```
OpenAIProvider

AnthropicProvider
```

Services never communicate directly with SDKs.

---

# Dependency Injection

Purpose

Manage object creation outside business logic.

Example

```
Router

↓

Depends()

↓

ChatService

↓

Provider
```

Benefits

- Loose coupling
- Easier testing
- Cleaner architecture

---

# Provider Pattern

Purpose

Hide external SDK implementations.

Architecture

```
ChatService

↓

LLMProvider

↓

OpenAIProvider
```

Allows providers to be swapped without changing business logic.

---

# Streaming

Traditional API

```
Wait

↓

Entire Response
```

Streaming

```
T

Th

The

The answer...
```

Benefits

- Better user experience
- Lower perceived latency

---

# LangChain

We use LangChain only for RAG functionality.

Responsibilities

- Documents
- Loaders
- Splitters
- Embeddings
- Retrievers

LangChain is **not** the application architecture.

---

# AI Agents

An AI Agent can:

- Plan
- Execute
- Observe
- Reflect
- Retry
- Use Tools

Unlike a chatbot, an agent can perform multi-step tasks autonomously.

---

## Tool Calling

A tool is a contract, not an implementation detail: a name, a description, a JSON Schema of arguments, and an `execute()`. The description and schema are the only things the model ever sees — how well they're written directly affects whether the model calls the tool correctly (or at all).

---

## The ReAct Loop

The simplest working "agent" is: send the conversation + available tools to the model → the model either answers directly or asks to call a tool → if it asks, run the tool and append the result to the conversation → send again → repeat until it answers directly.

```
Messages + Tools

↓

Model

↓

Tool call requested? ── no ──→ Final Answer
       │
      yes
       ↓
  Execute Tool

       ↓
Append result to messages
       │
       └──→ back to Model
```

Two failure modes to guard against explicitly, not as an afterthought:

- **Unbounded looping** — nothing stops a model from requesting tools forever. A max-iteration cap is not optional.
- **Hallucinated tool names** — the model can ask for a tool that doesn't exist. Crashing the request is worse than feeding an error string back and letting the model recover.

---

## Tool Calling vs. the Provider Pattern

Tool-calling wire formats are provider-specific (OpenAI's Responses API needs an echoed `function_call` item plus a `function_call_output` item, keyed by `call_id`; other providers shape this differently). If that shape leaks into the agent loop itself, swapping providers later means rewriting business logic — exactly what the Provider Pattern exists to prevent. The fix: give each provider a method that translates "a tool call and its result" into whatever its own wire format needs, and never construct that shape outside the provider.

---

## Planning (Plan-and-Execute)

A ReAct loop discovers its path one tool call at a time — it's reactive. Planning is the alternative: decompose a goal into an explicit, ordered list of steps *before* executing anything.

```
Goal

↓

Planner (structured output)

↓

Plan (ordered steps)

↓

Execute each step (still via the ReAct loop, with tools)

↓

Synthesize a final answer from all step results
```

Trade-off: a plan made upfront can't react to what a step actually discovers the way a pure ReAct loop can — which is why each step is still executed through the ReAct loop (it can still use tools and adapt within that one step), and why later steps are given earlier steps' results as context. Planning and reacting aren't mutually exclusive; plan-and-execute nests a ReAct loop inside each step.

The benefit that justifies the extra machinery: the plan itself is inspectable output. A user (or a future Reflection/Review step) can see the steps the model intends to take, not just the tool calls it happened to make.

---

## Structured Output vs. Prompt-Instructed JSON

Two ways to get JSON out of an LLM:

- **Prompt-instructed** — ask nicely in the prompt ("respond with JSON matching this shape"), then parse the text response and hope it matches. Fragile: the model can wrap it in prose, use markdown code fences, or drift from the schema.
- **Structured output** — pass a JSON Schema to the API itself (OpenAI's `strict` mode grammar-constrains generation so the output *cannot* violate the schema). Reliable, but requires a schema the API accepts (e.g. OpenAI's strict mode requires `additionalProperties: false` at every object level, which Pydantic models need `extra="forbid"` to produce).

Prefer structured output whenever a schema is available. Prompt-instructed JSON parsing is a workaround for when it isn't (or wasn't yet built) — worth naming as technical debt rather than a permanent pattern, so it gets revisited once the real mechanism exists.

---

## Reflection (Self-Critique)

A generate → critique → revise loop: produce an answer, ask the model to judge its own answer against the original question, and if it's found lacking, revise and re-check — bounded by an iteration cap, same discipline as the ReAct loop's tool-call cap.

```
Answer

↓

Critique (structured: satisfactory? + feedback)

↓

Satisfactory? ── yes ──→ Done
       │
       no
       ↓
   Revise (answer + feedback → new answer)
       │
       └──→ back to Critique
```

Two things worth being deliberate about:

- **What happens at the iteration cap matters, and it's not always "fail."** A tool loop that never gets an answer has genuinely failed — raising is correct. A reflection loop that never gets to "satisfactory" still has a real, usable answer sitting there — it just wasn't perfectly polished. Returning that last draft is the right call, not an error.
- **Self-critique is not the same as correctness.** A model judging its own output can be wrong, overconfident, or overly harsh — reflection improves average quality, it doesn't guarantee it. That's why the drafts and feedback are worth surfacing to the caller rather than hiding them: visibility into "the model thought this was fine" is itself useful signal.

**Distinct from offline evaluation** (`FaithfulnessService`, Module 5): that judges an answer *after the fact*, against retrieved context, for measurement purposes. Reflection judges an answer *before returning it*, against the question, as part of producing the answer. Same "LLM-as-judge" idea, different point in the pipeline, different purpose.

---

## Memory

Every agent service built so far is stateless per call — each request starts from nothing. Memory means carrying context across multiple calls: a real conversation, not just a single self-contained exchange.

```
Turn 1: "My favorite number is 47."  ──→  stored

Turn 2: "What's my favorite number?"  ──→  loads Turn 1  ──→  "47"
```

Two design choices worth naming explicitly:

- **What to store.** An agent turn can involve a lot of internal machinery (tool calls, intermediate results). Memory here stores only the human-visible exchange — the user's message and the final answer — not that internal machinery. It's simpler, keeps the memory store free of any provider-specific wire format, and matches what a person would actually recall about "the conversation so far."
- **Identity.** Memory needs a key — some `conversation_id` scoping which turns belong together. Without one, there's no way to know which history belongs to which caller. Auto-generating one when the caller doesn't supply it (and always returning it) is a small but real UX decision: the caller shouldn't have to invent an id scheme just to get a multi-turn conversation working.

**Same evolution story as the vector store.** `InMemoryVectorStore` (Module 5) was an intentional first pass — in-memory now, `PostgreSQL`/`pgvector` later, behind the same interface. `InMemoryConversationMemory` repeats that pattern exactly: build the interface, ship a process-local implementation, swap the implementation later (Redis or PostgreSQL) without touching anything that calls it.

---

## LangGraph: A Framework Should Read as Familiar, Not Magic

The test of whether a framework has actually been *understood*, not just *used*: rebuild something you already hand-built, and see if the framework version is recognizable as "the same thing, now managed" — not a black box that happens to produce similar output.

Concretely here: the Sprint 1 `AgentService` loop is —

```
while not done:
    ask the model (with tools)
    if it wants a tool: run it, feed the result back
    else: done
```

The LangGraph version is the same three moves, relabeled:

```
node "call_model"  →  ask the model (with tools)
node "call_tools"  →  run the tool, feed the result back
conditional edge   →  "if it wants a tool → call_tools, else → end"
```

Nothing about *what* gets called changed — the graph's nodes call the identical `LLMProvider.chat_with_tools()` / `Tool.execute()` methods the hand-built loop calls. What LangGraph actually added: a checkpointer (`MemorySaver`) that persists the state (`messages`) across calls automatically, keyed by a `thread_id` — the exact capability Sprint 4 hand-built as `ConversationMemory`, now framework-managed. And a recursion limit that serves the same role as the hand-rolled `max_iterations` guard.

**A structural lesson, not just a LangGraph one:** if a framework wants control over *how* the LLM gets called (e.g. a LangChain chat model bound to tools) rather than just *when* your own code runs, that's worth noticing and pushing back on — not because frameworks are bad, but because letting orchestration frameworks quietly own work an abstraction (Provider Pattern, here) already owns is how architecture erodes one convenient shortcut at a time.

---

## Dependency Pinning Across an Ecosystem

Installing the latest version of a package in the same ecosystem as existing pinned packages (here: `langgraph` alongside an already-pinned `langchain`) can silently pull in a newer *shared* dependency (`langchain-core`) that the existing pinned packages don't support — `pip`'s resolver doesn't retroactively check that. The fix isn't to unpin everything to "latest" (that reintroduces the exact version-drift risk pinning exists to prevent) — it's to find the version of the *new* package whose own constraints are compatible with what's already pinned, and confirm with `pip check` before moving on.

---

## Multi-Agent Collaboration: Specialists, Not a New Kind of Agent

The temptation with "multi-agent" is to invent a new abstraction — a `Specialist` base class, an `AgentRole` enum, something that feels proportionate to a grander-sounding capability. What actually made this work:

- **A specialist is just an agent with a narrower job.** `AgentService` already had everything needed — a tool set and a loop. The only thing missing was a way to give it an identity (`system_prompt`), so a Researcher and a Writer could be two configurations of the same class, not two new ones.
- **Coordination is a routing decision, repeated.** A `Supervisor` asking "who should act next, and what should they do?" is exactly the same shape as `generate_structured()` was already built for (Sprint 2) — just applied to a different question. No new provider capability, no new "coordination protocol."
- **The graph shape doesn't change with more workers.** Sprint 5's graph was one worker node (`call_tools`) behind a conditional edge. Sprint 6's graph is two worker nodes (`researcher`, `writer`) behind the same shape of conditional edge, routed by a decision (the supervisor's) instead of a boolean (has-tool-calls). Multi-agent collaboration, at this scale, is a routing problem wearing a bigger name.

The lesson generalizes past this project: before reaching for a new abstraction, check whether the "new" capability is actually a new *configuration* of something that already exists.

---

# Model Context Protocol (MCP)

MCP provides a standard way for AI applications to discover and interact with external tools.

Benefits

- Standardised tool interfaces
- Easier integration
- Reusable tool ecosystem

---

## A Well-Designed Abstraction Should Survive Contact With a New Protocol

The real test of whether `Tool` (built in Module 6, Sprint 1: name, description, JSON-Schema parameters, `execute()`) was actually a *good* abstraction, not just a convenient one for the one use case it was built for: hand it to a completely different protocol and see if it needs to change.

It didn't. `Tool.parameters` — a hand-written JSON Schema — maps onto MCP's `inputSchema` field with zero translation. `execute()` plugs directly into MCP's `call_tool` handler. The reason this worked: `Tool` was designed around a schema-first contract (what does the caller need to know to call this?) rather than around any particular caller's calling convention (OpenAI's tool-calling format, a Python function signature, or anything else). A schema-first design travels between protocols; a design implicitly shaped by one specific caller doesn't.

---

## Two Ways to Build an MCP Server, and Why the Choice Matters

The official Python SDK offers `FastMCP` (a decorator, `@mcp.tool()`, that infers a tool's schema from a Python function's type hints) and the low-level `Server` (you register `list_tools()`/`call_tool()` handlers yourself, supplying the schema explicitly).

`FastMCP` is the right choice when tools are being *defined* fresh, in Python, for MCP specifically — the decorator's inference is a genuine convenience there. It's the wrong choice when a schema *already exists* elsewhere (as `Tool.parameters` did) — the inference has nothing to infer from a generic `**kwargs` function signature, and would fight, not save, work already done. The low-level API isn't the "harder" option here; it's the one that matches the shape of the problem.

General lesson: a framework's "easy" high-level API optimizes for its own common case. When a project's own abstraction already solves the problem the high-level API is trying to solve, reach for the low-level API instead of contorting the existing abstraction to fit the framework's assumptions.

---

## Validate Third-Party API Shape Before Designing Around It

Two SDK inspection steps happened before any production code was written: checking `FastMCP.tool()`'s actual signature (confirming it infers from type hints, not a supplied schema) and running a full smoke test of the low-level `Server` + an in-memory client session (confirming `inputSchema` really does accept an arbitrary JSON Schema dict, and that discovery + execution round-trip correctly). Only after both were confirmed did `app/mcp/server.py` get written.

This is the same discipline Sprint 5's LangGraph work used (a throwaway smoke script before the real `agent_graph.py`), applied again here. The pattern generalizes: when adopting an SDK whose exact behavior isn't already known, spend five minutes confirming the shape of the thing before spending an hour designing around a guess.

---

## A CLI Convenience Wrapper Is Not the Same as the Protocol Itself

The Python MCP SDK ships a `mcp dev` command that launches the Inspector — but it explicitly refuses to run against anything but a `FastMCP` server; it errors out against the low-level `Server` this project uses. That looked, briefly, like "the Inspector doesn't support our design."

It wasn't true. The Inspector itself (`@modelcontextprotocol/inspector`, a separate npm package) speaks MCP — the protocol — not "whatever `FastMCP` happens to expose." Run directly (`npx @modelcontextprotocol/inspector python -m app.mcp.run_server`), bypassing the SDK's own convenience wrapper, it connects to our low-level server without any issue, because from its point of view it's just talking to *an* MCP server, not specifically a `FastMCP` one.

The general lesson: a language SDK's CLI tooling is often built around that SDK's own preferred high-level pattern, and its limitations reflect that convenience layer's choices — not the underlying spec's. When a "the tool doesn't support my approach" wall shows up, check whether the wall belongs to the protocol or just to one wrapper around it before concluding the approach itself needs to change.

---

## The Client Side Is the Server Side's Adapter, Mirrored

Sprint 1 built `build_mcp_server()`: given a local `Tool`, produce something that looks like an MCP tool to a client (`inputSchema`, `call_tool`). Sprint 2 built `MCPToolAdapter`: given a remote MCP tool, produce something that looks like a local `Tool` (`.name`, `.parameters`, `.execute()`). Same translation, opposite direction.

Noticing that symmetry before writing any code is what kept Sprint 2 small: there was no need to invent new concepts for "how does a remote tool's schema get represented" or "what happens when a remote tool errors" — those questions were already answered in Sprint 1, just facing the other way. When a new sprint's problem turns out to be the mirror image of a solved one, look for the reflection before designing something new.

**Consequence worth naming:** because both directions go through the exact same `Tool` interface, `AgentService` needs zero changes to use a mix of local and MCP-sourced tools in the same `tools` list — it was never written to know or care where a tool's `execute()` actually runs.

---

## "Remote" Isn't a Feature Flag — It's a Different Transport

Sprints 1–2's stdio transport is a subprocess pipe: same machine, spawned per connection, gone when the parent process exits. Calling that "remote execution" would have been technically working but conceptually dishonest — nothing actually crossed a network boundary. Sprint 3 fixed that by switching to streamable-HTTP: the MCP server becomes a standing service on its own port, reachable by URL, running independently of whatever connects to it.

The interesting part is how little else changed. `MCPToolAdapter`, `discover_tools()`, `Tool` — none of it cared whether the underlying transport was a pipe or a socket. Only the *connection* function changed (`connect_stdio_mcp_server` → `connect_http_mcp_server`); everything built on top of a `ClientSession` stayed identical. That's what a well-drawn abstraction boundary buys: transport is an implementation detail the protocol library owns, not something that should leak into the code that discovers and uses tools.

---

## When a Dependency Needs a Lifecycle, Reach for `lifespan`, Not a Bigger `@lru_cache`

Every dependency built before this sprint was a synchronous, lazy constructor call — `@lru_cache` on a function that returns `SomeService(...)`. That pattern quietly assumes construction is cheap and instantaneous. Connecting to a network service and discovering its tools is neither: it's genuinely async, it can fail, and it needs to happen once at startup and be torn down at shutdown — not on whatever request happens to touch it first.

Trying to force that into an `@lru_cache` function would mean either blocking synchronous code doing async work (awkward at best) or lazily connecting on first request (meaning the first real user request pays the connection cost and risk, not startup). FastAPI's `lifespan` context manager exists precisely for this shape of problem: it's the tool for "this needs setting up once, kept alive, and torn down cleanly" — not a variant of dependency injection, a different lifecycle entirely. Recognizing which shape a new dependency has (constructor-cheap vs. lifecycle-managed) determines which of the two patterns it belongs in.

---

# Frontend & Browser Clients

## CORS Is a Browser Rule, Not a Server Rule

The Same-Origin Policy — and CORS, the mechanism that relaxes it — is enforced entirely by the browser, not the server. A `curl` request or a backend integration test hits the API directly and never triggers it, because there's no browser in the loop deciding whether to expose the response to calling JavaScript. `CORSMiddleware` doesn't protect the server from anything; it's the server telling browsers "this origin is allowed to read my responses," and only browsers listen.

The practical consequence: a "the frontend can't reach the backend" bug can look completely healthy from every backend-side check (logs show 200s, `curl` works fine) while genuinely failing for the one client that matters — the browser — because the error surfaces only in its console, as a blocked response the JavaScript never gets to see. Debugging this from the server side alone is looking in the wrong place; the browser console is the actual source of truth.

`allow_origins=["*"]` would have made this invisible during development, but it's also a wildcard permission — this project set `FRONTEND_URL` as an explicit configured origin instead, on the same "don't hide problems, don't over-grant access" reasoning that shaped every other config default (e.g. `mcp_server_host`/`port`).

---

## Verifying a UI Change Means Opening an Actual Browser

Every prior sprint's "live verification" meant hitting an endpoint — `curl`, Swagger, a Python smoke script — and reading the JSON back. That works because the client and the correctness criterion were the same thing: valid response body in, valid response body confirmed.

A frontend breaks that equivalence. `GET /health` returning 200 says nothing about whether `js/main.js` actually parsed the response, updated the right DOM node, or whether CSS rendered the status pill in a readable color — none of that is visible to `curl`. Real verification needed an actual browser executing the actual JavaScript against the actual CSS: a headless Chromium instance (via Playwright), loading the real page, checking the console for errors, and a screenshot inspected for correct rendering, not merely "did it not crash."

The general principle: the verification method has to match what the client actually is. A JSON API's client is any HTTP caller — curl is a faithful stand-in. A browser UI's client is a browser — nothing else is a faithful stand-in for it.

---

## Operational Ordering Can Be a Real Dependency, Not Just a Convenience

Module 7 Sprint 3 already established that the backend depends on the MCP HTTP server being up first (its `lifespan` connects to it at startup and fails hard otherwise). Adding a frontend didn't remove that dependency — it added a third link to the same chain: MCP server → backend → frontend, in that order, across three independent processes.

This is easy to treat as a documentation footnote, but it's a real architectural fact worth naming: whenever one running process's startup (or a request it serves) depends on another already being reachable, that ordering isn't optional detail — it's part of the system's actual behavior, and skipping it produces a failure (`ExceptionGroup`/`httpx.ConnectError` here) that looks unrelated to its real cause unless the dependency chain is already understood.

---

## Two Endpoints Can Both Be "The Chat Endpoint," and Not Be Interchangeable

By Sprint 2, this project had two endpoints that both answer "send a chat message, get a reply": `POST /chat` (stateless, and its streaming sibling `POST /chat/stream`) and `POST /agents/chat` (stateful, via `conversation_id`). They look interchangeable from a UI's point of view — same shape of request, same shape of intent — but they're built for different things, and each is missing what the other has: `/chat/stream` streams tokens live but forgets everything between calls; `/agents/chat` remembers the whole conversation but returns its answer all at once.

Wiring a UI to "the chat endpoint" without naming which one, and why, would have silently picked a trade-off no one decided on. Making the choice explicit — streaming over memory, because the UI's most visible behavior (does text appear live?) mattered more here than a capability (follow-up context) the UI wasn't yet built to use anyway — is the same discipline as picking `FastMCP` vs. the low-level `Server` API in Module 7: two options that both "work," where the right one depends on which property the moment actually needs, not which sounds more complete.

---

## Two Real Operational Gotchas, From an Actual Local Run

Getting Sprint 2 running end to end on the user's own machine (not just the Playwright-driven verification) surfaced two failure modes worth naming, because both look like application bugs and are actually environment/process mistakes:

- **A "venv active" prompt doesn't guarantee the right binary resolves.** Running the bare `uvicorn app.main:app --reload` command picked up a *global* `uvicorn` (a different Python install entirely) instead of the project's `.venv` one, producing `ModuleNotFoundError: No module named 'app'` — an error that looks like a broken import, not a `PATH` issue. `python -m uvicorn ...` sidesteps this: it always uses whichever `python` is currently active, rather than trusting `PATH` to have resolved `uvicorn` to the matching install.
- **A static file server's "root" is whatever directory launched it, not the project's frontend folder.** Running `python -m http.server 5500` from the repo root instead of `frontend/` produced a real, correct 404 for `/chat.html` — the file existed, just not where the server was looking. `cd` into the target directory and confirm with `pwd` before starting a static server; don't assume the working directory from where a terminal happens to be.

Neither is specific to this project — both are the general class of "the error message describes a symptom one layer removed from the actual cause" (PATH resolution, cwd-relative serving), which is exactly why matching the debugging strategy to where the failure actually originates (check `which python`; check `pwd`) resolves them in seconds instead of guessing at application logic.

---

# Evaluation

A production AI system must be measured.

Metrics include:

- Retrieval Precision
- Retrieval Recall
- Faithfulness
- Groundedness
- Hallucination Rate
- Latency
- Token Usage
- Cost

Evaluation is an engineering discipline, not an optional extra.

---

## Observability Has a Precondition: Something to Observe

Module 9 (cost tracking, latency monitoring, model comparison, prompt versioning) was scoped down to a real, concrete Sprint 1 plan — and then deliberately not built. Working through *why* is the actual lesson, more than the metrics list above.

Every one of those capabilities only pays for itself in one of two situations: there's **ongoing real traffic** to watch (so a trend, a spike, a regression means something), or there's an **automated mechanism that acts** on what's measured (traffic gets routed to whichever provider is cheaper, an alert fires, something changes). Neither existed here. No production traffic. No automated provider routing — provider selection was (and still is) a hard-coded constructor call.

A smaller version was considered — a single endpoint comparing OpenAI and Claude on one prompt — and rejected for a sharper reason: a comparison whose result doesn't change what the system does next has no lasting effect. You look at it once, and the system is exactly the same afterward. That's not a smaller version of the same value; it's a demo with none of it.

**The general principle:** "we might need this later" is not, by itself, a reason to build something now — *especially* infrastructure whose entire purpose is watching something over time. It has zero payoff until the "over time" part exists, and a real ongoing cost before that (a pricing table that goes stale is a maintenance burden with no offsetting benefit yet). The cheap version of "staying ready" is leaving the door open — here, that meant proving the abstraction that would matter later (`ClaudeProvider`, showing the Provider Pattern actually generalizes) without building the system that would consume it before there's any traffic to feed it.

---

# AI Engineering Principles

Throughout this bootcamp we follow these principles:

- Build production-quality systems.
- Understand concepts before using frameworks.
- Keep architecture independent of vendors.
- Separate business logic from infrastructure.
- Prefer composition over inheritance.
- Design for maintainability.
- Deliver working features every sprint.
- Measure system quality continuously.

---

# Key Takeaway

The goal of this bootcamp is **not** to learn individual libraries.

The goal is to understand how to design, build, deploy, and maintain production AI systems.

Libraries will evolve.

Good architecture and engineering principles remain valuable.
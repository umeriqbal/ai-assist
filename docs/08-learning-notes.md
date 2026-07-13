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
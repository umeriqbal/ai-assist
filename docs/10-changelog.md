# Changelog

All notable changes to the Enterprise AI Assistant project are documented in this file.

The format follows the principles of Keep a Changelog.

---

# [1.0.0] - Enterprise AI Assistant (In Progress)

**Status:** 🚧 In Progress

Taken up out of the original roadmap order, at the user's direction — Module 8 (Production Infrastructure) is still not started, and Module 9 (Evaluation & Observability) was scoped then deliberately deferred (see the Unreleased entry below).

### Added — Sprint 1: Frontend Foundations (Complete)

- **Stack decision, made before any code:** standalone static frontend — plain HTML/CSS/JS, no build tooling, no framework. React, Vue, and Svelte were all considered and declined, consistent with this project's running theme of understanding a layer by hand before reaching for a framework (Module 3's semantic search, Module 6's hand-built ReAct loop before LangGraph)
- `CORSMiddleware` added to `create_app()` (`app/core/application.py`) — **the first client in this entire project served from a different origin than the backend.** Every prior caller (curl, Swagger's own UI, another Python process via `connect_stdio_mcp_server`/`connect_http_mcp_server`) was same-origin or not a browser at all, so nothing before this ever triggered a browser's CORS enforcement
- `FRONTEND_URL` setting (`app/core/config.py`) — the allowed origin is named explicitly, not `allow_origins=["*"]`
- `frontend/index.html`, `css/styles.css`, `js/api.js` (shared `fetch()` wrapper — `apiGet`/`apiPost` — every later sprint's page will reuse this), `js/main.js` (calls `GET /health` on load, renders the result into the DOM). Native ES modules (`<script type="module">`), not a bundler — standard browser JS
- Live-verified in a **real headless browser**, not a curl simulation: `chromium-cli` doesn't exist in this environment and no project run-skill covered launching this app yet, so a one-off Playwright driver script was written (Playwright's Chromium binaries were already cached locally). Confirmed: real CORS negotiation succeeded, the health data rendered correctly into the DOM, zero console errors, and a screenshot showed correct visual layout (a green "Backend: reachable" pill, all four `/health` fields listed)
- Surfaced a real operational dependency along the way: `create_app()`'s `lifespan` (Module 7, Sprint 3) requires the MCP HTTP server already running, so exercising the full stack needs **three processes in order** — `app.mcp.run_http_server`, then the FastAPI app, then the `frontend/` static server. No single command starts all three yet
- Recommended follow-up, not yet done: generate a project run-skill (`/run-skill-generator`) capturing this three-process startup order and the Playwright driver pattern, before Module 10 has many more UI sprints to verify the same way repeatedly

### Added — Sprint 2: Enterprise Chat UI (Complete)

- Scoping decision, made before any code: wire the chat page to `POST /chat` + `POST /chat/stream` (`ChatService`/`StreamingService`, Module 4) rather than `POST /agents/chat` (Module 6's `AgentService`, which has real multi-turn memory via `conversation_id` but no streaming variant today). Chose live token-by-token streaming over cross-turn memory — each send is still an independent call, matching what the streaming endpoint already supports without new backend work.
- `frontend/chat.html` — a new page (kept separate from `index.html`, one HTML page per feature, per the plan in [04-folder-structure.md](04-folder-structure.md)): a scrolling message list plus a textarea/send-button input row.
- `frontend/js/chat.js` — on send, renders the user's message immediately, then streams the assistant's reply into its own bubble chunk by chunk as `/chat/stream`'s response body arrives.
- `frontend/js/api.js` gained `apiPostStream(path, body, onChunk)` — reads `response.body.getReader()` directly, since streaming raw text can't reuse the existing `request()` helper's `response.json()` call.
- `frontend/css/styles.css` gained message-bubble styling (user vs. assistant, visually distinct), a scrolling chat container, and the input row; `index.html`/`chat.html` both gained a small top-bar nav (`Status` / `Chat`) linking between the two pages — no router, plain `<a href>`.
- Live-verified in a real headless browser: sent a message, watched the assistant bubble fill in as chunks arrived, confirmed zero real console errors (only the expected `favicon.ico` 404 any static site gets) and a screenshot of both pages rendering correctly.
- Confirmed working end to end on the user's own machine, all three processes run manually. Surfaced two real environment issues along the way (both now in [07-development-guide.md](07-development-guide.md)'s Common Issues): a bare `uvicorn` command resolving to a global Python 3.10 install instead of the project's `.venv` (fixed by running `python -m uvicorn` instead, which always uses the active interpreter), and `python -m http.server` returning a correct-but-confusing 404 when launched from the repo root instead of `frontend/` (the server's web root is whatever directory it was started from).

### Added — Sprint 3: Knowledge Base UI (Complete)

- Scoping decision, made before any code: wire the page to `POST /documents/upload` (multipart file upload) and `POST /documents/search` (semantic search) — Module 5's two end-user-facing endpoints — rather than `POST /documents`, `/documents/chunks`, `/documents/embeddings`, or `/documents/index`, which expose the RAG pipeline's individual internal stages for testing, not something an end user interacts with directly.
- `frontend/kb.html` — one page, two sections: an upload panel (file picker restricted to `.pdf` via `accept`, optional source name, submit) and a search panel (query input, submit), so the index → search round trip is visible on one screen.
- `frontend/js/kb.js` — upload renders a confirmation card (source, pages loaded, chunks indexed) or a surfaced backend error; search renders each result as a card (content, source badge from `metadata`, similarity score).
- `frontend/js/api.js` gained `apiPostForm(path, formData)` — sends a `FormData` body with **no manually-set `Content-Type`** (the browser sets the multipart boundary itself); a third distinct request shape after `apiPost`'s JSON and `apiPostStream`'s streamed-read, each with a genuinely different wire contract.
- `frontend/css/styles.css` gained form/input styling, an upload-result notice, and search-result cards; all three pages (`index.html`/`chat.html`/`kb.html`) gained a `Knowledge Base` nav link.
- Live-verified in a real headless browser, end to end: uploaded a real (minimal, hand-crafted) PDF fixture, confirmed the indexing confirmation rendered correctly, searched for its content, and confirmed real search results (with real similarity scores) rendered as cards. Also confirmed, via a direct API call first, that uploading a non-PDF file correctly surfaces the backend's existing `"No loader registered for '.txt'."` error through the UI rather than silently failing — the file input's `accept=".pdf"` plus a visible hint now steer users away from hitting it in the first place.

### Not Included

- Website Crawling, Agents UI, Evaluation Dashboard, Admin Interface (Sprints 4+, not yet scoped)
- Cross-turn conversation memory in the chat UI (would require a streaming variant of `AgentService`, a backend change — deliberately deferred, see the Sprint 2 scoping decision above)
- Non-PDF document upload in the UI (DOCX/HTML/Markdown loaders remain unimplemented on the backend — pre-existing, Medium Priority backlog item from Module 5, not addressed by this sprint)

---

# Unreleased — Standalone Work Between Modules 7 and 8

Not tied to a module's sprint sequence; recorded here since it's real, tested code and a real scoping decision.

### Added

- `ClaudeProvider` (`app/providers/claude_provider.py`) — Anthropic implementation of `LLMProvider`, all 6 methods (`chat`, `stream_chat`, `chat_with_tools`, `tool_result_messages`, `generate_structured`, `health_check`). Built to prove the Provider Pattern actually generalizes to a second vendor, not just in theory. API shape validated by SDK introspection before writing any code (same discipline as every other new SDK integration in this project) — `anthropic==0.116.0` checked against pinned `httpx`/`pydantic` first, no conflict this time.
- Real difference worth recording: Claude's Messages API takes a system prompt via its own top-level `system=` parameter, not as a `{"role": "system", ...}` entry inside `messages` the way OpenAI's Responses API allows. `ClaudeProvider.chat_with_tools()` pulls system-role entries out of the incoming generic `messages` list and redirects them — exactly the class of problem `tool_result_messages()` already existed to absorb per-provider.
- `ANTHROPIC_API_KEY` (optional, unlike the required `OPENAI_API_KEY`) and `ANTHROPIC_CHAT_MODEL` settings; `get_claude_provider()` added to `dependencies/llm.py`, alongside — not replacing — `get_openai_provider()`.
- **Not wired into any active service.** Every `get_*_service()` in `dependencies/services.py` still calls `get_openai_provider()`. `ClaudeProvider` exists so a future provider switch is a config change, not a rewrite.

### Scoped, then deliberately not built

- **Module 9 — Evaluation & Observability.** Scoped to a concrete Sprint 1 plan: `CostTracker` as an injected recorder (optional constructor arg on providers, reporting usage as a side effect rather than changing `chat()`'s return type), a new `app/observability/` layer, `InMemoryCostTracker`, a pricing table, a `GET /observability/costs` endpoint. Design was sound; built nothing, on reflection. Every capability in this module — cost tracking, latency monitoring, model comparison, prompt versioning — only has real value against ongoing real traffic, or when something automated acts on the data (e.g. routing requests to whichever provider is cheaper). Neither exists yet: no production traffic, and provider selection is a hard-coded constructor call, not a runtime decision.
- A smaller alternative was also considered and rejected: a single `POST /evaluate/compare` endpoint calling OpenAI and Claude on one prompt, no persistent tracking. Rejected because a comparison result that doesn't change what the system does next has no lasting effect — it's looked at once, then nothing.
- Revisit trigger: real production traffic worth watching (likely after Module 8's deployment work), or provider selection becoming a genuine runtime decision. `ClaudeProvider` above exists specifically so that door stays open cheaply.

---

# [0.7.0] - Model Context Protocol (MCP)

**Status:** ✅ Complete

### Added — Sprint 3: Remote Execution / Agent Integration (Complete)

- `app/mcp/http_server.py` (new) — wraps `build_mcp_server()`'s low-level `Server` in a Starlette ASGI app served over MCP's streamable-HTTP transport, using `StreamableHTTPSessionManager` plus a ~3-line ASGI adapter written directly (not imported from `mcp.server.fastmcp`'s internals, which this project deliberately doesn't depend on). Validated with a full smoke test — real uvicorn server on a real port, real HTTP client — before writing this as production code
- `app/mcp/run_http_server.py` (new) — standalone entry point serving the same tools (`EchoTool`, `KnowledgeBaseSearchTool`) over streamable-HTTP on its own port, genuinely network-addressable — unlike Sprints 1–2's stdio transport, this is not just a subprocess pipe
- `connect_http_mcp_server(url)` (new, `app/mcp/client.py`) — mirrors `connect_stdio_mcp_server`, using `streamable_http_client` (not the deprecated `streamablehttp_client` alias, caught and switched during implementation)
- Settings gained `mcp_server_host`/`mcp_server_port`/`mcp_server_url` (`app/core/config.py`), per Decision 009 — no hard-coded connection details
- `create_app()` gained its first `lifespan` (`app/core/application.py`) — connects to the MCP HTTP server at startup via `connect_http_mcp_server()`, discovers its tools via `discover_tools()`, and builds an `AgentService` from them, held open for the app's entire lifetime. The first dependency in this project needing real async setup/teardown, not just a lazy `@lru_cache` constructor call — startup fails clearly if the MCP server isn't already running, since there's no sensible fallback for "the tools this agent needs don't exist yet"
- `get_mcp_agent_service(request: Request)` (new, `app/dependencies/services.py`) — reads the lifespan-built `AgentService` off `request.app.state`; not `@lru_cache`, since the lifespan already populates it once per app lifetime
- `POST /agents/mcp-chat` (new) — same `AgentChatRequest`/`AgentChatResponse` shape as `POST /agents/chat`, backed by an `AgentService` whose tools are entirely MCP-discovered
- Integration test (`test_mcp_http_transport.py`, new) — a real uvicorn server on a real port, a real client connecting over HTTP; deliberately not mocked, since the whole point of this increment is proving the network transport actually works
- Live-verified with both processes running for real: `run_http_server.py` and the FastAPI app started independently; a forced remote `echo` call round-tripped correctly (`REMOTE-MCP-ROUNDTRIP-CONFIRMED`); a knowledge-base question correctly triggered a real HTTP call to the MCP server and got back an honest "no results" (confirming the known cross-process vector-store gap, not a bug)
- **Module 7 (Model Context Protocol) is now fully complete** — all 3 sprints (Server Foundations, Client + Tool Discovery, Remote Execution/Agent Integration) delivered, unit-tested, and live-verified across genuine process boundaries

### Added — Sprint 1: MCP Server Foundations (Complete)

- `mcp==1.28.1` added to `requirements.txt`, plus an explicit `starlette==0.47.3` pin — installing `mcp` alone pulls in a `starlette` release that conflicts with `fastapi==0.116.1`'s pin (`starlette<0.48.0`); same class of ecosystem dependency conflict as Sprint 5's `langgraph`/`langchain-core` issue, resolved the same way (find a compatible resolve, confirm with `pip check`, and this time also pin the shared dependency explicitly so a future fresh install doesn't drift back into the conflict)
- `app/mcp/` layer created (new top-level folder, reviewed and confirmed before adding, per [04-folder-structure.md](docs/04-folder-structure.md)'s explicit rule) — confines the `mcp` SDK the same way `rag/` confines LangChain and `agents/` confines LangGraph
- `build_mcp_server()` (new, `app/mcp/server.py`) — uses the low-level MCP `Server` API rather than `FastMCP`, validated with a smoke test before committing to the design: `Tool.parameters` (a hand-written JSON Schema, from Module 6 Sprint 1) maps directly onto MCP's `inputSchema` with zero adaptation, whereas `FastMCP`'s decorator infers schemas from Python type hints and would fight an already-explicit schema. Unknown tool names return an error `TextContent` instead of crashing, mirroring `AgentService`'s existing convention
- `app/mcp/run_server.py` (new) — standalone stdio-transport entry point exposing `EchoTool` and the real `KnowledgeBaseSearchTool` (wired to the actual `RetrievalService`)
- Unit tests: tool discovery (name/description/schema fidelity), successful execution, unknown-tool graceful handling, multi-tool exposure — using the MCP SDK's in-memory client/server session harness, no subprocess needed for the automated suite
- Live-verified beyond the in-memory harness: spawned `run_server.py` as a real subprocess and connected a real `ClientSession` over stdio — both tools discovered correctly, `EchoTool` executed correctly, `KnowledgeBaseSearchTool` correctly exercised the real embedding/retrieval pipeline (freshly empty vector store in the subprocess, correctly reported no results)
- Known, not yet addressed: the MCP server process and the FastAPI app process each hold their own separate in-memory vector store — a document indexed via `POST /documents/index` is invisible to the MCP-exposed `search_knowledge_base` tool. Fine for this foundational sprint; will matter once real cross-process data sharing is needed
- Addendum: since this server has no HTTP surface, it has no Swagger entry. Confirmed the official MCP Inspector (`npx @modelcontextprotocol/inspector python -m app.mcp.run_server`) works as the practical equivalent — a browser UI for listing and calling tools — despite the SDK's own `mcp dev` CLI wrapper explicitly refusing to run against a low-level `Server` (it only supports `FastMCP`). Documented in [07-development-guide.md](docs/07-development-guide.md)

### Added — Sprint 2: MCP Client + Tool Discovery (Complete)

- `MCPToolAdapter` (new, `app/mcp/client.py`) — adapts a tool discovered on a remote MCP server into this project's own `Tool` interface; the mirror image of Sprint 1's `build_mcp_server()` (which adapted a local `Tool` to look like an MCP tool). Remote tool errors surface as plain text content, not exceptions — respects `CallToolResult.isError` without special-casing it, consistent with how `AgentService` already treats "Error: ..." tool output as ordinary text
- `discover_tools(session)` (new) — lists every tool a connected `ClientSession` exposes and wraps each into an `MCPToolAdapter`, with zero hard-coded tool names anywhere in this code
- `connect_stdio_mcp_server(command, args)` (new) — async context manager wrapping `stdio_client` + `ClientSession.initialize()`, spawning an MCP server as a subprocess and yielding a ready-to-use session
- Validated with a smoke test before writing production code (same discipline as every SDK integration this module): confirmed `CallToolResult`'s `content`/`isError` shape, and that our own server's "unknown tool" handling comes back as plain text with `isError=False`
- Unit tests: schema-faithful discovery, successful execution through a real (in-memory) MCP session, multi-tool discovery, graceful surfacing of a remote tool error — using the same in-memory client/server harness as Sprint 1
- Live-verified beyond the in-memory harness: connected to the real Sprint 1 `run_server.py` subprocess, discovered both `echo` and `search_knowledge_base` with no prior knowledge of their names, and executed both successfully — completing the full `Tool` → MCP server → subprocess boundary → MCP client → `Tool` round trip
- Scope note: this sprint deliberately stops at proving the client + adapter in isolation. Wiring MCP-discovered tools into a running agent is Sprint 3's job, not duplicated here

---

# [0.6.0] - AI Agents

**Status:** ✅ Complete

### Added — Sprint 6: Multi-Agent Collaboration (Complete)

- `AgentService` gained an optional `system_prompt` constructor param — the first time an agent has had a role, not just a tool set; prepended as a `{"role": "system", ...}` message when set, a no-op otherwise (existing callers/tests unaffected)
- `SupervisorDecision` (new, `app/agents/supervisor_decision.py`) — `next: Literal["researcher", "writer", "finish"]` + `instructions: str`, strict-schema model
- `Supervisor` (new, `app/agents/supervisor.py`) — decides which specialist acts next given the transcript so far, via `generate_structured()` (Sprint 2's mechanism, reused a third time — no new provider capability needed)
- `MultiAgentState` + `supervisor`/`researcher`/`writer` graph nodes (new, `app/agents/multi_agent_graph.py`) — Researcher (`AgentService` + `KnowledgeBaseSearchTool`) and Writer (`AgentService`, no tools) coordinated by the Supervisor, built on the exact graph pattern `agent_graph.py` established in Sprint 5 (conditional edge + node-per-worker), just with more than one worker node this time. No checkpointer — this endpoint deliberately has no cross-call memory (Sprints 4–5 already demonstrated that capability)
- `MultiAgentService` (new, `app/services/multi_agent_service.py`) — thin wrapper invoking the graph, returning the final answer plus the full per-specialist transcript
- `POST /agents/collaborate` endpoint
- Unit tests: full researcher → writer → finish routing sequence, empty-prompt rejection, iteration-limit cap without needing to script every possible loop path
- Live-verified against the real OpenAI API and a real indexed document: the Supervisor correctly sequenced Researcher (retrieved the fact via the knowledge-base tool) → Writer (composed a polished, friendly answer from the researcher's findings) → finish — two genuinely distinct specialist outputs in the transcript, not one agent doing everything
- This realizes the "Planner/Supervisor → Specialist Agents → Final Answer" sketch that sat in `03-architecture.md` since before Module 6 began, with two concrete specialists rather than an open-ended set, and no separate "Reviewer Agent" — self-critique already exists as `ReflectionService` (Sprint 3) and wasn't duplicated here
- **Module 6 (AI Agents) is now fully complete** — all 6 sprints (Agent Architecture, Planning, Reflection, Memory, LangGraph + State Management, Multi-Agent Collaboration) delivered, unit-tested, and live-verified against the real OpenAI API

### Added — Sprint 5: LangGraph + State Management (Complete)

- `langgraph==0.6.11` added to `requirements.txt` — the first new dependency since Module 5. Deliberately pinned to the 0.6.x line: `langgraph`'s 1.x releases require `langchain-core>=1.0`, which conflicts with the pinned `langchain==0.3.27`/`langchain-openai==0.3.31`/`langchain-community==0.3.27` stack (all require `langchain-core<1.0.0`). Installing latest-`langgraph` first, discovering the conflict, then resolving to a compatible version was part of this increment, not a footnote — `pip check` confirms no broken requirements
- `AgentGraphState` + `call_model`/`call_tools` nodes (new, `app/agents/agent_graph.py`) — rebuild the Sprint 1 ReAct loop as a LangGraph graph. The nodes call the exact same `LLMProvider.chat_with_tools()`, `Tool.execute()`, and `LLMProvider.tool_result_messages()` that `AgentService` already uses — LangGraph replaces only the hand-written loop's control flow (a conditional edge routes back to `call_model` while tool calls are pending, or ends), not the underlying mechanics. LangGraph confined to `app/agents/`, mirroring Decision 013's isolation of LangChain to `app/rag/` — no LangChain chat model or message types used
- Compiled with LangGraph's `MemorySaver` checkpointer, keyed by `conversation_id` — replaces `ConversationMemory` for this path; a graph recursion limit (derived from `max_iterations`) stands in for the hand-rolled iteration cap, translated to the same `RuntimeError` on exceeding it
- `AgentGraphService` (new, `app/services/agent_graph_service.py`) — thin wrapper invoking the compiled graph
- `POST /agents/graph-chat` — same `AgentChatRequest`/`AgentChatResponse` shape as `POST /agents/chat` (unchanged), so the hand-built and graph-based implementations are directly comparable
- Unit tests: no-tool path, tool round-trip, unknown-tool fallback, iteration-limit cap, cross-turn memory under the same `conversation_id`, and isolation between different `conversation_id`s — mirroring `AgentService`'s test suite to demonstrate equivalent behavior
- Live-verified against the real OpenAI API: a fact stated in turn 1 recalled in turn 2 under the same `conversation_id`; a question requiring a freshly indexed document correctly triggered `KnowledgeBaseSearchTool` through the graph
- Known, explicitly documented (not fixed) asymmetry: `POST /agents/chat` and `POST /agents/graph-chat` use two independent state stores — a `conversation_id` from one is meaningless to the other — and `MemorySaver` persists the entire graph state (including tool-call round-trips) versus `ConversationMemory`'s curated human-only turns

### Added — Sprint 4: Memory (Complete)

- `ConversationMemory` (new, `app/agents/memory.py`) — ABC with `get_history()` / `append_turn()`; stores only the human-visible exchange (user message, final assistant answer), deliberately excluding the tool-call round-trips a turn may go through internally, keeping the store provider-agnostic
- `InMemoryConversationMemory` (new, `app/agents/in_memory_conversation_memory.py`) — process-local, non-persistent by design, same trade-off as `InMemoryVectorStore`; ready to swap for Redis/PostgreSQL (both already "Future" in the tech stack) behind the same interface
- `AgentService.chat()` extended with an optional `conversation_id` — when given, prior turns are loaded and prepended to the new user message before the existing ReAct loop runs unchanged, then the new turn is persisted once an answer is produced; raises if a `conversation_id` is passed but no memory store is configured for that `AgentService` instance
- `dependencies/llm.py` gained `get_conversation_memory()` (singleton, same caching rationale as `get_vector_store()`), wired into `get_agent_service()`
- `POST /agents/chat` — request gained an optional `conversation_id`; the server generates one when omitted and always returns it, so a client can continue the conversation on the next call
- Unit tests: `InMemoryConversationMemory` (empty-conversation default, ordering, multi-turn accumulation, isolation by id), `AgentService` (no-memory-used when no `conversation_id`, prior history included when one is given, new turn persisted, explicit error when `conversation_id` is passed without a configured memory store)
- Live-verified against the real OpenAI API: a fact stated in turn 1 was correctly recalled in turn 2 under the same `conversation_id`; a fresh conversation (new `conversation_id`) correctly had no knowledge of it
- Scope note: memory was added to `AgentService`/`POST /agents/chat` only, not `PlanningService`/`ReflectionService` — kept to the single concrete, demonstrable capability the roadmap names for this sprint rather than expanding scope

### Added — Sprint 3: Reflection (Complete)

- `Critique` (new, `app/agents/critique.py`) — `is_satisfactory: bool` / `feedback: str`, strict-schema Pydantic model
- `Reflector` (new, `app/agents/reflector.py`) — critiques a candidate answer against its question via `LLMProvider.generate_structured()`; required no new provider capability, pure reuse of Sprint 2's mechanism
- `ReflectionService` (new, `app/services/reflection_service.py`) — generate → critique → revise loop: initial answer via `AgentService.chat()`, critiqued by `Reflector`, revised via another `AgentService.chat()` call (question + previous answer + feedback, so revision can still use tools) if unsatisfactory, bounded by `max_iterations` (default 3). Deliberately different failure behavior from `AgentService`'s tool loop: hitting the iteration cap returns the last draft as a best-effort answer instead of raising — a reflection loop that never finishes still has a usable answer, unlike a tool loop that never got one
- `POST /agents/reflect` endpoint — returns the final answer plus every draft and its critique, so the self-correction process is visible
- Unit tests: `Reflector` contract via the fake provider, `ReflectionService` (immediate-satisfactory shortcut, one revision cycle, iteration-limit cap without raising, empty-question rejection)
- Live-verified against the real OpenAI API: both a general-knowledge question and a strict-format request were judged satisfactory on the first draft (no revision triggered); the revision branch itself is deterministically covered by unit tests rather than forced live
- Explicitly distinguished from `FaithfulnessService` (Module 5): that's an offline evaluation check on an already-given answer; `ReflectionService` is an inline runtime self-correction loop before an answer is ever returned

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

- Persistent conversation memory (Redis/PostgreSQL) — `InMemoryConversationMemory` is process-local by design, same as `InMemoryVectorStore`; `MemorySaver` carries the identical caveat for the graph path
- Reconciling the two independent `/agents/chat` vs. `/agents/graph-chat` state stores — deliberately kept separate for side-by-side comparison, not merged
- Cross-call memory for `POST /agents/collaborate` — deliberately out of scope for Sprint 6; Sprints 4–5 already covered that ground
- A "Reviewer Agent" as a third multi-agent specialist — self-critique already exists as `ReflectionService` (Sprint 3) and wasn't duplicated

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

## Carried over from 0.5.0 (not blocking)

- DOCX upload
- HTML ingestion
- Markdown ingestion

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
| 0.6.0 | AI Agents | ✅ |
| 0.7.0 | MCP | ✅ |
| 0.8.0 | Infrastructure | ⏳ |
| 0.9.0 | Evaluation | ⏸️ Deferred |
| 1.0.0 | Enterprise AI Assistant | 🚧 |

---

# Project Statistics

Current Status

- Modules Completed: 7 / 10
- Current Module: 10 (Sprint 1 of ~6 complete) — taken up out of order; Module 8 not yet started, Module 9 deliberately deferred
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
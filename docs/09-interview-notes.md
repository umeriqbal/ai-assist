# AI Engineer Interview Notes

> This document is a living interview preparation guide based entirely on concepts implemented during the Enterprise AI Assistant project.

The goal is not to memorise answers, but to understand the engineering decisions behind them.

---

# Module 1 — LLM Fundamentals

## Q1. What is a Large Language Model?

### Answer

A Large Language Model (LLM) is a neural network trained to predict the next token in a sequence of text. During inference, it uses the provided context to generate the most probable continuation.

Examples:

- GPT-4.1
- Claude
- Gemini
- Llama

---

## Q2. What is a token?

### Answer

A token is the unit of text processed by an LLM.

Tokens may represent:

- Whole words
- Parts of words
- Punctuation
- Whitespace

Tokens determine:

- API cost
- Context window usage
- Processing time

---

## Q3. What is a context window?

### Answer

The context window is the maximum number of tokens an LLM can process in a single request.

It includes:

- System prompt
- User prompt
- Conversation history
- Retrieved documents
- Tool outputs

---

## Q4. What causes hallucinations?

### Answer

Hallucinations occur when the model generates information that is not supported by its training data or provided context.

Ways to reduce hallucinations:

- Better prompts
- RAG
- Grounding with documents
- Structured outputs
- Evaluation

---

# Module 2 — Prompt Engineering

## Q5. What makes a good prompt?

### Answer

A good prompt includes:

- Role
- Task
- Context
- Constraints
- Output format

---

## Q6. Why use structured outputs?

### Answer

Structured outputs make AI responses easier to validate and consume programmatically.

Benefits:

- Reliable parsing
- Type safety
- Validation
- Better API integration

---

## Q7. Why validate AI output with Pydantic?

### Answer

Pydantic ensures responses match an expected schema.

Benefits:

- Detect malformed responses
- Prevent runtime errors
- Improve reliability

---

# Module 3 — Semantic Search

## Q8. What is an embedding?

### Answer

An embedding is a numerical vector representing the semantic meaning of text.

Similar text produces similar vectors.

---

## Q9. What is semantic search?

### Answer

Semantic search retrieves information based on meaning rather than exact keyword matching.

---

## Q10. What is cosine similarity?

### Answer

Cosine similarity measures the angle between two vectors to determine semantic similarity.

Higher values indicate greater similarity.

---

## Q11. Why do documents need chunking?

### Answer

Large documents exceed model context limits.

Chunking improves:

- Retrieval quality
- Embedding accuracy
- Context relevance

---

## Q12. What is chunk overlap?

### Answer

Chunk overlap repeats part of one chunk in the next to preserve context across chunk boundaries.

---

# Module 4 — Enterprise AI Platform

## Q13. Why use Layered Architecture?

### Answer

Layered Architecture separates concerns.

```
API

↓

Services

↓

Providers

↓

External Systems
```

Benefits:

- Maintainability
- Testability
- Scalability

---

## Q14. Why keep routers thin?

### Answer

Routers should only handle HTTP concerns.

Business logic belongs in services.

Benefits:

- Easier testing
- Cleaner code
- Better separation of concerns

---

## Q15. What is the Provider Pattern?

### Answer

Providers encapsulate external SDKs.

Example

```
ChatService

↓

LLMProvider

↓

OpenAIProvider
```

This reduces coupling to third-party libraries.

---

## Q16. What is Dependency Injection?

### Answer

Dependency Injection supplies objects from outside instead of creating them inside classes.

Benefits:

- Loose coupling
- Easier testing
- Better maintainability

---

## Q17. Why use an Application Factory?

### Answer

An Application Factory centralises application creation.

Benefits:

- Easier testing
- Configurable startup
- Cleaner architecture

---

## Q18. Why use async programming?

### Answer

Async allows the application to handle many concurrent I/O operations efficiently.

Useful for:

- OpenAI requests
- Databases
- Streaming
- File operations

---

## Q19. Why stream AI responses?

### Answer

Streaming reduces perceived latency by returning tokens as they are generated.

Benefits:

- Better UX
- Faster feedback
- Improved responsiveness

---

# Module 5 — Enterprise RAG

## Q20. What is RAG?

### Answer

Retrieval Augmented Generation combines document retrieval with an LLM.

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

---

## Q21. Why use RAG instead of fine-tuning?

### Answer

RAG is preferred when knowledge changes frequently.

Advantages:

- Up-to-date information
- No model retraining
- Lower cost
- Easier maintenance

---

## Q22. What is a LangChain Document?

### Answer

A `Document` is a standard container holding:

- Page content
- Metadata

It provides a consistent representation for downstream processing.

---

## Q23. Why preserve metadata?

### Answer

Metadata enables:

- Citations
- Filtering
- Source tracking
- Page references

---

## Q24. Why use RecursiveCharacterTextSplitter?

### Answer

It attempts to split documents at natural boundaries before falling back to smaller separators.

This preserves semantic meaning better than fixed-length splitting.

---

## Q25. Why use embeddings?

### Answer

Embeddings convert text into vectors that can be compared mathematically for semantic similarity.

---

## Q26. What is a vector store?

### Answer

A vector store stores embeddings and supports similarity search.

Examples:

- pgvector
- Pinecone
- Weaviate
- Chroma

---

## Q27. Why choose PostgreSQL + pgvector?

### Answer

Benefits:

- Mature database
- Lower operational complexity
- SQL support
- ACID compliance
- Good performance for many enterprise workloads

---

# Module 6 — AI Agents

## Q28. What is an AI Agent?

### Answer

An AI Agent is an LLM capable of planning and executing multi-step tasks using memory and tools.

---

## Q29. What is the difference between a chatbot and an agent?

### Answer

A chatbot responds to prompts.

An agent can:

- Plan
- Use tools
- Make decisions
- Execute workflows
- Reflect on results

---

## Q30. How does an agent decide to call a tool? (Sprint 1)

### Answer

The ReAct pattern: send the conversation plus the available tools' schemas to the model. The model either answers directly or requests a tool call by name with arguments. If it requests one, execute it and feed the result back into the conversation, then ask again — repeating until it returns a final answer instead of another tool call.

Two failure modes have to be handled explicitly, not left implicit:

- **Unbounded looping** — nothing stops a model from requesting tools forever without a hard iteration cap.
- **Hallucinated tool names** — the model can request a tool that doesn't exist; feeding an error back and letting the model recover is better than crashing the request.

---

## Q31. Why did tool-calling need a change to the Provider Pattern? (Sprint 1)

### Answer

Tool-calling wire formats are provider-specific — OpenAI's Responses API needs an echoed `function_call` item plus a `function_call_output` item keyed by `call_id`; other providers shape this differently. If that shape were built inside the agent's business logic, swapping providers later would mean rewriting the agent loop — exactly what the Provider Pattern exists to prevent.

The fix: give each provider a method (`tool_result_messages()`) that translates "a tool call and its result" into its own wire format, so the shape never leaves the provider layer.

---

## Q32. What is plan-and-execute, and how is it different from ReAct? (Sprint 2)

### Answer

ReAct is reactive — the model decides one tool call at a time, discovering its path as it goes. Plan-and-execute decomposes a goal into an explicit, ordered list of steps *before* executing anything, then runs each step (still through a ReAct loop, so each step can still use tools), passing earlier steps' results into later ones, and finally synthesizes one answer from all the results.

Trade-off: an upfront plan can't react to what a step discovers the way a pure ReAct loop can — which is why plan-and-execute nests a ReAct loop inside each step rather than replacing it. The benefit that justifies the extra machinery: the plan itself becomes inspectable, user-visible output, not just an internal decision.

---

## Q33. Structured output vs. prompt-instructed JSON — why does it matter? (Sprint 2)

### Answer

Prompt-instructed JSON (asking nicely in the prompt and parsing the text response) is fragile — the model can wrap it in prose or drift from the schema. Structured output passes a JSON Schema to the API itself; in strict mode, generation is grammar-constrained so the output cannot violate the schema.

Prefer structured output whenever a schema is available. `FaithfulnessService` (Module 5) uses the fragile prompt-instructed approach because it predates this capability — it's flagged as technical debt rather than treated as a permanent pattern, precisely so it gets revisited now that the real mechanism (`LLMProvider.generate_structured()`) exists.

---

## Q34. What is Reflection, and when should the loop stop? (Sprint 3)

### Answer

Reflection is a generate → critique → revise loop: produce an answer, have the model critique its own answer against the original question, and if unsatisfactory, revise and re-check — bounded by an iteration cap.

What happens at the cap matters and isn't automatically "fail": a tool loop that never produced an answer has genuinely failed, so raising is correct there. A reflection loop that never reaches "satisfactory" still has a real, usable answer sitting in hand — returning that last draft as a best-effort result is the right call, not an error.

---

## Q35. Is Reflection the same as the faithfulness/hallucination check from Module 5?

### Answer

No — same underlying idea (LLM-as-judge), different purpose and different place in the pipeline. `FaithfulnessService` is an **offline evaluation** check: it judges an answer *after the fact*, against retrieved context, for measurement purposes. `ReflectionService` is an **inline runtime** loop: it judges a candidate answer *before it's ever returned to the caller*, against the original question, as part of producing the answer.

---

## Q36. What does "memory" mean for an agent, and what should it actually store? (Sprint 4)

### Answer

Memory means carrying context across multiple separate requests — a real conversation, not just a single self-contained exchange each time. Concretely: give each conversation an id, load its prior turns before running the agent loop, and persist the new turn once an answer is produced.

The more interesting design question is *what* to store. An agent turn can involve a lot of internal machinery — tool calls, intermediate results. Storing only the human-visible exchange (the user's message and the final answer), not that internal machinery, is deliberate: it's simpler, it keeps the memory store free of any provider-specific format, and it matches what a person would actually mean by "the conversation so far."

---

## Q37. How is `InMemoryConversationMemory` similar to `InMemoryVectorStore`?

### Answer

Same story, one layer over. Both are an intentional first pass: build the interface (`VectorStore` / `ConversationMemory`), ship a process-local, non-persistent implementation now, and swap in a durable backend later (`PostgreSQL`+`pgvector` for vectors, Redis or PostgreSQL for conversation memory) without touching any code that calls the interface. It's the Provider Pattern's idea — depend on abstractions — applied to storage, not just LLM providers.

---

## Q38. What did LangGraph actually add, that hand-written code didn't already do? (Sprint 5)

### Answer

Two things, precisely: a `checkpointer` that persists graph state across calls keyed by a `thread_id` (the same capability `ConversationMemory` hand-built in Sprint 4, now framework-managed), and a recursion limit that serves the same role as the hand-rolled `max_iterations` guard from Sprint 1.

Everything else — *what* gets called (`LLMProvider.chat_with_tools()`, `Tool.execute()`) — is identical to `AgentService`. LangGraph only replaced the *control flow*: a hand-written `for` loop became graph nodes and a conditional edge. That's the point of building the loop by hand first — it makes it possible to say exactly what a framework did and didn't change, instead of taking it on faith.

---

## Q39. Why not let LangGraph nodes call a LangChain chat model directly, the way most LangGraph tutorials do? (Sprint 5)

### Answer

Because that would mean the LLM call itself — provider selection, tool-calling wire format — moves into LangChain's hands instead of the project's own `LLMProvider` abstraction. That's exactly the coupling the Provider Pattern (Decision 004) exists to prevent, and exactly the same isolation instinct that confines LangChain to `app/rag/` (Decision 013) — just applied to LangGraph and `app/agents/` instead.

The fix: graph nodes call `LLMProvider.chat_with_tools()` and `Tool.execute()` directly — the same calls `AgentService` makes. LangGraph becomes purely an orchestration layer over abstractions the project already owns, not a new place where a vendor SDK's shape leaks into business logic.

---

## Q40. What broke when installing `langgraph`, and what does that teach about dependency pinning? (Sprint 5)

### Answer

Installing latest `langgraph` (1.x) silently upgraded `langchain-core` to a version the already-pinned `langchain==0.3.27`/`langchain-openai==0.3.31`/`langchain-community==0.3.27` don't support (they all require `langchain-core<1.0.0`). `pip`'s resolver doesn't retroactively re-check already-installed packages' constraints against a new package's transitive upgrade.

The fix wasn't to unpin everything to "whatever's compatible" — that reintroduces the version drift pinning exists to prevent. It was to find the specific `langgraph` version (0.6.11) whose own dependency constraints stayed compatible with what was already pinned, then confirm with `pip check` before writing any code. Talking point: dependency conflicts inside one ecosystem (here, everything under the LangChain umbrella) are common precisely because packages share a core dependency that doesn't version in lockstep with each of them.

---

## Q41. Why is a specialist just a differently-configured `AgentService`, not a new class? (Sprint 6)

### Answer

Because the only things that make a "specialist" specialist are its tool set and its role — both of which `AgentService` already had a place for (`tools`, and now `system_prompt`). A Researcher is an `AgentService` with `KnowledgeBaseSearchTool` and a research-framed system prompt; a Writer is the same class with no tools and a writing-framed prompt. Inventing a `Specialist` base class or a `Role` enum on top of that would be an abstraction with nothing to abstract — the variation is entirely in configuration, not behavior.

---

## Q42. How does the Supervisor decide who acts next, and why is that not new machinery? (Sprint 6)

### Answer

The Supervisor looks at the transcript so far and asks a structured question: which specialist should act next (or is the task done), and what should they do? That's answered by `generate_structured()` — the exact same structured-output mechanism `Planner` (Sprint 2) and `Reflector` (Sprint 3) already used, just pointed at a routing decision instead of a plan or a critique. The graph orchestrating it is the same shape as Sprint 5's single-agent graph, just with two worker nodes behind the conditional edge instead of one. Multi-agent collaboration, built this way, isn't a new category of system — it's the same two tools (structured decisions, graph routing) applied one level up.

---

## Q43. Why no "Reviewer Agent," when the sketch in the architecture docs included one?

### Answer

Because it would have duplicated a capability that already exists. `ReflectionService` (Sprint 3) already does self-critique — generate, critique, revise. Adding a third specialist whose job is "review the answer" would be re-solving a problem Sprint 3 solved, under a different name, inside a different sprint. Recognizing that a "new" piece of a system is actually a capability already built elsewhere — and reusing it instead of rebuilding it — is as much a part of system design as building the new pieces are.

---

# Model Context Protocol (MCP)

## Q44. What is MCP?

### Answer

Model Context Protocol is an open standard for connecting AI models with external tools and resources.

Benefits:

- Standardised integrations
- Tool discovery
- Reusable ecosystem

---

## Q45. Why did an existing abstraction (`Tool`) turn out to map directly onto MCP, with no changes? (Sprint 1)

### Answer

`Tool` (built in Module 6, Sprint 1) was designed schema-first: name, description, a JSON Schema of parameters, and `execute()` — a contract about what a caller needs to know, not about any one caller's specific calling convention. MCP's tool registration wants exactly that same information (`inputSchema` is a JSON Schema). Because `Tool` was never coupled to OpenAI's specific tool-calling wire format — that coupling was deliberately kept inside the provider layer (Decision 004) — handing a `Tool` instance to a completely different protocol required zero changes to `Tool` itself, only a small adapter (`build_mcp_server()`) around it.

---

## Q46. Why use the low-level MCP `Server` API instead of the higher-level `FastMCP`? (Sprint 1)

### Answer

`FastMCP`'s `@mcp.tool()` decorator infers a tool's JSON Schema from a Python function's type hints — convenient when a tool is being defined fresh for MCP. But `Tool.parameters` already *is* an explicit JSON Schema; forcing it through type-hint inference has nothing to infer from (`execute(**kwargs)` has no fixed signature) and would fight, not reuse, work already done. The low-level `Server` API takes the schema directly via `types.Tool(inputSchema=...)`, matching the shape of the problem exactly. Confirmed with a smoke test before writing any production code, rather than assumed.

---

## Q47. How does an MCP client turn a remote tool into something an agent can use? (Sprint 2)

### Answer

Three steps: connect (spawn or dial the server and open a session), discover (`session.list_tools()` returns each tool's name, description, and JSON Schema), and adapt (wrap each discovered tool in something that implements the project's own `Tool` interface — `MCPToolAdapter` — so `execute()` just calls `session.call_tool()` under the hood). The key property: none of this code hard-codes a tool name anywhere. Whatever the server happens to expose is what gets discovered and used.

---

## Q48. Why is the MCP client side described as a "mirror image" of the server side? (Sprint 2)

### Answer

Sprint 1 built an adapter that takes a local `Tool` and makes it *look like* an MCP tool to a client (`build_mcp_server()`). Sprint 2 built the opposite adapter — one that takes a remote MCP tool and makes it *look like* a local `Tool` (`MCPToolAdapter`) to the rest of the codebase. Same translation, opposite direction, both sides of the same interface. Recognizing that symmetry before writing code is what kept Sprint 2 small — questions like "how do we represent a tool's schema" or "what happens when a tool call fails" were already answered in Sprint 1, just facing the other way.

The payoff: `AgentService` needs zero changes to use a mix of local and MCP-discovered tools in the same `tools` list. It was never written to know or care where a tool's `execute()` actually runs — local, or over stdio to a subprocess.

---

## Q49. Why wasn't stdio transport already "remote execution"? (Sprint 3)

### Answer

Stdio is a subprocess pipe — the client spawns the server as a child process on the same machine and talks to it over stdin/stdout. Nothing crosses an actual network boundary; the server doesn't outlive the connection or exist independently of it. "Remote execution" means a standing service, reachable by address, running independently of whoever connects to it — which is what Sprint 3's streamable-HTTP transport actually provides: the MCP server runs on its own port as a persistent process, and any client that knows the URL can connect, call tools, and disconnect without the server's lifecycle depending on them at all.

---

## Q50. What changed, and what didn't, when switching from stdio to HTTP transport? (Sprint 3)

### Answer

Only the connection step: `connect_stdio_mcp_server()` became `connect_http_mcp_server()`, swapping `stdio_client` for `streamable_http_client`. Everything downstream of a `ClientSession` — `discover_tools()`, `MCPToolAdapter`, `Tool` itself — was completely unaware of which transport it was running over. That's the payoff of a properly layered protocol library: transport is the library's concern, not something that should leak into code that discovers and uses tools. If switching transports required touching business logic, the abstraction boundary would have been drawn in the wrong place.

---

## Q51. Why did wiring MCP tools into an agent need a new pattern (`lifespan`) instead of another `@lru_cache` function? (Sprint 3)

### Answer

Every dependency before this was a synchronous, lazy constructor — cheap to build, safe to build on first access. Connecting to a network service and discovering its tools is neither: it's async, it can fail, and it needs to happen once at startup and be cleanly torn down at shutdown, not whenever the first request happens to touch it. FastAPI's `lifespan` context manager is built for exactly that shape of problem. The general principle: a dependency's *lifecycle* (constructor-cheap vs. needs-real-setup-and-teardown) determines which pattern it belongs in — forcing a lifecycle-managed resource into a lazy-singleton pattern either blocks somewhere awkward or pushes connection risk onto whichever request arrives first.

---

# System Design Questions

## Q52. How would you design an enterprise AI assistant?

### Talking Points

- Layered architecture
- Provider abstraction
- RAG
- Vector database
- Agents
- Tool calling
- Evaluation
- Monitoring
- Deployment

---

## Q53. How do you reduce hallucinations?

### Talking Points

- Better prompts
- RAG
- Citations
- Evaluation
- Context management
- Grounding

---

## Q54. How would you support multiple LLM providers?

### Answer

Introduce an abstraction.

```
LLMProvider

├── OpenAIProvider

├── AnthropicProvider

├── BedrockProvider
```

Business logic depends only on the interface.

---

## Q55. What would you monitor in production?

### Metrics

- Request latency
- Token usage
- API cost
- Error rate
- Retrieval quality
- Hallucination rate
- Model availability

---

## Q56. You scoped Module 9 (observability) in detail and then didn't build it — why?

### Answer

Because scoping revealed it had no payoff yet, not because it ran out of time. Cost tracking, latency monitoring, model comparison, and prompt versioning all share one precondition: they only create value against *ongoing real traffic*, or when something *automated* acts on what they measure. This project has neither — no production traffic, and provider selection is a hard-coded constructor call, not a runtime decision anything could route against. Building the tracking apparatus now would mean carrying a real, recurring cost (a pricing table alone goes stale) with nothing observing it. The right engineering call was to design it, confirm it was sound, and then not build it — "we might need this later" isn't sufficient justification on its own, especially for infrastructure whose entire value is watching something over time.

---

## Q57. If observability wasn't worth building, why build `ClaudeProvider` at all?

### Answer

Different shape of value. `ClaudeProvider` isn't infrastructure waiting for future traffic — it's a one-time proof that an abstraction already believed to be sound (the Provider Pattern, built in Module 4) actually holds up against a second real vendor, not just a hypothetical one. It cost one file and zero changes to any of its 10 existing consumers. And it leaves a door open cheaply: if provider choice ever needs to become a real decision, swapping is a config change, not a rewrite. That's a materially smaller bet than building a tracking system for traffic that doesn't exist yet.

---

## Q58. What would make Module 9 worth revisiting?

### Answer

Two concrete triggers, not a timeline: real production traffic worth watching (most likely once Module 8's deployment work ships this to somewhere users actually hit it), or provider selection becoming a genuine runtime decision rather than a hard-coded one. Absent either, the module stays deferred — revisiting it earlier would mean building for a hypothetical, which is exactly what got rejected here.

---

## Q59. Why was Module 10 (the frontend) taken up before Module 8 (infrastructure) or a completed Module 9?

### Answer

The user's own call, and it's a defensible one: nothing in Modules 1–7's architecture (routers → services → providers/RAG/agents/MCP) depends on Docker, Terraform, AWS, or an observability layer existing first. A browser client only needs a running API to call — it doesn't need that API containerized, deployed, or measured. Module 8 (infra) and Module 9 (deferred) are both "how this gets operated and watched," which is orthogonal to "does a real UI exist yet." Sequencing bootcamp modules by actual dependency rather than by their listed order is itself the more realistic engineering practice — real projects rarely execute a roadmap in the order it was written.

---

## Q60. Why a standalone static frontend instead of having FastAPI serve it (e.g. via Jinja2 templates or a `StaticFiles` mount)?

### Answer

Because the two are genuinely different architectures with different consequences, not a style preference. A FastAPI-served frontend means one process, one origin, no CORS — simpler locally, but it couples deployment: the frontend can't be pushed to a CDN independently, can't be cached at the edge, and every backend deploy redeploys the UI whether it changed or not. A standalone static site decouples those lifecycles — which is how frontends are actually deployed in most production systems (a CDN/static host, separate from the API) — at the cost of needing CORS, since the browser now treats them as different origins. This project chose to pay that cost deliberately, to practice the pattern that matches real deployments rather than the path of least local friction.

---

## Q61. Why did FastAPI startup fail the first time the frontend and backend were run together, and what does that reveal?

### Answer

Not a frontend bug — a pre-existing dependency surfacing in a new context. Since Module 7 Sprint 3, `create_app()`'s `lifespan` connects to the MCP HTTP server at startup and fails hard if it isn't reachable; that was already true before the frontend existed. Running three processes for the first time (MCP server, backend, frontend) just made an ordering mistake newly possible: starting the backend before the MCP server produces an `ExceptionGroup`/`httpx.ConnectError` that reads as unrelated to its actual cause unless you already know the chain. The lesson is general — adding a new process to a system doesn't create new dependencies by itself, but it multiplies the ways an existing one can be triggered by the wrong startup order.

---

## Q62. How would you debug a report that "the frontend can't reach the backend," given everything looks fine in the backend logs?

### Answer

Start in the browser, not the server. If CORS is blocking the response, the backend logs will often show a normal 200 — the request succeeded, the browser just refuses to hand the response to the page's JavaScript. `curl`ing the same endpoint will also succeed, because `curl` isn't a browser and CORS isn't a server-side check; the block happens client-side, after a valid response comes back. The actual signal is in the browser's own console (a CORS error naming the blocked origin) — checking that first would have ruled out or confirmed CORS in seconds, versus a lot of unproductive time staring at server-side logs that were never going to show the problem.

---

## Q63. What's the real difference between testing a JSON API endpoint and testing a browser UI?

### Answer

The client itself. A JSON API's real client is "any HTTP caller" — a `curl` request or a Python `httpx` call is a faithful stand-in, because correctness is fully captured by the response body and status code. A browser UI's real client is a browser executing real JavaScript against real CSS — `curl` hitting the same endpoint proves the API works, but says nothing about whether the page's script parsed the response, updated the right element, or whether it's even readable once styled. That gap is why this project's frontend was verified with an actual headless Chromium browser (via Playwright) — loading the real page, checking the console for errors, and inspecting a screenshot — rather than treating a passing `curl` command as proof the feature works.

---

## Q64. This project has two endpoints that can both power a "chat" feature — `POST /chat/stream` and `POST /agents/chat`. Why aren't they interchangeable, and which did the chat UI use?

### Answer

They optimize for different things. `POST /chat/stream` (Module 4's `ChatService`/`StreamingService`) streams tokens live as they generate, but is stateless — no `conversation_id`, so a follow-up message carries zero context from the previous one. `POST /agents/chat` (Module 6's `AgentService`) has real cross-turn memory via `conversation_id`, but returns its answer all at once — there's no streaming variant of the agent loop yet. The Sprint 2 chat UI wired to `/chat/stream`, trading away conversation memory for the more visibly important property at this stage: text appearing live as the model generates it. Adding memory to the streaming path later would mean a backend change (a streaming `AgentService` variant), not a frontend one.

---

## Q65. Why did adding `apiPostStream()` to `js/api.js` require a new function instead of extending the existing `request()`/`apiPost()` helper?

### Answer

Because the response shapes are fundamentally different, not just different call sites. `apiGet`/`apiPost` both call `response.json()` — the entire body is buffered by `fetch()` internally and parsed as one JSON value once the response completes. A streamed `text/plain` body has no single JSON value to parse; it needs `response.body.getReader()`, read in a loop, with each chunk handed to a callback as it arrives — the whole point is *not* waiting for the full response. Retrofitting `request()` to handle both would mean branching internally on whether the caller wants a parsed JSON object or a stream of raw chunks — two different contracts pretending to be one function. A second, explicit function keeps each helper's contract simple and matches what it's actually doing.

---

## Q66. Why does `js/api.js` have three separate "POST" helpers (`apiPost`, `apiPostStream`, `apiPostForm`) instead of one function with an options flag?

### Answer

Because they don't share a wire contract, only an HTTP verb. `apiPost` sends a JSON body and parses a JSON response in one step. `apiPostStream` sends a JSON body but reads the response as a sequence of raw chunks over time, never calling `response.json()` at all. `apiPostForm` sends a `FormData` body and must *not* set a `Content-Type` header — the browser generates the multipart boundary itself, and setting it manually breaks the upload. Collapsing these into one function with a `mode` parameter would hide three genuinely different behaviors behind one signature, for the sake of a coincidence (all three happen to use `POST`). The right question when two things look similar isn't "do they share a verb" — it's "do they share a contract."

---

## Q67. The knowledge base UI only accepts PDF uploads. Is that a frontend limitation or a backend one, and how would you extend it?

### Answer

Backend. `POST /documents/upload` resolves a loader by file extension via `DocumentLoaderFactory`, which today only has `PDFLoader` registered — a gap dating back to Module 5, not introduced by this sprint. The frontend's `accept=".pdf"` on the file input and the visible "PDF only" hint are UX guidance, not enforcement — they steer users away from a failure that already exists server-side, and if someone bypasses them, the backend's real error (`"No loader registered for '.txt'."`) still surfaces correctly through the UI rather than failing silently. Extending it means registering additional loaders (DOCX/HTML/Markdown) in `DocumentLoaderFactory`, unrelated to anything in `frontend/`.

---

## Q68. How did you verify the file upload feature actually worked, given the backend only accepts PDFs?

### Answer

The first verification attempt used a `.txt` file and failed — correctly, because the backend has no loader for that extension. That wasn't a bug to fix; it revealed the test data was wrong for what the feature needed. Real verification required a real PDF: since no PDF-generation library or fixture file existed in the project yet, one was generated using the exact hand-crafted-PDF technique the backend's own test suite already uses (`tests/conftest.py`'s `write_minimal_pdf()` — a minimal valid PDF written as a raw byte template, no external library). That file, uploaded through the actual browser UI, produced a real indexed chunk; searching for its content afterward returned a real similarity-scored result. The lesson: testing a file-upload feature with a placeholder file only proves the form submits — it doesn't prove the feature works, because "works" depends on the file actually being the type the system is built to handle.

---

# Practical Questions

You should be able to explain the architecture you built during this bootcamp, including:

- Why routers are thin
- Why services contain business logic
- Why providers wrap SDKs
- Why LangChain is isolated in the RAG layer
- Why PostgreSQL + pgvector was selected
- How streaming works
- How dependency injection is implemented
- How RAG improves answer quality

---

# Interview Advice

Interviewers are usually more interested in **why** you made an engineering decision than whether you used a particular library.

When discussing this project:

- Explain the problem.
- Explain the trade-offs considered.
- Explain why the chosen solution fits the requirements.
- Be prepared to discuss how the architecture could evolve as the system grows.

A clear explanation of your design decisions often demonstrates more engineering maturity than simply listing technologies.
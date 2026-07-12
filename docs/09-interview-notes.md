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

# Model Context Protocol (MCP)

## Q30. What is MCP?

### Answer

Model Context Protocol is an open standard for connecting AI models with external tools and resources.

Benefits:

- Standardised integrations
- Tool discovery
- Reusable ecosystem

---

# System Design Questions

## Q31. How would you design an enterprise AI assistant?

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

## Q32. How do you reduce hallucinations?

### Talking Points

- Better prompts
- RAG
- Citations
- Evaluation
- Context management
- Grounding

---

## Q33. How would you support multiple LLM providers?

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

## Q34. What would you monitor in production?

### Metrics

- Request latency
- Token usage
- API cost
- Error rate
- Retrieval quality
- Hallucination rate
- Model availability

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
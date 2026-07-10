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

# Model Context Protocol (MCP)

MCP provides a standard way for AI applications to discover and interact with external tools.

Benefits

- Standardised tool interfaces
- Easier integration
- Reusable tool ecosystem

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
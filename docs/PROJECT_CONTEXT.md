# Enterprise AI Assistant
## Project Context

> This file is the primary source of context for continuing the AI Engineer Bootcamp in a new ChatGPT conversation.

---

# Project Goal

Build a production-quality Enterprise AI Assistant while learning modern AI Engineering through hands-on development.

The emphasis is on architecture, maintainability, scalability and production practices rather than toy examples.

The completed project should demonstrate the skills expected of an AI Engineer.

---

# Current Status

Current Module:

Module 5 – Enterprise RAG

Current Sprint:

Sprint 1

Current Increment:

Increment 1 – LangChain Documents

Status:

Ready to begin LangChain integration.

---

# Bootcamp Modules

| Module | Status |
|---------|--------|
| Module 1 - LLM Fundamentals | Complete |
| Module 2 - Prompt Engineering | Complete |
| Module 3 - Semantic Search | Complete |
| Module 4 - Enterprise AI Platform | Complete |
| Module 5 - Enterprise RAG | Current |
| Module 6 - AI Agents | Pending |
| Module 7 - Model Context Protocol (MCP) | Pending |
| Module 8 - Production Infrastructure | Pending |
| Module 9 - Evaluation & Observability | Pending |
| Module 10 - Enterprise AI Assistant | Pending |

---

# Architecture Principles

The project follows Layer-Based Architecture.

```
API
    ↓
Services
    ↓
Providers
    ↓
External APIs
```

LangChain is used only inside the RAG layer.

Routers never communicate directly with providers.

Business logic belongs in Services.

External SDKs are wrapped by Providers.

---

# Coding Standards

- Python 3.12+
- FastAPI
- Async first
- SOLID principles
- Strong typing
- Pydantic validation
- Thin routers
- Service layer
- Provider abstraction
- Dependency Injection
- Complete file replacements during implementation
- Git commit after every completed increment

---

# Current Folder Structure

```
enterprise-ai-assistant/

backend/
    app/
        api/
        core/
        providers/
        services/
        dependencies/
        rag/
        database/
        schemas/
        models/
        agents/
        tools/
        main.py

frontend/

infrastructure/

docs/
```

---

# Technologies

Backend

- FastAPI
- Pydantic
- OpenAI SDK
- Structlog

Future

- LangChain
- LangGraph
- PostgreSQL
- pgvector
- SQLAlchemy
- Docker
- Terraform
- AWS

---

# Completed Features

Application configuration

- Environment variables
- Typed configuration
- Pydantic Settings

Application Factory

- create_app()

Logging

- Structured logging
- Configurable log levels

Health Endpoints

- /
- /live
- /ready
- /health

Dependency Injection

- FastAPI Depends
- Provider injection

Provider Pattern

- LLMProvider interface
- OpenAIProvider implementation

Service Layer

- ChatService
- StreamingService

Chat API

- POST /chat

Streaming

- Provider streaming
- StreamingService
- Streaming endpoint

---

# Design Decisions

Layer-based architecture.

LangChain is isolated within the RAG layer.

Use official OpenAI SDK.

Use FastAPI Dependency Injection.

One responsibility per class.

Thin routers.

Async throughout.

No framework-specific code inside routers.

---

# Current Objective

Begin Module 5.

Implement Enterprise RAG.

First milestone:

Upload a document and represent it as LangChain Document objects.

---

# Upcoming Milestones

1. LangChain Documents
2. Recursive Text Splitter
3. Embeddings
4. Vector Store
5. Retriever
6. Question Answering
7. Source Citations
8. PostgreSQL + pgvector
9. Hybrid Search
10. Evaluation

---

# Long-Term Goal

Deliver a production-ready Enterprise AI Assistant capable of:

- Chat
- Enterprise RAG
- Agents
- Tool Calling
- MCP
- Evaluation
- AWS Deployment

This repository should represent production-quality AI Engineering work suitable for a professional portfolio.

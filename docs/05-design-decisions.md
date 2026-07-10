# Design Decisions

> This document records the key architectural decisions made during the development of the Enterprise AI Assistant.

Unlike implementation details, these decisions are intended to remain stable throughout the lifetime of the project.

---

# Decision 001

## Use Layer-Based Architecture

**Status**

Accepted

---

### Decision

Organize the application into horizontal layers.

```
API

↓

Services

↓

Providers

↓

External Systems
```

---

### Reason

- Clear separation of concerns
- Easier to learn
- Easier to test
- Scales well
- Widely used in enterprise applications

---

### Consequences

Benefits

- Thin routers
- Reusable services
- Framework independence
- Testability

Trade-offs

- More files
- Slightly more boilerplate

---

# Decision 002

## Thin Routers

**Status**

Accepted

---

### Decision

Routers only handle HTTP.

Responsibilities

- Receive request
- Validate request
- Call service
- Return response

Routers must not contain:

- Business logic
- SQL
- OpenAI SDK
- LangChain
- Prompt construction

---

### Reason

Keeps API layer small and maintainable.

---

# Decision 003

## Service Layer

**Status**

Accepted

---

### Decision

Business logic belongs inside dedicated services.

Examples

```
ChatService

StreamingService

DocumentService

RetrievalService

AgentService
```

---

### Reason

Separates business rules from HTTP and infrastructure.

---

### Consequences

Business logic can be reused by:

- REST API
- CLI
- Scheduled Jobs
- Background Workers
- Tests

---

# Decision 004

## Provider Pattern

**Status**

Accepted

---

### Decision

External SDKs are wrapped by Providers.

```
LLMProvider

↓

OpenAIProvider
```

Future providers

```
AnthropicProvider

BedrockProvider

GeminiProvider

OllamaProvider
```

---

### Reason

Avoid coupling business logic to vendor SDKs.

---

### Benefits

Easy provider replacement.

Cleaner testing.

Future proof.

---

# Decision 005

## Dependency Injection

**Status**

Accepted

---

### Decision

Use FastAPI Dependency Injection throughout the project.

```
Depends(...)
```

Objects are never instantiated inside routers.

---

### Reason

- Loose coupling
- Easier testing
- Cleaner architecture

---

# Decision 006

## Async First

**Status**

Accepted

---

### Decision

Use async programming for all I/O.

Examples

- HTTP
- Database
- OpenAI
- File access
- Streaming

---

### Reason

Improved scalability.

Modern Python best practice.

---

# Decision 007

## Strong Typing

**Status**

Accepted

---

### Decision

Every public method should include type hints.

Example

```
async def chat(
    prompt: str,
) -> str
```

---

### Reason

- Better IDE support
- Better readability
- Safer refactoring

---

# Decision 008

## Pydantic Everywhere

**Status**

Accepted

---

### Decision

All external input is validated using Pydantic.

Includes

- API Requests
- API Responses
- Configuration

---

### Reason

Validation should happen automatically.

---

# Decision 009

## Configuration Management

**Status**

Accepted

---

### Decision

Configuration is loaded through Pydantic Settings.

```
.env

↓

Settings

↓

Application
```

---

### Reason

Single source of truth.

Environment-specific configuration.

No hardcoded secrets.

---

# Decision 010

## Application Factory

**Status**

Accepted

---

### Decision

The application is created through:

```
create_app()
```

instead of:

```
app = FastAPI()
```

inside main.py.

---

### Reason

Supports:

- Startup configuration
- Middleware
- Testing
- Future expansion

---

# Decision 011

## Structured Logging

**Status**

Accepted

---

### Decision

Use Structlog.

Avoid print().

---

### Reason

Production-ready logging.

Machine readable.

Cloud friendly.

---

# Decision 012

## Health Endpoints

**Status**

Accepted

---

### Decision

Maintain three operational endpoints.

```
/live

/ready

/health
```

---

### Reason

Supports

- Docker
- Kubernetes
- Load Balancers
- Monitoring

---

# Decision 013

## LangChain Boundary

**Status**

Accepted

---

### Decision

LangChain exists only inside:

```
app/rag/
```

Never inside:

- Routers
- Services
- Providers

---

### Reason

Avoid framework coupling.

Maintain architecture ownership.

---

### Consequences

Future replacement of LangChain is possible with minimal changes.

---

# Decision 014

## Official SDKs

**Status**

Accepted

---

### Decision

Use official SDKs whenever available.

Examples

- OpenAI SDK
- Anthropic SDK
- AWS SDK

---

### Reason

Better support.

Better documentation.

Fewer compatibility issues.

---

# Decision 015

## PostgreSQL + pgvector

**Status**

Accepted

---

### Decision

Use PostgreSQL with pgvector.

Do not introduce a dedicated vector database unless justified.

---

### Reason

- Mature ecosystem
- Lower operational complexity
- Excellent production support
- Fits project scale

---

# Decision 016

## One Responsibility Per Class

**Status**

Accepted

---

### Decision

Each class should have exactly one responsibility.

Examples

```
ChatService

StreamingService

DocumentService

EmbeddingService
```

Avoid large "God classes."

---

### Reason

Simpler testing.

Better maintainability.

Improved readability.

---

# Decision 017

## Complete File Replacements

**Status**

Accepted

---

### Decision

During the bootcamp, implementation instructions provide complete file contents instead of partial snippets.

---

### Reason

Reduces confusion.

Avoids merge mistakes.

Ensures every student reaches the same architecture.

---

# Decision 018

## Feature-Driven Learning

**Status**

Accepted

---

### Decision

Each sprint must deliver a user-visible capability.

Examples

- Upload a document
- Ask questions
- Search PDFs
- Build an agent

Not just internal infrastructure.

---

### Reason

Keeps learning practical.

Produces a demonstrable portfolio.

Maintains motivation.

---

# Decision 019

## Documentation as Code

**Status**

Accepted

---

### Decision

Documentation evolves alongside the project.

Every sprint updates:

- Progress
- Architecture
- Changelog
- Learning Notes

---

### Reason

The repository—not the chat history—is the source of truth.

---

# Decision 020

## Bootcamp Objective

**Status**

Accepted

---

### Decision

The goal is **not** to become an expert in a single framework.

The goal is to become an AI Engineer capable of designing, building, deploying, and maintaining production AI systems.

Frameworks are tools.

Architecture is the skill.

---

# Summary

The Enterprise AI Assistant is guided by the following principles:

- Layered Architecture
- SOLID Principles
- Dependency Injection
- Provider Pattern
- Service Layer
- Async First
- Strong Typing
- Pydantic Validation
- Official SDKs
- LangChain isolated within the RAG layer
- Feature-driven development
- Production-ready engineering practices

These decisions should remain stable unless there is a compelling architectural reason to revisit them.
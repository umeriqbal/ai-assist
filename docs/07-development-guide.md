# Development Guide

> This document describes how to set up, run, test, and contribute to the Enterprise AI Assistant.

This guide should allow a new developer to clone the repository and begin development in a few minutes.

---

# Prerequisites

Install the following software before starting.

| Software | Version |
|-----------|----------|
| Python | 3.12+ |
| Git | Latest |
| VS Code | Latest |
| Docker Desktop | Latest (later modules) |
| PostgreSQL | Later modules |
| Node.js | Latest LTS (frontend later) |

---

# Clone Repository

```bash
git clone https://github.com/<your-account>/enterprise-ai-assistant.git

cd enterprise-ai-assistant
```

---

# Backend Setup

Navigate to the backend.

```bash
cd backend
```

Create a virtual environment.

macOS/Linux

```bash
python3 -m venv .venv
```

Windows

```powershell
python -m venv .venv
```

---

# Activate Virtual Environment

macOS/Linux

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Verify

```bash
which python
```

Expected

```
backend/.venv/bin/python
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

Upgrade pip if required.

```bash
python -m pip install --upgrade pip
```

---

# Environment Variables

Create

```
backend/.env
```

Example

```env
OPENAI_API_KEY=your_openai_key

OPENAI_CHAT_MODEL=gpt-4.1

LOG_LEVEL=INFO
```

Never commit:

- .env
- API Keys
- Secrets

---

# Run Application

From

```
backend/
```

Execute

```bash
python -m uvicorn app.main:app --reload
```

Expected output

```
Application startup complete.

Uvicorn running on:

http://127.0.0.1:8000
```

---

# API Documentation

Open

```
http://127.0.0.1:8000/docs
```

Swagger UI

---

OpenAPI JSON

```
http://127.0.0.1:8000/openapi.json
```

---

# Health Checks

Verify

```
GET /

GET /health

GET /live

GET /ready
```

Expected

HTTP 200

---

# Chat Endpoint

Request

```http
POST /chat
```

Example

```json
{
    "prompt": "Explain embeddings."
}
```

---

# Streaming Endpoint

Request

```http
POST /chat/stream
```

Example

```bash
curl -N \
-X POST \
http://127.0.0.1:8000/chat/stream \
-H "Content-Type: application/json" \
-d '{
    "prompt":"Explain RAG"
}'
```

---

# Recommended VS Code Extensions

Install

- Python
- Pylance
- Ruff
- Black Formatter
- GitLens
- Docker
- Markdown All in One

---

# Code Formatting

Format code before committing.

Example

```bash
black .
```

Future

```bash
ruff check .

ruff format .
```

---

# Project Structure

```
backend/

app/

api/

core/

providers/

services/

rag/

schemas/

database/

agents/

tools/
```

Do not create additional top-level folders without an architectural review.

---

# Git Workflow

Create a feature branch.

```bash
git checkout -b feature/module-05-rag
```

Commit frequently.

Example

```bash
git add .

git commit -m "feat: add LangChain document service"
```

Push

```bash
git push origin feature/module-05-rag
```

---

# Commit Message Convention

Use conventional commits.

Examples

```
feat:

fix:

refactor:

docs:

test:

perf:

chore:
```

Example

```
feat: implement recursive text splitter

fix: handle empty prompts

docs: update architecture
```

---

# Testing

Run all tests

```bash
pytest
```

Future

Run only unit tests

```bash
pytest tests/unit
```

Integration tests

```bash
pytest tests/integration
```

API tests

```bash
pytest tests/api
```

---

# Logging

Logs are configured through Structlog.

Log level

```
LOG_LEVEL=INFO
```

Future

```
DEBUG

WARNING

ERROR
```

---

# Debugging

Useful commands

Current Python

```bash
which python
```

Installed packages

```bash
pip list
```

Installed OpenAI package

```bash
pip show openai
```

Installed LangChain

```bash
pip show langchain
```

---

# Common Issues

## ModuleNotFoundError

Ensure the server is started from

```
backend/
```

Correct

```bash
python -m uvicorn app.main:app --reload
```

---

## Virtual Environment Not Active

Verify

```bash
which python
```

Expected

```
backend/.venv/bin/python
```

---

## Environment Variables Missing

Verify

```
backend/.env
```

exists.

---

## OpenAI Authentication

Check

```
OPENAI_API_KEY
```

Restart the server after updating the `.env` file.

---

# Development Rules

Always

- Use async where appropriate.
- Keep routers thin.
- Keep business logic in services.
- Wrap SDKs in providers.
- Validate input with Pydantic.
- Write meaningful commit messages.
- Update documentation after each sprint.

Never

- Call the OpenAI SDK directly from a router.
- Put business logic inside routers.
- Hard-code secrets.
- Commit `.env`.
- Skip type hints on public methods.

---

# Daily Development Workflow

```
Pull latest changes

↓

Activate virtual environment

↓

Implement feature

↓

Run application

↓

Test manually

↓

Run automated tests

↓

Update documentation

↓

Commit

↓

Push
```

---

# Bootcamp Workflow

Each module follows the same pattern.

```
Sprint

↓

Increment

↓

Implementation

↓

Testing

↓

Architecture Review

↓

Documentation

↓

Git Commit

↓

Next Increment
```

This process is followed throughout the entire AI Engineer Bootcamp to reinforce production-quality engineering practices alongside AI development.
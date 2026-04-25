# Advanced FastAPI LLM Backend

A production-ready backend system built with FastAPI demonstrating async programming, LLM integration, caching, database persistence, and clean architecture.

---

## Features

*  Async FastAPI APIs
*  LLM integration using Groq
*  Parallel execution using asyncio
*  Retry with exponential backoff
*  Timeout handling
*  Redis caching (TTL-based)
*  PostgreSQL persistence
*  Structured logging with rotation
*  Clean architecture (API → Service → Repository → Client)

---

##  Architecture

Client → FastAPI → Service → Redis → LLM → PostgreSQL

---

##  Project Structure

```
api/            # Routes
services/       # Business logic
clients/        # External APIs (Groq)
repositories/   # DB & Redis access
db/             # Database config
models/         # DB models
schemas/        # Request/response schemas
utils/          # Logger, helpers
```

---

## Tech Stack

* FastAPI
* asyncio
* Redis
* PostgreSQL
* SQLAlchemy (async)
* Groq SDK
* Python logging

---

## Setup

```bash
git clone <repo>
cd project
pip install -r requirements.txt
```

---

## Environment Variables

Create `.env` file:

```
GROQ_API_KEY=your_api_key
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/ask_ai
```

---

## Run

```bash
uvicorn main:app --reload
```

---

## API Endpoints

### Health Check

```
GET /health
```

### Ask LLM

```
POST /ask
{
  "question": "Explain Python"
}
```

---

## Key Concepts Demonstrated

* Async vs Sync execution
* Concurrency control (Semaphore)
* Caching strategies
* Retry & resilience patterns
* Clean architecture design
* Logging & observability

---

## Use Case

This project simulates a scalable GenAI backend where LLM calls are optimized using caching, retries, and async execution.

---

## Author

Pramod Waghmare

# Advanced FastAPI LLM Backend

A production-ready backend system built with FastAPI demonstrating async programming, LLM integration, caching, database persistence, and clean architecture.

---

## Features

* Async FastAPI APIs
* LLM integration using Groq
* Parallel execution using asyncio
* Retry with exponential backoff
* Timeout handling
* Redis caching (TTL-based)
* PostgreSQL persistence
* Structured logging with rotation
* Clean architecture (API → Service → Repository → Client)

---

## Architecture

Client → FastAPI → Service → Redis (cache) → LLM → PostgreSQL (storage)

---

## Project Structure

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
git clone https://github.com/waghmarepatil/Ask-AI.git
cd Ask-AI
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_api_key
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ask_ai
```

---

## Start Dependencies

### Redis

Install and start Redis:

```bash
brew install redis
brew services start redis
```

Verify:

```bash
redis-cli ping
```

Expected output:

```
PONG
```

---

### PostgreSQL

Install and start PostgreSQL:

```bash
brew install postgresql
brew services start postgresql
```

Create database:

```bash
psql postgres
```

```sql
CREATE DATABASE ask_ai;
```

---

## Run Application

```bash
uvicorn main:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

---

## API Endpoints

### Health Check

```
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

### Ask LLM

```
POST /ask
```

Request:

```json
{
  "question": "Explain Python"
}
```

Response:

```json
{
  "question": "Explain Python",
  "answer": "Python is a high-level, interpreted programming language..."
}
```

---

## Example cURL

```bash
curl -X POST http://127.0.0.1:8000/ask \
-H "Content-Type: application/json" \
-d '{"question": "Explain Python"}'
```

---

## Key Concepts Demonstrated

* Async vs Sync execution
* Concurrency control (Semaphore)
* Caching strategies
* Retry and resilience patterns
* Timeout handling
* Clean architecture design
* Logging and observability

---

## Use Case

This project simulates a scalable GenAI backend where LLM calls are optimized using caching, retries, and asynchronous execution.

---

## Future Improvements

* Rate limiting using Redis
* Streaming LLM responses
* Multi-model fallback strategy
* Metrics and monitoring (Prometheus, Grafana)
* Background processing

---

## Author

Pramod Waghmare

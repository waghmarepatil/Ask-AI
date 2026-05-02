# Advanced FastAPI LLM Backend

A production-style backend system with LLM + RAG support.

---

## Features

* FastAPI async APIs
* Groq LLM integration
* Redis caching (no TTL)
* PostgreSQL persistence
* RAG with PDF support
* FAISS vector search
* Context caching optimization
* Retry + timeout + concurrency control
* Structured logging

---

## Architecture

Client → FastAPI → Service →
→ Redis (cache)
→ RAG (PDF → embeddings → FAISS)
→ LLM
→ PostgreSQL

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Environment Variables

```
GROQ_API_KEY=your_key
DATABASE_URL=postgresql+asyncpg://...
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## Run

```bash
uvicorn main:app --reload
```

---

## API

### Health

GET /health

---

### Chat (LLM + RAG)

POST /chat

---

## Example: Normal LLM

```bash
curl -X POST http://localhost:8000/chat \
  -F "question=Explain Python decorators"
```

---

## Example: RAG (PDF)

```bash
curl -X POST http://localhost:8000/chat \
  -F "question=Summarize this document" \
  -F "file=@sample.pdf"
```

---

## How it works

### Without file

→ Direct LLM call

### With file

→ RAG pipeline → context → LLM

---

## Key Concepts

* Async programming
* Dependency injection
* RAG architecture
* Vector search (FAISS)
* Caching strategy
* Retry + timeout

---

## Future Improvements

* Persistent vector DB
* Multi-document RAG
* Streaming
* Monitoring

---

## Author

Pramod Waghmare

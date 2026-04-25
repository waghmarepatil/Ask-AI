# System Architecture – Ask-AI

This document describes the architecture, components, and data flow of the Ask-AI backend system.

---

## Overview

Ask-AI is a FastAPI-based backend designed to integrate:

* Large Language Model (Groq)
* Redis for caching
* PostgreSQL for persistence
* Asynchronous processing
* Structured logging

The system is built with a focus on performance, scalability, and reliability.

---

## High-Level Architecture

```
Client
  ↓
FastAPI (API Layer)
  ↓
Service Layer (LLMService)
  ↓
 ├── Redis (Cache)
 ├── Groq (LLM API)
 └── PostgreSQL (Database)
```

---

## Layers Explained

### 1. API Layer (`api/`)

* Handles HTTP requests and responses
* Validates input/output using Pydantic schemas
* Injects dependencies such as database sessions

Example:

```
POST /ask
```

---

### 2. Service Layer (`services/`)

* Contains core business logic
* Responsible for:

  * Cache lookup
  * Retry mechanism
  * Timeout handling
  * Concurrency control (Semaphore)
  * Orchestrating data flow

---

### 3. Client Layer (`clients/`)

* Handles communication with external services
* Example: Groq LLM client
* Uses thread offloading (`asyncio.to_thread`) for non-blocking execution

---

### 4. Repository Layer (`repositories/`)

#### Redis Repository

* Provides cache access (GET/SET)
* Handles JSON serialization/deserialization
* Supports TTL-based expiration

#### Database Repository

* Persists question and answer pairs
* Uses async SQLAlchemy sessions

---

### 5. Database Layer (`db/`, `models/`)

* PostgreSQL as primary storage
* Async engine using `asyncpg`
* ORM via SQLAlchemy

---

## Request Flow

1. Client sends request to `/ask`
2. API validates input
3. Service generates cache key
4. Redis lookup:

   * If hit, return cached response
   * If miss, proceed to LLM call
5. LLM call (Groq):

   * Wrapped with retry logic (3 attempts)
   * Timeout protection
   * Controlled concurrency using semaphore
6. Response storage:

   * Cached in Redis (short-term)
   * Stored in PostgreSQL (long-term)
7. Response returned to client

---

## Asynchronous Design

* Uses `async/await` for non-blocking I/O
* `asyncio.Semaphore` to limit concurrent LLM calls
* `asyncio.wait_for` to enforce timeouts
* Optional parallel execution using `asyncio.gather`

---

## Caching Strategy

* Redis used to reduce latency and avoid repeated LLM calls
* Cache key format:

```
llm:<hash(question)>
```

* TTL (default): 60 seconds

---

## Retry Strategy

* Maximum 3 attempts
* Exponential backoff:

```
2^attempt seconds
```

---

## Timeout Handling

Each LLM call is wrapped with:

```
asyncio.wait_for(timeout=5)
```

Prevents long-running or stuck requests.

---

## Database Design

Table: `questions`

| Column     | Type      |
| ---------- | --------- |
| id         | Integer   |
| question   | Text      |
| answer     | Text      |
| created_at | Timestamp |

---

## Logging

* Structured logging across all layers
* Daily rotating log files
* Separate error logs
* Log levels:

  * INFO: normal flow
  * WARNING: retries or recoverable issues
  * ERROR: failures

---

## Security Considerations

* Environment variables managed via `.env`
* API keys not stored in source code
* Sensitive data not logged

---

## Scalability Considerations

* Stateless API enables horizontal scaling
* Redis reduces load on LLM API
* Database provides persistence and analytics capability
* Semaphore prevents overloading external services

---

## Trade-offs

| Feature | Trade-off                      |
| ------- | ------------------------------ |
| Caching | Possibility of stale data      |
| Retry   | Increased response latency     |
| Timeout | Risk of failing slow responses |

---

## Future Improvements

* Rate limiting using Redis
* Streaming responses from LLM
* Multi-model fallback strategy
* Metrics and monitoring (Prometheus, Grafana)
* Background processing (Celery or similar)

---

## Summary

This system demonstrates:

* Clean architectural separation
* Asynchronous programming patterns
* Effective caching strategy
* Fault tolerance mechanisms
* Observability through logging

It represents a production-style backend system for GenAI applications.

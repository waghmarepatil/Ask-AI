# System Architecture – Ask-AI

This document describes the architecture, components, and data flow of the Ask-AI backend system.

---

## Overview

Ask-AI is a FastAPI-based backend designed to integrate:

* Large Language Model (Groq)
* Redis for caching
* PostgreSQL for persistence
* Retrieval-Augmented Generation (RAG)
* Asynchronous processing
* Structured logging

The system is built with a focus on performance, scalability, and reliability.

---

## High-Level Architecture

Client
↓
FastAPI (API Layer)
↓
Service Layer (LLMService)
↓
├── Redis (Cache)
├── RAG Service (Retrieval Layer)
│     ├── PDF Processing
│     ├── Chunking
│     ├── Embeddings (SentenceTransformer)
│     └── FAISS (Vector Search)
├── Groq (LLM API)
└── PostgreSQL (Database)

---

## Layers Explained

### 1. API Layer (`api/`)

* Handles HTTP requests and responses
* Validates input/output using Pydantic schemas
* Supports both JSON and multipart/form-data (PDF upload)

Endpoint:
POST /chat

---

### 2. Service Layer (`services/`)

Responsible for:

* Cache lookup (Redis)
* Retry mechanism (3 attempts)
* Timeout handling
* Concurrency control (Semaphore)
* RAG orchestration
* LLM invocation

---

### 3. RAG Layer (`services/rag/`)

Implements Retrieval-Augmented Generation:

Steps:

1. Extract text from PDF
2. Split into chunks
3. Generate embeddings
4. Store in FAISS index
5. Retrieve top-k relevant chunks
6. Build context for LLM

---

### 4. Client Layer (`clients/`)

* Handles communication with Groq LLM
* Uses asyncio.to_thread for non-blocking execution

---

### 5. Repository Layer (`repositories/`)

#### Redis Repository

* Cache storage (no TTL)
* JSON serialization
* Context + response caching

#### Database Repository

* Stores question/answer pairs
* Async SQLAlchemy

---

## Request Flow

### Without PDF

1. Request → API
2. Cache lookup
3. LLM call
4. Store in Redis + DB
5. Return response

---

### With PDF (RAG)

1. Upload PDF
2. Extract text
3. Chunk + embed
4. Retrieve relevant chunks
5. Cache context
6. Pass context to LLM
7. Store response
8. Return answer

---

## Caching Strategy

Two-level caching:

1. Response cache
   key: llm:<hash(question)>

2. Context cache
   key: context:<hash(pdf)>

* No TTL (persists until Redis restart)
* Avoids recomputation of embeddings

---

## Retry Strategy

* 3 attempts
* Exponential backoff

---

## Timeout Handling

Each LLM call:

asyncio.wait_for(timeout=5)

---

## Logging

* Structured logs
* Rotating files
* Separate error logs

---

## Scalability Considerations

* Stateless API
* Redis reduces LLM load
* RAG reduces hallucination
* Semaphore prevents overload

---

## Trade-offs

* Rebuilding FAISS per request (can be optimized)
* Cache memory growth without TTL

---

## Future Improvements

* Persistent vector DB (FAISS / Pinecone)
* Multi-document RAG
* Streaming responses
* Rate limiting
* Metrics (Prometheus)

---

## Summary

This system demonstrates:

* Clean architecture
* Async programming
* RAG implementation
* Performance optimization
* Production-ready patterns

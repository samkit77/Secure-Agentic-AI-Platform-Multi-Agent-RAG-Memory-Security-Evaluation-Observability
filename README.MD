# Secure Agentic AI Platform — Multi-Agent RAG, Memory, Security, Evaluation & Observability

> **Security-focused, observable, evaluated Agentic RAG platform with multi-agent orchestration, hybrid retrieval, semantic memory, MCP tools, LLM gateway, caching, guardrails, and automated red teaming.**

### ⚡ Built With

**Multi-Agent Workflow** · **LangGraph** · **Hybrid Retrieval** · **Qdrant** · **BM25** · **MMR** · **Query Rewriting** · **Semantic Memory** · **MCP Web Search** · **Guardrails AI** · **Prompt-Injection Detection** · **PyRIT Red Teaming** · **Redis Caching** · **FastAPI Rate Limiting** · **Portkey LLM Gateway** · **LangSmith Observability** · **Token / Cost / Latency Tracking** · **Citations & Provenance** · **Multi-Format / Scalable Document Ingestion** · **DeepEval** · **Ragas**

---

## 🚀 What This Project Does

The system combines **adaptive retrieval, multi-agent orchestration, long-term semantic memory, external tools, layered security, caching, observability, and automated evaluation**.

### Core Capabilities

| Capability                    | Implementation                                                |
| ----------------------------- | ------------------------------------------------------------- |
| 🤖 **Multi-Agent RAG**        | LangGraph planner, retriever, evaluator, rewriter & responder |
| 🔍 **Hybrid Retrieval**       | Qdrant dense search + BM25                                    |
| 🎯 **Retrieval Optimization** | Ensemble fusion + MMR + LLM contextual filtering              |
| 🔄 **Query Recovery**         | Relevance checking + automatic query rewriting                |
| 🧠 **Semantic Memory**        | Qdrant long-term memory + LangGraph short-term state          |
| 🌐 **Web Search**             | MCP + DuckDuckGo fallback                                     |
| 🛡️ **AI Security**           | Guardrails + prompt-injection detection + output validation   |
| 🧨 **Red Teaming**            | Microsoft PyRIT + LLM-based security scoring                  |
| 📚 **Document Ingestion**     | PDF, DOCX, HTML, CSV, TXT, Markdown                           |
| 📌 **Citations**              | Source/chunk metadata + structured provenance                 |
| ⚡ **Caching**                 | Redis response caching with TTL                               |
| 🚦 **Rate Limiting**          | 20 requests / 60s / client IP                                 |
| 🔌 **LLM Gateway**            | Portkey routing, retries & fallback                           |
| 📊 **Observability**          | LangSmith traces, tokens, cost & latency                      |
| 🧪 **Evaluation**             | DeepEval + Ragas + PyRIT                                      |
| 🎨 **Frontend**               | Streamlit                                                     |

---

## 🧠 Agentic Workflow

This project extends that architecture into an agentic workflow:

                        User
                         ↓
                 Input Guardrails
                         ↓
             Prompt Injection Detection
                         ↓
                  Redis Cache
                  ↙         ↘
              HIT             MISS
               ↓                ↓
            Answer        LangGraph Agent
                              ↓
                           Planner
                              ↓
                       Hybrid Retrieval
                       ↙              ↘
                  Qdrant              BM25
                    ↓                   ↓
                    └────── Fusion ────┘
                              ↓
                             MMR
                              ↓
                       LLM Chain Filter
                              ↓
                      Relevance Checker
                         ↓           ↓
                      Relevant     Not Relevant
                         ↓             ↓
                     Responder   Query Rewriter
                                     ↓
                                  Retrieval
                                     ↓
                                Retry Limit
                                     ↓
                                MCP Web Search
                                     ↓
                                  Responder
                                     
                                ↓
                        Output Guardrails
                                ↓
                         Answer+Citations
                                ↓
                        Semantic Memory Store

The system also has a separate red-team evaluation layer:

    PyRIT
    ↓
    Prompt Injection / Jailbreak / XPIA
    ↓
    FastAPI /query
    ↓
    Complete Agentic RAG
    ↓
    PyRIT LLM Scorer
    ↓
    Security Evaluation
---

## 🔍 Retrieval

The retrieval stack combines multiple techniques to improve both semantic and exact-term matching.

```text
Qdrant Dense Search
        +
BM25 Keyword Search
        ↓
Weighted Ensemble
        ↓
MMR
        ↓
LLM Context Filter
        ↓
Relevance Checker
```

---

## 🧠 Semantic Memory

Long-term semantic memory is stored separately from conversation state.

```text
Conversation
     ↓
Memory Extraction
     ↓
Durable Information
     ↓
Embedding
     ↓
Qdrant semantic_memory
```

Features:

* LLM-based memory extraction
* Preferences, goals, projects and interests
* Semantic deduplication
* User-scoped memory filtering
* LangGraph `MemorySaver` for short-term state

---

## 🛡️ Security

Security is implemented as a layered defense rather than relying on a single prompt or model.

```text
Input
 ↓
Guardrails
 ↓
Prompt-Injection Detection
 ↓
Agentic Workflow
 ↓
Output Guardrails
 ↓
Response
```

Includes:

* Prompt-injection detection
* Input validation
* Output validation
* Tool isolation through MCP
* API rate limiting
* Automated adversarial evaluation

Blocked prompt-injection requests do not enter the main RAG workflow.

---

## 🧨 Red Teaming

Microsoft **PyRIT** evaluates the production API independently from the normal inference path.

Current attack suite:

| Attack Category  |
| ---------------- |
| Prompt Injection |
| Jailbreak        |
| XPIA             |
| **Total**        | 

The red-team pipeline measures:

* Blocked attacks
* Successful attacks
* Scoring failures
* Attack Success Rate (ASR)

```text
PyRIT
  ↓
Adversarial Prompt
  ↓
FastAPI /query
  ↓
Full RAG + Security Pipeline
  ↓
LLM Scorer
  ↓
Security Metrics
```

---

## ⚡ Caching & API Protection

### Redis

Application-level response caching:

```text
Request
 ↓
Normalized Query
 ↓
Redis
 ├── HIT  → Cached Response
 └── MISS → Agentic RAG → Redis SET
```

```text
TTL: 3600 seconds
```

Redis is an optimization layer and is independent of the LLM gateway.

### Rate Limiting

FastAPI `/query`:

```text
20 requests / 60 seconds / client IP
```

Exceeded limits return `HTTP 429`.

---

## 🔌 LLM Gateway & Observability

### Portkey

Portkey acts as the **LLM gateway** for:

* Provider routing
* Gateway configuration
* Retry/fallback behavior
* Centralized LLM access

```text
Portkey → LLM Gateway
Redis   → Application Cache
```

### LangSmith

LangSmith provides end-to-end observability for:

* LangGraph execution
* Agent/node traces
* LLM calls
* Retrieval
* Latency
* Token usage
* Model usage
* Cost

This allows the system to measure both **AI quality and infrastructure/LLM efficiency**.

---

## 📚 Document Ingestion & Citations

Supported formats:

```text
PDF
DOCX
HTML
CSV
TXT
Markdown
```

The ingestion pipeline normalizes, chunks, embeds and indexes documents into Qdrant.

Document metadata includes:

```text
source
source_type
chunk_index
text
```

This metadata is preserved through retrieval and used for **source attribution and citations** in API responses.

The ingestion architecture is modular and designed to support larger document collections and future scalable ingestion workflows.

---

## 🧪 Evaluation

The project evaluates **quality and security separately**.

### DeepEval

* Contextual Precision
* Contextual Recall
* Contextual Relevancy
* Answer Relevancy
* Faithfulness

### Ragas

* Context Precision
* Response Relevancy

### PyRIT

* Prompt Injection
* Jailbreak
* XPIA

```text
RAG Quality
 ├── DeepEval
 └── Ragas

Security
 └── PyRIT
```

---

## 🧰 Technology Stack

| Layer           | Technology                                 |
| --------------- | ------------------------------------------ |
| API             | FastAPI                                    |
| Agent Framework | LangGraph                                  |
| LLM             | OpenAI                                     |
| LLM Gateway     | Portkey                                    |
| Embeddings      | `text-embedding-3-small`                   |
| Vector DB       | Qdrant                                     |
| Retrieval       | Dense + BM25                               |
| Optimization    | Ensemble + MMR + LLM Filtering             |
| Query Recovery  | Query Rewriter                             |
| Web Tools       | MCP + DuckDuckGo                           |
| Memory          | Qdrant + MemorySaver                       |
| Security        | Guardrails AI + Prompt-Injection Detection |
| Cache           | Redis                                      |
| Rate Limiting   | FastAPI                                    |
| Observability   | LangSmith                                  |
| Evaluation      | DeepEval + Ragas                           |
| Red Teaming     | Microsoft PyRIT                            |
| Frontend        | Streamlit                                  |

---

## 📁 Project Structure

```text
enterprise-agentic-rag/
│
├── app/
│   ├── agents/
│   │   ├── graph.py
│   │   ├── state.py
│   │   └── nodes/
│   ├── ingestion/
│   │   └── loaders/
│   ├── services/
│   │   ├── retrieval/
│   │   ├── memory/
│   │   └── cache/
│   ├── security/
│   ├── guardrails/
│   ├── mcp/
│   └── main.py
│
├── evaluation/
├── red_team/
├── docker-compose.yml
└── .env
```

---



## 📌 Current Scope

### Implemented

**Agentic**

* Multi-agent LangGraph workflow
* Planner
* Hybrid retrieval
* Relevance checking
* Query rewriting
* MCP fallback
* Semantic memory

**Security**

* Guardrails
* Prompt-injection detection
* Output validation
* Rate limiting
* PyRIT red teaming

**Infrastructure**

* Redis caching
* Portkey LLM gateway
* LangSmith observability
* Token/cost/latency tracking
* Qdrant vector storage
* Multi-format document ingestion

**Evaluation**

* DeepEval
* Ragas
* PyRIT
* Source citations/provenance


---


**The goal is not simply to generate answers — it is to build a RAG system that can retrieve intelligently, recover from failure, use tools safely, remember useful context, expose provenance, measure its own performance, and withstand adversarial testing.**

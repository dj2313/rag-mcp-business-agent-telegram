# 🤖 RAG + MCP Business Agent — Product Requirements Document

## 📋 Document Info

| Field        | Value                                      |
|--------------|--------------------------------------------|
| Project      | RAG + MCP Business Agent                   |
| Version      | 1.0                                        |
| Date         | March 2026                                 |
| IDE          | Google Antigravity                         |
| Language     | Python 3.11+                               |
| Status       | ✅ Ready for Development                   |
| Priority     | 🔴 High — Build This Week                  |

---

## 📌 Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Goals & Success Criteria](#3-goals--success-criteria)
4. [Tech Stack](#4-tech-stack)
5. [System Architecture](#5-system-architecture)
6. [How It Works — Step by Step](#6-how-it-works--step-by-step)
7. [Functional Requirements](#7-functional-requirements)
8. [Non-Functional Requirements](#8-non-functional-requirements)
9. [Folder Structure](#9-folder-structure)
10. [Development Roadmap](#10-development-roadmap)
11. [Environment Setup](#11-environment-setup)
12. [Launch & Testing Guide](#12-launch--testing-guide)
13. [Deployment Guide](#13-deployment-guide)
14. [Risks & Mitigations](#14-risks--mitigations)
15. [Out of Scope (v1)](#15-out-of-scope-v1)
16. [Glossary](#16-glossary)

---

## 1. Executive Summary

This project is a **fully autonomous AI business agent** built in Python. It combines three powerful AI techniques into one deployable application:

- **RAG (Retrieval-Augmented Generation)** — The agent searches your private company documents and uses that knowledge to answer questions accurately.
- **MCP (Model Context Protocol)** — The agent connects to your database, APIs, and services via structured tools. It can query records, send emails, and create tickets automatically.
- **LLM (Groq + Llama 3)** — The brain that reads all retrieved context, decides which tools to use, and generates the final smart response.

The user interface is **Telegram**. A user sends a message, the agent thinks, uses tools if needed, and replies — all automatically with zero human involvement after deployment. The entire stack runs on **free APIs and open-source tools**.

---

## 2. Problem Statement

Most AI apps today are just chatbots. They respond to messages but cannot take real actions, access live data, or work without a human monitoring them. This project solves three specific problems:

1. **Chatbots are passive** — they answer but cannot send emails, query databases, or create tickets on their own.
2. **RAG is disconnected** — most RAG systems answer from static documents but cannot combine that with live business data.
3. **Agents are expensive** — most agentic AI tutorials require paid OpenAI APIs, making them inaccessible for indie developers.

This agent is **active**, **connected**, and **free to run**.

---

## 3. Goals & Success Criteria

### Primary Goals

- ✅ Build an agent that runs automatically with zero manual operation after launch
- ✅ Use only free APIs and open-source tools (no OpenAI, no paid subscriptions)
- ✅ Demonstrate working RAG + MCP + LLM integration in a production-style app
- ✅ Communicate with users via Telegram (send, receive, and reply to messages)

### Success Criteria

| Criteria | Target |
|----------|--------|
| Response time | Under 8 seconds for standard queries |
| RAG accuracy | Correctly retrieves from documents for knowledge questions |
| MCP tool use | Correctly queries DB or sends email when triggered |
| Autonomous actions | Sends email/ticket without human involvement |
| Cost | Zero paid API usage in baseline build |
| Uptime | Runs continuously after deployment |

---

## 4. Tech Stack

> All tools below are **free-tier compatible** and work in **Google Antigravity IDE**.

| Layer              | Technology                  | Why                                                      |
|--------------------|-----------------------------|----------------------------------------------------------|
| **LLM Brain**      | Groq API (Llama 3.3)        | Free tier, 30k tokens/min, fastest open inference        |
| **Local LLM**      | Ollama (optional)           | Run Llama locally for 100% free with no rate limits      |
| **Embeddings**     | `sentence-transformers`     | Free local embeddings, no API cost                       |
| **Vector DB**      | ChromaDB                    | Free, runs locally, stores document vectors for RAG      |
| **MCP Server**     | `mcp` Python SDK            | Official Anthropic SDK for tool-use protocol             |
| **Agent Framework**| LangGraph                   | Builds multi-step agentic loops with tool calling        |
| **Telegram Bot**   | `python-telegram-bot`       | Free, handles send/receive/chat with users               |
| **Database**       | SQLite (dev) / Supabase     | SQLite = zero setup; Supabase = free hosted PostgreSQL   |
| **Email**          | Gmail SMTP / Resend API     | Gmail SMTP free; Resend gives 3000 emails/month free     |
| **Language**       | Python 3.11+                | Best AI/ML ecosystem, all libraries are Python-first     |
| **IDE**            | Google Antigravity          | AI-powered IDE for building this project                 |

### Why Groq and not OpenAI?

Groq's free tier offers **30,000 tokens per minute** on Llama 3.3, which handles all agentic loops easily. OpenAI charges per token. For a prototype or small-scale deployment, Groq is the correct and cost-free choice. If you want to upgrade later, swapping Groq for OpenAI is a single line change in LangChain.

---

## 5. System Architecture

### High-Level Flow

```
User (Telegram)
      │
      ▼
┌─────────────────────────────────────────────────┐
│              Telegram Bot Layer                  │
│         (receives & sends messages)              │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│            LangGraph Agent Loop                  │
│   (decides: answer directly OR use tools)        │
└──────────┬─────────────────────┬────────────────┘
           │                     │
           ▼                     ▼
┌──────────────────┐   ┌──────────────────────────┐
│   RAG System     │   │      MCP Server           │
│  (ChromaDB)      │   │  (DB, Email, Tickets)     │
│  searches your   │   │  fetches live data and    │
│  documents       │   │  performs real actions    │
└──────────┬───────┘   └────────────┬─────────────┘
           │                        │
           └────────────┬───────────┘
                        │
                        ▼
          ┌─────────────────────────┐
          │     Groq LLM            │
          │  (Llama 3.3 — Brain)    │
          │  combines all context   │
          │  generates final answer │
          └────────────┬────────────┘
                       │
                       ▼
              Reply sent to Telegram
```

### Component Responsibilities

| Component | Job |
|-----------|-----|
| Telegram Layer | Receives user messages, sends back responses |
| LangGraph Agent | Routes queries to RAG, MCP tools, or direct answer |
| RAG System | Converts documents to vectors, retrieves relevant chunks |
| MCP Server | Exposes database queries, email, ticket creation as tools |
| Groq LLM | Reads all context, decides tool use, generates responses |

---

## 6. How It Works — Step by Step

This is exactly what happens when a user sends a Telegram message:

```
Step 1 — User sends message on Telegram
         "What is our refund policy and can you email it to john@company.com?"

Step 2 — Telegram bot receives the message
         Passes it to the LangGraph agent

Step 3 — LangGraph agent analyzes intent
         Detects: needs document info (RAG) + needs to send email (MCP)

Step 4 — RAG searches ChromaDB
         Finds the most relevant chunks from your refund policy document
         Returns top 3 matching text chunks

Step 5 — LLM reads the RAG chunks
         Summarizes the refund policy clearly

Step 6 — MCP email tool is triggered
         Agent calls send_email(to="john@company.com", body=summary)
         Email is sent automatically

Step 7 — LLM generates final Telegram reply
         "I found your refund policy and sent a summary to john@company.com ✅"

Step 8 — Telegram bot sends the reply
         User receives the response in under 8 seconds
```

---

## 7. Functional Requirements

### 7.1 Telegram Interface

| ID | Requirement |
|----|-------------|
| FR-01 | Agent MUST receive text messages from any Telegram user |
| FR-02 | Agent MUST respond in the same chat within 8 seconds |
| FR-03 | Agent MUST support PDF and TXT file uploads for document ingestion |
| FR-04 | Agent MUST support commands: `/start`, `/help`, `/ingest`, `/status` |
| FR-05 | Agent MUST handle errors gracefully and inform the user if something fails |

### 7.2 RAG System

| ID | Requirement |
|----|-------------|
| FR-06 | System MUST ingest PDF and TXT documents into ChromaDB |
| FR-07 | RAG MUST retrieve top-3 most relevant chunks per query |
| FR-08 | Embeddings MUST be generated via `sentence-transformers` locally |
| FR-09 | Documents MUST persist between agent restarts (ChromaDB persistent mode) |
| FR-10 | User MUST be able to add new documents via Telegram `/ingest` command |

### 7.3 MCP Server Tools

| ID | Requirement |
|----|-------------|
| FR-11 | MCP MUST expose at minimum 4 tools: `search_database`, `get_record`, `send_email`, `create_ticket` |
| FR-12 | All MCP tools MUST return structured JSON |
| FR-13 | Tool errors MUST be caught and return a human-readable error message |
| FR-14 | MCP server MUST run as an async subprocess alongside the Telegram bot |

### 7.4 LLM Reasoning

| ID | Requirement |
|----|-------------|
| FR-15 | LLM MUST include retrieved RAG context when answering knowledge questions |
| FR-16 | LLM MUST autonomously decide whether to call a tool or answer directly |
| FR-17 | Agent MUST support multi-step tool chains (e.g. search DB → send email) |
| FR-18 | LLM MUST use Groq API with Llama 3.3 model as default |

### 7.5 Autonomous Actions

| ID | Requirement |
|----|-------------|
| FR-19 | When user mentions "send email" or "notify", agent MUST send email via MCP |
| FR-20 | When user mentions "create ticket" or "report issue", agent MUST create ticket via MCP |
| FR-21 | All autonomous actions MUST send a confirmation message back to the user |
| FR-22 | Agent MUST log all actions taken to a local log file |

---

## 8. Non-Functional Requirements

| ID | Category | Requirement |
|----|----------|-------------|
| NFR-01 | Performance | Response time under 8 seconds for standard queries |
| NFR-02 | Cost | Zero paid API usage in baseline build |
| NFR-03 | Availability | Runs continuously after deployment without manual restarts |
| NFR-04 | Scalability | New MCP tools can be added without rewriting core agent logic |
| NFR-05 | Security | All API keys stored in `.env` file, never hardcoded |
| NFR-06 | Portability | Runs in Google Antigravity and on Railway/Fly.io deployment |
| NFR-07 | Maintainability | Each layer (RAG, MCP, Agent, Telegram) is independently testable |

---

## 9. Folder Structure

```
business-agent/
│
├── agent/
│   ├── graph.py            # LangGraph agent — the main reasoning loop
│   ├── tools.py            # Tool definitions that LangGraph can call
│   └── prompts.py          # System prompts for the LLM
│
├── mcp_server/
│   ├── server.py           # MCP server entry point
│   ├── db_tools.py         # search_database and get_record tools
│   └── action_tools.py     # send_email and create_ticket tools
│
├── rag/
│   ├── ingest.py           # Document ingestion pipeline
│   ├── retriever.py        # ChromaDB query and retrieval
│   └── documents/          # Put your company PDFs and TXTs here
│
├── telegram/
│   └── bot.py              # Telegram bot — handles incoming messages
│
├── tests/
│   ├── test_rag.py         # Unit tests for RAG retrieval
│   ├── test_mcp.py         # Unit tests for MCP tools
│   └── test_agent.py       # Integration test for full agent loop
│
├── .env                    # All secrets — NEVER commit this to git
├── .gitignore              # Must include .env and chroma_db/
├── requirements.txt        # All Python packages
├── Procfile                # For Railway deployment: web: python main.py
└── main.py                 # Entry point — starts bot + MCP server
```

---

## 10. Development Roadmap

> Target: **Working agent in 6 days** as a solo developer.

| Phase | Day | What to Build | Done When |
|-------|-----|---------------|-----------|
| **Phase 1** | Day 1 | Telegram bot + Groq LLM connected | Bot replies intelligently to messages |
| **Phase 2** | Day 2 | RAG pipeline: ingest docs → ChromaDB → retrieval | Agent answers from your documents |
| **Phase 3** | Day 3 | MCP server with `send_email` + `search_database` tools | Agent can query DB and send email |
| **Phase 4** | Day 4 | LangGraph connects LLM + RAG + MCP tools | Full agent loop working end-to-end |
| **Phase 5** | Day 5 | Error handling, logging, `.env` config, unit tests | Production-ready and tested |
| **Phase 6** | Day 6-7 | Deploy to Railway.app (free tier) | Always-on, live deployment |

---

## 11. Environment Setup

### Step 1 — Create Free Accounts

- **Groq**: [console.groq.com](https://console.groq.com) → Sign up → Copy API key
- **Telegram**: Open Telegram → Search `@BotFather` → `/newbot` → Copy bot token
- **Gmail**: Google Account → Security → App Passwords → Create one for "Mail"
- **Supabase** *(optional)*: [supabase.com](https://supabase.com) → Free PostgreSQL database

### Step 2 — Install Python Packages

```bash
pip install langchain langchain-groq langgraph
pip install chromadb sentence-transformers
pip install mcp python-telegram-bot
pip install python-dotenv aiohttp fastapi uvicorn
pip install pytest pytest-asyncio
```

Or save as `requirements.txt`:

```text
langchain==0.3.0
langchain-groq==0.2.0
langgraph==0.2.0
chromadb==0.5.0
sentence-transformers==3.0.0
mcp==1.0.0
python-telegram-bot==21.0
python-dotenv==1.0.0
aiohttp==3.9.0
fastapi==0.115.0
uvicorn==0.30.0
pytest==8.0.0
pytest-asyncio==0.23.0
```

### Step 3 — Create .env File

```env
# LLM
GROQ_API_KEY=your_groq_api_key_here

# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Email
GMAIL_SENDER=youremail@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password_here

# Database (leave as sqlite for local dev)
DATABASE_URL=sqlite:///./business_agent.db

# Optional: Supabase for production
# DATABASE_URL=postgresql://user:pass@db.supabase.co:5432/postgres
```

### Step 4 — Create .gitignore

```gitignore
.env
chroma_db/
__pycache__/
*.pyc
.pytest_cache/
*.db
```

---

## 12. Launch & Testing Guide

### Running Locally in Google Antigravity

```bash
# Start the agent (runs Telegram bot + MCP server together)
python main.py
```

Open Telegram, find your bot by its username, and send it a message. You will see the response within seconds.

### Testing Each Layer Individually

**Test RAG without Telegram:**
```bash
python -m pytest tests/test_rag.py -v
```

**Test MCP tools directly:**
```bash
python -m pytest tests/test_mcp.py -v
```

**Test the full agent loop without Telegram:**
```bash
python tests/test_agent.py
# This runs the agent in terminal — no Telegram needed
```

**Test in Telegram:**
Just message your bot. Use these test messages to verify everything:

| Message to send | What it tests |
|-----------------|---------------|
| `"What is our refund policy?"` | RAG retrieval |
| `"Get me the record for customer ID 123"` | MCP database tool |
| `"Send an email to test@gmail.com saying hello"` | MCP email tool |
| `"What is 2+2"` | Direct LLM answer (no tools) |
| `/status` | Bot command handling |

---

## 13. Deployment Guide

### Option A — Railway.app (Recommended)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project in your folder
railway init

# 4. Deploy
railway up
```

Then go to Railway dashboard → add all your `.env` variables there.
Your agent will be live at a public URL, running 24/7.

### Option B — Fly.io

```bash
# 1. Install flyctl
curl -L https://fly.io/install.sh | sh

# 2. Launch
fly launch

# 3. Set secrets
fly secrets set GROQ_API_KEY=your_key TELEGRAM_BOT_TOKEN=your_token

# 4. Deploy
fly deploy
```

### Procfile (Required for Railway)

Create a file called `Procfile` with no extension:
```
web: python main.py
```

### Switch to Webhook Mode for Production

In `telegram/bot.py`, change from polling to webhook for production:

```python
# DEVELOPMENT — polling (use this locally)
app.run_polling()

# PRODUCTION — webhook (use this on Railway/Fly)
app.run_webhook(
    listen="0.0.0.0",
    port=8080,
    webhook_url=f"https://your-railway-url.up.railway.app/{TOKEN}"
)
```

---

## 14. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Groq rate limit hit | Agent stops responding | Add retry logic with 3-second backoff |
| ChromaDB corrupts on crash | RAG stops working | Back up chroma_db/ folder daily |
| Telegram webhook stops | Users get no replies | Set up Railway health check endpoint |
| MCP tool throws exception | Agent crashes mid-loop | Wrap all MCP tools in try/except |
| `.env` file committed to git | Secrets exposed | Add `.env` to `.gitignore` immediately |

---

## 15. Out of Scope (v1)

These features will NOT be built in version 1 to keep scope focused:

- ❌ Multi-user authentication or per-user memory
- ❌ Voice message processing
- ❌ Image understanding / vision
- ❌ WhatsApp or Discord interface (Telegram only)
- ❌ Web UI frontend (Telegram is the only interface)
- ❌ Agent-to-agent communication (single agent only)
- ❌ Streaming responses (full response sent at once)

---

## 16. Glossary

| Term | Plain English Explanation |
|------|--------------------------|
| **RAG** | Retrieval-Augmented Generation. The agent searches your documents, finds the most relevant text, and adds it to the LLM's prompt as extra context before answering. |
| **MCP** | Model Context Protocol. An open standard by Anthropic that lets an LLM call external tools (databases, APIs, email) in a structured, reliable way. |
| **LangGraph** | A Python library for building AI agents as graphs. Each node in the graph is a step: receive input → retrieve → call tool → generate response. |
| **ChromaDB** | An open-source vector database. Stores your documents as mathematical vectors so the agent can find "similar" text to any query. |
| **Groq** | A free LLM API that runs Llama 3.3 at very high speed. Free tier at console.groq.com. |
| **Embedding** | A list of numbers that represents the meaning of a piece of text. Similar texts have similar number patterns, which is how RAG search works. |
| **Tool Use** | When an LLM decides to call an external function (like `send_email`) instead of answering from its own knowledge. |
| **Agent Loop** | The repeating cycle: receive input → reason → act → observe result → repeat until the task is complete. |
| **Webhook** | A URL that Telegram calls every time a user sends a message. Better than polling for production deployments. |
| **Polling** | The bot checks Telegram every few seconds asking "any new messages?" — good for development, not ideal for production. |

---

*End of Document — RAG + MCP Business Agent PRD v1.0 — March 2026*

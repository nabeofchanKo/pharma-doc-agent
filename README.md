# 💊 Pharma Doc Agent

A RAG (Retrieval-Augmented Generation) powered AI assistant designed to answer questions from pharmaceutical PDF documents with strict referencing constraints.

## 🏗 Architecture (Tier 1 Standard)

- **Frontend:** Streamlit (UI/UX)
- **Backend:** FastAPI (Async Streaming API)
- **Database:** PostgreSQL (Chat History Persistence)
- **Vector DB:** ChromaDB (In-memory vector storage)
- **LLM:** OpenAI GPT-3.5/4
- **Containerization:** Docker & Docker Compose

## 🚀 Features

- **Real-time Streaming:** Token-by-token response generation.
- **RAG Implementation:** Local embeddings with vector search.
- **Strict Hallucination Control:** Context-aware prompting.

## 🛠️ How to Run

1. Clone and Setup .env
   ```bash
   OPENAI_API_KEY=sk-...
   POSTGRES_USER=pharma_user
   POSTGRES_PASSWORD=pharma_password
   POSTGRES_DB=pharma_chat_db
   ```
2. Clone and Setup .env
   ```bash
   docker-compose up --build
   ```
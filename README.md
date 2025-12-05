# PharmaDoc Agent 💊🤖

## 📌 Overview
**PharmaDoc Agent** is an AI-powered document processing pipeline designed to streamline **Pharmacovigilance (PV)** and **Logistics Operations**.
By leveraging LLMs (Large Language Models) and RAG (Retrieval-Augmented Generation), it automatically extracts critical information from unstructured documents like Adverse Event Reports (CIOMS) or Shipping Invoices.

**PharmaDoc Agent** は、製薬（PV）および物流業務を効率化するために設計された、AIドキュメント処理パイプラインです。
LLMとRAG技術を活用し、副作用報告書（CIOMS）や通関書類（Invoice）などの「非構造化データ」から、重要項目を自動抽出・構造化します。

## 🚀 Key Features (Planned)
- **Universal Ingestion**: Supports PDF, Excel, and Email text via Drag & Drop.
- **Intelligent Extraction**: Extracts specific entities (e.g., Patient ID, Drug Name, Side Effects, Lot No.) using LLMs.
- **Business Logic Validation**:
    - **Pharma**: Detects "Serious" adverse events and flags priority.
    - **Logistics**: Cross-checks Invoice amounts against PO data.
- **Microservices Architecture**: Built with FastAPI (Backend) and Streamlit (Frontend).

## 🛠️ Tech Stack
- **Language**: Python 3.10+
- **LLM / AI**: LangChain, OpenAI API (GPT-4o)
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Database**: ChromaDB (Vector Store)
- **Infrastructure**: Docker, Docker Compose, AWS (App Runner)

## 🏗️ Architecture
(Coming Soon: Diagram showing Flow from PDF -> OCR -> LLM -> JSON)

## 👤 Author
**Applied AI Engineer**
Focusing on Pharma & Supply Chain DX.
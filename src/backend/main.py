import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from src.backend.schemas import HealthResponse, UploadResponse, ChatRequest, ChatResponse
from src.backend.services.pdf_loader import PDFLoader
from src.backend.services.rag_service import RAGService
from src.backend.db import models
from src.backend.db.database import engine

app = FastAPI(title="PharmaDoc Agent API")

# 🔥 Create Database Tables (Add this line!)
# This will create tables defined in models.py if they don't exist
models.Base.metadata.create_all(bind=engine)

# Initialize RAG Service (Global instance)
# Note: In production, use dependency injection (Depends)
rag_service = RAGService()

UPLOAD_DIR = "/app/data/input"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Specify response_model to enable return value type validation
@app.get("/health", response_model=HealthResponse)
def read_health():
    # Even if a dictionary is returned, Pydantic automatically converts it into the specified model
    return {
        "status": "healthy",
        "version": "0.1.0"
    }

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    # 1. Read file content
    content = await file.read()

    # 2. Save original file locally (Audit trail)
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(content)

    # 3. Extract Text (Using our new PDFLoader)
    text = PDFLoader.extract_text_from_stream(content)

    # 4. Process for RAG (Chunking & Embedding)
    # This might take a few seconds, so async is good here
    num_chunks = rag_service.process_document(text, file.filename)

    return {
        "filename": file.filename,
        "saved_path": file_location,
        "size": len(content),
        "message": f"File processed successfully! Stored {num_chunks} vector chunks."
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):

    return rag_service.generate_answer(request.message)

@app.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    return StreamingResponse(
        rag_service.a_generate_answer_stream(request.message),
        media_type="text/event-stream"
    )
from pydantic import BaseModel
from typing import Optional

class HealthResponse(BaseModel):
    status: str
    version: str

class UploadResponse(BaseModel):
    filename: str
    saved_path: str
    size: int
    message: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    context: list[str]
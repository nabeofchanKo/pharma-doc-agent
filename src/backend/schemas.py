from pydantic import BaseModel
from typing import Optional

# APIのレスポンス定義（返り血の厳格化）
class HealthResponse(BaseModel):
    status: str
    version: str

class UploadResponse(BaseModel):
    filename: str
    saved_path: str
    size: int
    message: str
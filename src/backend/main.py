import os
import shutil
from fastapi import FastAPI, UploadFile, File
# Dockerのルート(/app)から見た完全なパスを指定する
from src.backend.schemas import HealthResponse, UploadResponse

app = FastAPI(title="PharmaDoc Agent API")

UPLOAD_DIR = "/app/data/input"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# response_model を指定することで、返り値の型チェックを行う
@app.get("/health", response_model=HealthResponse)
def read_health():
    # 辞書を返しても、Pydanticが自動でクラスに変換してくれる
    return {
        "status": "healthy",
        "version": "0.1.0"
    }

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    
    # ファイルサイズを取得するためにポインタを末尾へ
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)  # ポインタを先頭に戻す

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {
        "filename": file.filename,
        "saved_path": file_location,
        "size": file_size,
        "message": "File uploaded successfully"
    }
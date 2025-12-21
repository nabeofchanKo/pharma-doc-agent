import os
import shutil
from fastapi import FastAPI, UploadFile, File

app = FastAPI(title="PharmaDoc Agent API")

# Save To
# 保存先ディレクトリ（コンテナ内のパス）
UPLOAD_DIR = "/app/data/input"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/health")
def read_health():
    return {"message": "Ready to analyze CIOMS reports"}

# endpoint for uploading files
# ファイルアップロード用エンドポイント（POSTメソッド）
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Recieve and save a file from Frontend
    Frontendから送られてきたfileを受け取り、保存する
    """

    file_location = f"{UPLOAD_DIR}/{file.filename}"
    
    # Save a file with shutil
    # ファイルを保存する処理（shutilを使ってコピー）
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"filename": file.filename, "status": "saved", "location": file_location}
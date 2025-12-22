import requests
import os
from typing import Optional, Dict, Any

class APIClient:
    def __init__(self, base_url: str = "http://backend:8000"):
        self.base_url = base_url
    
    def check_health(self) -> Dict[str, Any]:
        """Backendのヘルスチェックを行う"""
        try:
            response =  requests.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return response.jsou()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "details": str(e)}
        
    def upload_file(self, file_obj, filename: str) -> Optional[Dict[str, Any]]:
        """ファイルをアップロードする"""
        try:
            files = {"file": (filename, file_obj, "application/pdf")}
            response = requests.post(f"{self.base_url}/upload", files=files, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Upload failed: {e}")
            return None
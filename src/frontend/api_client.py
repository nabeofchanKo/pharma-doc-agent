import requests
import os
from typing import Optional, Dict, Any

class APIClient:
    def __init__(self, base_url: str = "http://backend:8000"):
        self.base_url = base_url
    
    def check_health(self) -> Dict[str, Any]:
        """Perform a health check on the backend"""
        try:
            response =  requests.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "details": str(e)}
        
    def upload_file(self, file_obj, filename: str) -> Optional[Dict[str, Any]]:
        """Upload a file"""
        try:
            files = {"file": (filename, file_obj, "application/pdf")}
            response = requests.post(f"{self.base_url}/upload", files=files, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Upload failed: {e}")
            return None
        
    def chat(self, message: str)  -> Optional[Dict[str, Any]]:
        try:
            response = requests.post(
                f"{self.base_url}/chat", 
                json={"message":message},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Chat failed: {e}")
            return None
        
    def chat_stream(self, message: str):
            """
            Stream the chat response from the backend.
            Yields: str (partial response chunks)
            """
            try:
                with requests.post(
                    f"{self.base_url}/chat/stream", 
                    json={"message": message}, 
                    stream=True,
                    timeout=30
                ) as response:
                    response.raise_for_status()
                    
                    for chunk in response.iter_content(chunk_size=None):
                        if chunk:
                            yield chunk.decode('utf-8')
                            
            except requests.exceptions.RequestException as e:
                print(f"Chat stream failed: {e}")
                yield f"Error: {str(e)}"
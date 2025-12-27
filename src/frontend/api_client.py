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
                # stream=True is critical! Without this, the client waits for the full response.
                with requests.post(
                    f"{self.base_url}/chat/stream", 
                    json={"message": message}, 
                    stream=True,
                    timeout=30
                ) as response:
                    response.raise_for_status()
                    
                    # Loop to process each chunk as it arrives
                    for chunk in response.iter_content(chunk_size=None):
                        if chunk:
                            # Decode bytes to string and yield
                            yield chunk.decode('utf-8')
                            
            except requests.exceptions.RequestException as e:
                print(f"Chat stream failed: {e}")
                yield f"Error: {str(e)}"

    def get_history(self):
        """
        Fetch chat history from the backend.
        Returns: List of dicts (role, content)
        """
        try:
            # We currently use "default_session" hardcoded
            response = requests.get(f"{self.base_url}/chat/history?session_id=default_session")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Failed to fetch history: {e}")
            return []
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List
import os

class RAGService:
    """
    Core service for RAG (Retrieval-Augmented Generation) operations.
    Manages embedding generation and vector database interactions.
    """

    def __init__(self):
        # Initialize Embedding Model (Runs locally!)
        # We cache models in ./models to avoid re-downloading
        model_name = "intfloat/multilingual-e5-small"
        model_kwargs = {"device": "cpu"} # Use "cuda" if GPU is available
        encode_kwargs = {"normalize_embeddings": True}

        print(f"Loading Embedding Model: {model_name}...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
            cache_folder="/root/.cache/huggingface" # Matches docker volume
        )

        # Initialize Vector DB (Chroma)
        # Persist data to /app/data/vector_db"
        self.persist_directory = "/app/data/vector_db"
        self.vector_db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def process_document(self, text: str, filename: str) -> int:
        """
        Splits text into chunks, creates embeddings, and saves to Vector DB.
        
        Returns:
            int: Number of chunks created.
        """

        # 1. Split Text (Chunking)
        # Chunk size 500 is a good balance for Japanese/English mixed content
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "、", " ", ""]
        )
        chunks = text_splitter.split_text(text)

        # 2. Add Metadata (Important for citation!)
        metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]

        # 3. Save to ChromaDB
        if chunks:
            self.vector_db.add_texts(texts=chunks, metadatas=metadatas)
            self.vector_db.persist() # Force save to disk
        
        return len(chunks)
    
    def search(self, query: str, k: int = 3) -> List[str]:
        """
        Semantic search for relevant document chunks.
        """
        docs = self.vector_db.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
    
    def generate_answer(self, query: str) -> dict:
        """
        Retrieve context and generate answer.
        Returns a dict with 'response' and 'context'.
        """

        # 1. Search for context
        context_docs = self.search(query)

        # 2. Construct Prompt
        context_text = "\n".join(context_docs)

        # 3. Generate (Dummy for today)
        dummy_response = "Dummy Response: " + context_text 

        return {
            "response": "This is a dummy response based on context...",
            "context": [dummy_response]
        }
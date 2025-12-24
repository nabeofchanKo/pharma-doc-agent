from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
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

        # Initialize LLM (GPT)
        self.llm =ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0
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
        Retrieve context and generate answer using GPT.
        
        Args:
            query (str): The user's question.
            
        Returns:
            dict: Contains the 'response' (str) and 'context' (List[str]).
        """

        # 1. Serch for context
        # Retrive the top 3 most relevant chunks from the vector database
        context_docs = self.search(query, k=3)
        context_text = "\n\n".join(context_docs)

        # Handle case where no context is found (optional safety check)
        if not context_docs:
            return {
                "response": "I could not find relevant information in the uploaded document.",
                "context": []
            }
        
        # 2. Define Prompt Template
        # Instructions are in English to ensure better adherence by the LLM.
        # We explicitly instruct the model NOT to hallucinate (make things up).
        template = """
        You are an intelligent assistant designed to analyze pharmaceutical documents.
        Answer the user's question based ONLY on the provided context below.
        Respond in the same language as the user's question.
        
        If the answer is not present in the context, clearly state that the information is not available in the document.
        Do not use outside knowledge or make up answers.

        Context:
        {context}

        Question:
        {question}
        """

        prompt = ChatPromptTemplate.from_template(template)

        # 3. Create Chain (LCEL: LangChain Expression Language)
        # Flow: Prompt -> LLM -> String Output
        chain = prompt |  self.llm | StrOutputParser()

        # 4. Invoce Chain
        # This sends the request to OpenAI API
        response_text = chain.invoke({
            "context": context_text,
            "question": query
        })

        return {
            "response": response_text,
            "context": context_docs
        }
    
    async def a_generate_answer_stream(self, query: str):
        """
        Generator function to stream the answer chunk by chunk.
        Yields: str (partial answer)
        """
        # 1. Search
        context_docs = self.search(query, k=3)
        context_text = "\n\n".join(context_docs)

        # 2. Prompt
        template = """
        You are an intelligent assistant designed to analyze pharmaceutical documents.
        Answer the user's question based ONLY on the provided context below.
        Respond in the same language as the user's question.
        
        If the answer is not present in the context, clearly state that the information is not available in the document.

        Context:
        {context}

        Question:
        {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        
        # 3. Chain
        chain = prompt | self.llm | StrOutputParser()
        
        # 4. Stream
        async for chunk in chain.astream({
            "context": context_text,
            "question": query
        }):
            yield chunk
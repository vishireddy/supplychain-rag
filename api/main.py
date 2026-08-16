"""
FastAPI backend for the Supply Chain RAG system (optional bonus)
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
from ingest import ingest_pdfs
from rag import answer_question
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

app = FastAPI(
    title="Supply Chain RAG API",
    description="RAG system for supply chain documents",
    version="1.0.0"
)

CHROMA_DB_PATH = "./chroma_db"
DATA_PATH = "./data"

# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    top_k: int = 5

class SourceInfo(BaseModel):
    file: str
    page: int

class AnswerResponse(BaseModel):
    answer: str
    sources: list[SourceInfo]

class IngestResponse(BaseModel):
    files: int
    chunks: int

class StatsResponse(BaseModel):
    collection_name: str
    total_chunks: int
    embedding_model: str
    llm_model: str

@app.post("/ingest", response_model=IngestResponse)
async def ingest(files: list[UploadFile] = File(...)):
    """
    Ingest one or more PDF files into the vector database.
    
    Returns:
        JSON with number of files and chunks processed
    """
    try:
        os.makedirs(DATA_PATH, exist_ok=True)
        file_paths = []
        
        for file in files:
            file_path = os.path.join(DATA_PATH, file.filename)
            with open(file_path, "wb") as f:
                contents = await file.read()
                f.write(contents)
            file_paths.append(file_path)
        
        files_count, chunks_count = ingest_pdfs(file_paths)
        return IngestResponse(files=files_count, chunks=chunks_count)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):
    """
    Ask a question and get an answer with sources.
    
    Args:
        request: QuestionRequest with 'question' and optional 'top_k'
    
    Returns:
        JSON with answer and sources
    """
    try:
        result = answer_question(request.question)
        
        # Convert sources to SourceInfo format
        sources = [
            SourceInfo(
                file=os.path.basename(source["file"]),
                page=int(source["page"]) if isinstance(source["page"], (int, str)) else 0
            )
            for source in result["sources"]
        ]
        
        return AnswerResponse(answer=result["answer"], sources=sources)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/stats", response_model=StatsResponse)
async def stats():
    """
    Get statistics about the indexed documents.
    
    Returns:
        JSON with collection info and metadata
    """
    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        vectorstore = Chroma(
            collection_name="supplychain",
            embedding_function=embeddings,
            persist_directory=CHROMA_DB_PATH
        )
        
        # Get collection count
        collection = vectorstore._collection
        total_chunks = collection.count()
        
        return StatsResponse(
            collection_name="supplychain",
            total_chunks=total_chunks,
            embedding_model="text-embedding-3-small",
            llm_model="gpt-4o"
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

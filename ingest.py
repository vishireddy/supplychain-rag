"""
Ingestion pipeline: load PDFs, chunk, embed, and store in ChromaDB
Uses local embeddings (no API key required)
"""
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

# Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
CHROMA_DB_PATH = "./chroma_db"
DATA_PATH = "./data"

def load_and_chunk_pdfs(pdf_paths: list) -> list:
    """
    Load PDFs and split them into chunks.
    
    Args:
        pdf_paths: List of PDF file paths
    
    Returns:
        List of chunked documents
    """
    all_documents = []
    
    for pdf_path in pdf_paths:
        print(f"Loading {pdf_path}...")
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        all_documents.extend(documents)
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(all_documents)
    print(f"Created {len(chunks)} chunks from {len(all_documents)} documents")
    
    return chunks

def ingest_pdfs(pdf_paths: list) -> tuple[int, int]:
    """
    Ingest PDFs: load, chunk, embed, and store in ChromaDB.
    
    Args:
        pdf_paths: List of PDF file paths
    
    Returns:
        Tuple of (number of files, number of chunks)
    """
    chunks = load_and_chunk_pdfs(pdf_paths)
    
    # Initialize embeddings and vector store (using local HuggingFace embeddings - no API key needed)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Check if collection already exists
    try:
        vectorstore = Chroma(
            collection_name="supplychain",
            embedding_function=embeddings,
            persist_directory=CHROMA_DB_PATH
        )
        # Add new documents to existing collection
        vectorstore.add_documents(chunks)
    except Exception as e:
        # Create new collection
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name="supplychain",
            persist_directory=CHROMA_DB_PATH
        )
    
    # Persist to disk
    vectorstore.persist()
    
    return len(pdf_paths), len(chunks)

def get_vectorstore():
    """Get the persisted vectorstore."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma(
        collection_name="supplychain",
        embedding_function=embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    return vectorstore

if __name__ == "__main__":
    # Example: ingest provided PDFs
    pdf_files = [
        os.path.join(DATA_PATH, "Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf"),
        os.path.join(DATA_PATH, "Meridian_Procurement_Policy_Handbook_v4.2.pdf")
    ]
    
    files_count, chunks_count = ingest_pdfs(pdf_files)
    print(f"\n✅ Ingestion complete: {files_count} files processed, {chunks_count} chunks stored")

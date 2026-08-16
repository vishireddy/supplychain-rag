"""
RAG module: retrieve relevant documents and generate answers using Groq API
Uses local embeddings (free) + Groq LLM (fast & free tier)
"""
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

CHROMA_DB_PATH = "./chroma_db"
TOP_K = 5  # Number of chunks to retrieve

def get_qa_chain():
    """
    Create and return a QA chain with retrieval from ChromaDB.
    Uses Groq for fast LLM inference (30+ req/min free tier).
    
    Returns:
        Tuple of (chain, vectorstore)
    """
    # Local embeddings - no API key needed
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(
        collection_name="supplychain",
        embedding_function=embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    
    # Groq LLM (ultra-fast, free tier: 30 requests/minute)
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in .env file. Get it from https://console.groq.com")
    
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model="llama-3.1-8b-instant",  # Fast, free model on Groq
        temperature=0.1
    )
    
    # System prompt for honest refusal
    prompt_template = """Answer only from the context provided below. If the context does not contain the answer, say that the information is not available in the uploaded documents.

Context:
{context}

Question: {question}

Answer:"""
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})
    
    # Build RAG chain using modern LangChain API
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain, retriever, vectorstore

def answer_question(question: str) -> dict:
    """
    Answer a question using the RAG system.
    
    Args:
        question: The question to answer
    
    Returns:
        Dictionary with 'answer' and 'sources' (list of source info)
    """
    chain, retriever, vectorstore = get_qa_chain()
    
    # Get answer from chain
    answer = chain.invoke(question)
    
    # Get source documents
    source_docs = retriever.invoke(question)
    
    # Extract sources
    sources = []
    for doc in source_docs:
        source_info = {
            "file": doc.metadata.get("source", "Unknown"),
            "page": doc.metadata.get("page", "N/A")
        }
        sources.append(source_info)
    
    return {
        "answer": answer,
        "sources": sources
    }

if __name__ == "__main__":
    # Example: test the QA system
    question = "What is the approval authority for a purchase order worth ₹1.4 crore?"
    result = answer_question(question)
    
    print(f"Question: {question}")
    print(f"\nAnswer: {result['answer']}")
    print(f"\nSources:")
    for source in result['sources']:
        print(f"  - {source['file']} (Page {source['page']})")

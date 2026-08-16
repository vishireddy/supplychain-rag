"""
Streamlit UI for the Supply Chain RAG system
"""
import streamlit as st
from ingest import ingest_pdfs
from rag import answer_question
import os

st.set_page_config(page_title="Supply Chain RAG", layout="wide")

st.title("📋 Supply Chain RAG System")
st.markdown("Ask questions about procurement policies and supplier performance using AI.")

# Initialize session state
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    st.info("📚 Chunk Size: 1000 characters | Overlap: 150 characters")
    st.markdown("---")
    
    # File uploader
    st.subheader("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        
        if st.button("📥 Index Documents"):
            with st.spinner("Processing documents..."):
                # Save uploaded files
                os.makedirs("./data", exist_ok=True)
                file_paths = []
                for file in uploaded_files:
                    file_path = os.path.join("./data", file.name)
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())
                    file_paths.append(file_path)
                
                # Ingest PDFs
                files_count, chunks_count = ingest_pdfs(file_paths)
                st.success(f"✅ {files_count} files processed, {chunks_count} chunks stored")

# Main content
st.markdown("---")

col1, col2 = st.columns([3, 1])
with col1:
    question = st.text_input(
        "❓ Ask your question:",
        placeholder="e.g., What is the approval authority for a purchase order worth ₹1.4 crore?",
        key="question_input"
    )

with col2:
    submit_button = st.button("🔍 Search", use_container_width=True)

if submit_button and question:
    with st.spinner("Searching through documents..."):
        result = answer_question(question)
        
        # Display answer
        st.markdown("### 💬 Answer")
        st.write(result["answer"])
        
        # Display sources
        if result["sources"]:
            st.markdown("### 📄 Sources")
            for i, source in enumerate(result["sources"], 1):
                file_name = os.path.basename(source["file"])
                page = source["page"]
                st.write(f"**{i}.** {file_name} (Page {page})")
        else:
            st.warning("⚠️ No source documents found for this query.")

elif submit_button:
    st.warning("Please enter a question.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
    Supply Chain RAG System | Using GPT-4o + ChromaDB | text-embedding-3-small
    </div>
    """,
    unsafe_allow_html=True
)

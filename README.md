# Supply Chain RAG System

A Retrieval Augmented Generation (RAG) system for answering questions about supply chain policies and supplier performance using AI. Built with LangChain, ChromaDB, and GPT-4o.

## Overview

This system ingests two PDFs:
1. **Meridian Supply Chain Review** — Supplier scorecards, freight lane costs, inventory metrics, line stoppages, quality data
2. **Meridian Procurement Policy Handbook** — Supplier classifications, penalty clauses, approval limits, safety-stock formulas

It allows users to ask questions that require combining data from both documents (e.g., "What policy clauses does this supplier's performance trigger?").

## Setup

### Prerequisites
- Python 3.10 or higher
- OpenAI API key (obtain from https://platform.openai.com/api-keys)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd supplychain-rag
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Place the provided PDFs in the `data/` folder:**
   - `Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf`
   - `Meridian_Procurement_Policy_Handbook_v4.2.pdf`

## Running the Application

### Streamlit Interface (Recommended)

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`. 

**Steps:**
1. Click "Upload Documents" in the sidebar to load the PDFs
2. Click "Index Documents" to process and store them in ChromaDB
3. Type your question in the search box and click "Search"
4. View the answer with sources (document name and page number)

### FastAPI Backend (Optional Bonus)

To run the REST API:

```bash
python -m uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive API documentation.

**Endpoints:**
- `POST /ingest` — Upload and process PDFs
- `POST /ask` — Submit a question
- `GET /stats` — Get collection statistics

## Configuration

- **Chunk Size:** 1000 characters
- **Chunk Overlap:** 150 characters
- **Reason:** Ensures complete tables and related information stay together; reduces fragmentation of coherent ideas.
- **Top-K Retrieval:** 5 chunks (can be adjusted in code)
- **Embedding Model:** text-embedding-3-small
- **LLM:** GPT-4o with temperature 0.1

## Test Questions

Test your system with these questions from the assignment:

1. **Which supplier had the highest spend in Q1, and what was its on-time delivery percentage?**
   - Single-document answer (from supply chain review)

2. **How many line stoppages happened in Q1, what was the total downtime, and what caused them?**
   - Single-document answer

3. **What is the approval authority for a purchase order worth ₹1.4 crore?**
   - Single-document answer (from policy handbook)

4. **What are the four supplier classification categories, and what qualifies a supplier as Critical?**
   - Single-document answer (from policy handbook)

5. **Kaveri Metals recorded 88.1% on-time delivery and 1,150 defects per million in Q1. Which policy clauses does this trigger, and what exactly must the buyer do?**
   - **Cross-document answer** — Combines metrics from review + clauses from handbook

6. **The microcontroller supplier is single-source. What does the sourcing policy require in this situation, and what is the company already doing about it?**
   - **Cross-document answer** — Requires both documents

7. **Microcontrollers are imported with a 46-day lead time. Using the safety-stock policy, how many days of stock should be held for this part?**
   - **Cross-document answer** — Combines data from review + formula from policy

8. **Trident Circuit Boards had a defect rate of 640 parts per million. What is the cost consequence under the policy?**
   - **Cross-document answer**

9. **Which suppliers would fall below the B rating band on on-time delivery alone, and what is the escalation path for them?**
   - **Cross-document answer**

10. **Deliberate trap question: What is the annual salary of the Head of Procurement?**
    - System should refuse: *"The information is not available in the uploaded documents."*

## Key Features

✅ **Ingestion Pipeline** — Loads PDFs, chunks with recursive splitting, embeds with OpenAI, stores in ChromaDB  
✅ **ChromaDB Persistence** — Vector database persists to disk; survives app restart  
✅ **Multi-Document Retrieval** — Can answer questions combining data from multiple PDFs  
✅ **Source Attribution** — Every answer shows which document and page it came from  
✅ **Honest Refusal** — Refuses to answer questions not in the documents (trap question handling)  
✅ **Streamlit UI** — Clean, user-friendly interface for uploads and queries  
✅ **Optional FastAPI Backend** — REST API for production deployments (+15 bonus marks)

## Architecture

```
supplychain-rag/
├── app.py                     # Streamlit interface
├── ingest.py                  # PDF loading, chunking, embedding
├── rag.py                     # Retrieval + prompt + GPT-4o
├── api/
│   └── main.py               # FastAPI backend (optional)
├── data/                      # PDF files (provided)
├── chroma_db/                 # Persisted vector store
├── requirements.txt           # Python dependencies
├── .env.example              # API key template
├── .gitignore                # Excludes .env and large files
└── README.md                 # This file
```

## Troubleshooting

**Q: "Module not found" error when running**
- Run `pip install -r requirements.txt` again to ensure all dependencies are installed

**Q: "OPENAI_API_KEY not found"**
- Create `.env` file (copy from `.env.example`) and add your OpenAI API key

**Q: ChromaDB folder is huge**
- It's normal for large document collections. The `.gitignore` file excludes it from Git.

**Q: Answers are wrong or irrelevant**
- Check what chunks were retrieved (add `print()` statements in `rag.py`)
- Try increasing `TOP_K` from 5 to 6 in `rag.py` for cross-document questions
- Verify PDFs have selectable text (not scanned images)

## Notes

- **API Costs:** text-embedding-3-small is very cheap (~$0.02 per 1M tokens); GPT-4o is more expensive. Test locally first.
- **Chunking Trade-off:** Larger chunks (1200 chars) keep tables intact but reduce granularity. 1000 is a good middle ground.
- **Temperature:** Set to 0.1 to reduce hallucinations while maintaining coherent answers.
- **Never commit your API key** — Keep `.env` in `.gitignore`

## License

For educational purposes.

## Quick Start Guide

### 1. Install & Setup (5 minutes)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-...
```

### 2. Verify File Structure

Ensure you have the PDFs in the `data/` folder:
- `data/Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf`
- `data/Meridian_Procurement_Policy_Handbook_v4.2.pdf`

### 3. Run the App

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

### 4. Test It

In the sidebar:
- Click "Upload Documents" 
- Click "Index Documents" → You should see: `✅ 2 files processed, ~96 chunks stored`

In the main area:
- Ask: "What is the approval authority for a purchase order worth ₹1.4 crore?"
- You should get an answer with source document and page number

### 5. Verify Persistence

- Close the app (Ctrl+C)
- Run `streamlit run app.py` again
- The old chunks are still searchable without re-uploading ✅

### Test the Trap Question

Ask: "What is the annual salary of the Head of Procurement?"

Expected response: *"The information is not available in the uploaded documents."*

---

## Running FastAPI (Optional)

```bash
python -m uvicorn api.main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API docs.

**Try these:**
- Upload 2 files via `/ingest` → Returns `{"files": 2, "chunks": 96}`
- Ask a question via `/post` with `{"question": "...", "top_k": 5}`
- Get stats via `/stats`

---

## Architecture at a Glance

```
User Question
     ↓
[Streamlit UI] or [FastAPI]
     ↓
[rag.py] → OpenAI Embeddings
     ↓
[ChromaDB] ← Search for top-5 similar chunks
     ↓
[GPT-4o] + Retrieved chunks → Answer
     ↓
[Output with sources]
```

---

## Expected File Structure After Setup

```
supplychain-rag/
├── app.py
├── ingest.py
├── rag.py
├── api/main.py
├── data/
│   ├── Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf
│   └── Meridian_Procurement_Policy_Handbook_v4.2.pdf
├── chroma_db/  ← Created after first indexing
│   └── [vector database files]
├── requirements.txt
├── .env         ← Create this, don't commit
├── .env.example
├── .gitignore
├── README.md
└── QUICKSTART.md  ← You are here
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'streamlit'` | Run `pip install -r requirements.txt` |
| `OPENAI_API_KEY not found` | Create `.env` file with your API key |
| `PDFs not found` | Place PDFs in `data/` folder |
| `Answer is wrong/irrelevant` | Increase `TOP_K` in `rag.py` from 5 to 6 |
| "Information not available" (legitimate Q) | Check retrieval by adding `print()` in `rag.py` |

---

## Marking Checklist

- [ ] Virtual env created and dependencies installed
- [ ] API key in `.env` (not committed)
- [ ] 2 PDFs in `data/` folder
- [ ] `streamlit run app.py` starts without errors
- [ ] Upload → Index shows: `✅ 2 files processed, X chunks stored`
- [ ] Can ask questions and get answers with sources
- [ ] Trap question returns: "information is not available"
- [ ] Close and reopen app → old chunks still searchable (persistence)
- [ ] All 10 test questions answered (Q5-Q9 use both documents)
- [ ] FastAPI endpoints working (optional bonus)

---

## Next Steps

1. **Test all 10 questions** from the assignment (see README.md)
2. **Record a 3-minute demo** showing upload, indexing, queries, trap question
3. **Push to GitHub** with:
   - ✅ All `.py` files
   - ✅ `requirements.txt`
   - ✅ `.env.example` (NOT `.env`)
   - ✅ `README.md` with test results
   - ✅ PDFs in `data/` folder
   - ✅ `.gitignore` excluding `.env` and `chroma_db/`
4. **Submit**: GitHub link + 3-minute demo video

Good luck! 🚀

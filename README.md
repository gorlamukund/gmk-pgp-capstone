# 🤖 SAP BTP Document Assistant

A Generative AI-powered document assistant for SAP Engineers built using RAG (Retrieval-Augmented Generation) and Agentic AI frameworks.

---

## Overview
The SAP BTP Document Assistant allows users to upload enterprise documents and ask natural language questions. The system retrieves relevant content using a vector database and generates accurate, grounded responses using Claude AI.

In this scenario, the documents uploaded are related to SAP Business Technology Platform and AI Services using their framework called Joule.
---

## Tech Stack

| Component    | Technology |
|--------------|------------|
| Language     | Python 3.13.2 |
| LLM          | Claude (Anthropic API) |
| Framework    | LlamaIndex |
| Vector Store | ChromaDB |
| Embeddings   | HuggingFace (BAAI/bge-small-en-v1.5) |
| UI           | Streamlit |
| Deployment   | Render |

---

## System Architecture

User Interface (Streamlit)
↓
Input Validation (validator.py)
↓
Document Upload → DocumentProcessor → IngestionService → ChromaDB
↓
User Query → DocumentAgent (Claude AI)
↓
RetrieverService → ChromaDB (Similarity Search)
↓
RAG Pipeline → Claude generates grounded answer
↓
Guardrails (guardrails.py) → Validated Response
↓
User Interface (Streamlit)

---

## Agent Workflow

The system uses an AI agent with the following roles:

| Role      | Description                                       |
|-----------|---------------------------------------------------|
| Planner   | Decides the tool to use based on the question.    |
| Retriever | Searches ChromaDB for relevant document chunks    |
| Reasoner  | Analyzes retrieved content to formulate an answer |
| Responder | Generates the final grounded response              |

---

## Project Structure
gmk-pgp-capstone/
├── app/
│   ├── agents/
│   │   ├── agent.py          # ReActAgent with Anthropic tool calling
│   │   └── tools.py          # Agent tools definition
│   ├── core/
│   │   ├── config.py         # Central configuration
│   │   └── rag_pipeline.py   # RAG pipeline
│   ├── services/
│   │   ├── document_processor.py  # Document text extraction
│   │   ├── ingestion.py           # Chunking & ChromaDB storage
│   │   └── retriever.py           # Semantic similarity search
│   └── utils/
│       ├── validator.py      # Input validation
│       └── guardrails.py     # Output safety checks
├── data/                     # SAP BTP documentation
├── chroma_db/                # ChromaDB vector store
├── main.py                   # Entry point
├── streamlit_app.py          # Streamlit UI
├── ingest_docs.py            # Document ingestion script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not shared)
└── README.md                 # Project documentation

---

## Setup Instructions

### Prerequisites
- Python 3.13.2
- Anthropic API key

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd gmk-pgp-capstone
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
   - Open the `.env` file
   - Replace `your_anthropic_api_key_here` with your actual Anthropic API key
   - Get your API key from `https://console.anthropic.com`

5. Ingest documents:
```bash
python ingest_docs.py
```

6. Run the application:
```bash
streamlit run streamlit_app.py
```

---

## Usage

1. Open the app at `http://localhost:8501`
2. Upload documents using the sidebar (PDF, TXT, CSV, Excel, JSON, YAML, Markdown)
3. Type your question in the chat input
4. The AI agent retrieves relevant content and generates a grounded answer

---

## Safety Controls

- **Input Validation** — file size limit (10MB), query length checks, prompt injection detection
- **Output Guardrails** — empty response handling, grounding verification, warning flags
- **Error Handling** — all exceptions caught and displayed gracefully

---

## Limitations

- ChromaDB is stored locally — evaluators must run `ingest_docs.py` to populate the vector store
- Response quality depends on the relevance of uploaded documents
- Large documents may take time to ingest
- Supports English language documents only
- Maximum file size is 10MB per upload

---

## Assumptions

- User has a valid Anthropic API key
- Python 3.10 or higher is installed
- Internet connection required for Anthropic API calls and HuggingFace model download

---

## Security Considerations

- API keys stored in `.env` file — never committed to Git
- `.gitignore` excludes `.env`, `chroma_db/`, and `data/` folders
- Input validation prevents prompt injection attacks
- File size limits prevent denial of service

---

## Challenges Faced

- LlamaIndex version conflicts resolved by removing pinned versions
- ReActAgent API changed in newer LlamaIndex versions — switched to native Anthropic tool calling
- `.md` file support required adding a custom `_process_markdown` method
- Model name format differences between LlamaIndex Anthropic plugin versions

---

## Deployment Guide

### Option 1 — Run Locally (Recommended for Evaluation)

1. Follow the Setup Instructions above
2. Run the app:
```bash
streamlit run streamlit_app.py
```
3. Open browser at `http://localhost:8501`

### Option 2 — Deploy to Render

1. Create a free account at `https://render.com`
2. Connect your GitHub repository
3. Create a new **Web Service**
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
5. Add environment variables from `.env` file
6. Click **Deploy**

### Option 3 — Docker

1. Create a `Dockerfile`:
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
2. Build and run:
```bash
docker build -t sap-btp-assistant .
docker run -p 8501:8501 sap-btp-assistant
```
---

## Capstone Project

This is developed as part of the **Post Graduate Program in Generative AI and ML** program by edureka! / Illinois Tech.

**Submitted by:** Mukund Gorla  
**Submission Date:** June 11, 2026
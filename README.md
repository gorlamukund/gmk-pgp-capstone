# 🤖 SAP BTP Document Assistant

A Generative AI-powered document assistant for SAP Engineers built using RAG (Retrieval-Augmented Generation) and Agentic AI frameworks.

---

## Overview
The SAP BTP Document Assistant allows users to upload enterprise documents and ask natural language questions. The system retrieves relevant content using a vector database and generates accurate, grounded responses using Claude AI.

In this scenario, the documents uploaded are related to SAP Business Technology Platform and AI Services using their framework called Joule.
---

## Tech Stack

| Component    | Technology                           |
|--------------|--------------------------------------|
| Language     | Python 3.13.2                        |
| LLM          | Claude (Anthropic API)               |
| Framework    | LlamaIndex                           |
| Vector Store | ChromaDB                             |
| Embeddings   | HuggingFace (BAAI/bge-small-en-v1.5) |
| UI           | Streamlit                            |
| Deployment   | Render                               |

---

## System Architecture

### Document Ingestion Flow (one-time setup)
User uploads document
↓
Input Validation (validator.py)
↓
DocumentProcessor → IngestionService → ChromaDB

### Query Flow
User Question
↓
Streamlit UI (streamlit_app.py)
↓
Input Validation (validator.py)
↓
DocumentAgent → ReActAgent (agent.py)
↓
tools.py → search_documents / summarize_topic
↓
RetrieverService → ChromaDB (Similarity Search)
↓
Claude LLM generates grounded answer
↓
Guardrails (guardrails.py) → Validated Response
↓
Streamlit UI displays answer to User

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
│   │   ├── agent.py          # LlamaIndex ReActAgent (active)
|   |   ├── agent_sdk.py      # Anthropic SDK implementation (reference)
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

   **If using the zip file:**
   - Open the `.env` file
   - Replace `your_anthropic_api_key_here` with your actual Anthropic API key
   - Get your API key from `https://console.anthropic.com`

   **If cloning from GitHub:**
   - Copy `.env.example` to `.env`:
```bash
     cp .env.example .env
```
   - Open `.env` and replace `your_anthropic_api_key_here` with your actual Anthropic API key
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

## UI Usage Guide

### Main Interface
The application has two main areas:

**Sidebar (left panel):**
- **Document Upload** — upload your own documents (PDF, TXT, CSV, Excel, JSON, YAML, Markdown)
- **Ingested Documents** — shows list of successfully uploaded documents
- **Clear Chat History** — resets the conversation

**Main Panel:**
- **System Status** — confirms app is running with model and version info
- **Chat Interface** — type your questions in the input box at the bottom
- **Chat History** — all questions and answers displayed in conversation format

---

### How to Use

**Step 1 — Start the app:**
```bash
streamlit run streamlit_app.py
```

**Step 2 — Ingest documents (first time only):**
```bash
python ingest_docs.py
```
This loads the SAP BTP documentation into ChromaDB.

**Step 3 — Upload additional documents (optional):**
- Click **Browse files** in the sidebar
- Select your document
- Wait for the success message

**Step 4 — Ask questions:**
- Type your question in the chat input at the bottom
- Press **Enter**
- Wait for the AI agent to retrieve and generate an answer

---

### Example Questions
- `What is SAP AI Core?`
- `How do I create a deployment in SAP AI Launchpad?`
- `What are the key features of SAP AI Core?`
- `How do I manage resource groups?`
- `What are the service plans available in SAP AI Core?`

---

### Input Validation Rules
| Rule                 | Limit                               |
|----------------------|-------------------------------------|
| Minimum query length | 3 characters                        |
| Maximum query length | 500 characters                      |
| Maximum file size     | 10 MB                               |
| Supported file types  | PDF, TXT, CSV, XLSX, JSON, YAML, MD |

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
- ReActAgent API changed in newer LlamaIndex versions — resolved by migrating to LlamaIndex ReActAgent with ThreadPoolExecutor to handle uvloop/Streamlit async conflict on macOS
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
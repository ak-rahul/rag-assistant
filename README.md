# RAG Assistant (polished)

Production-ready RAG assistant using LangChain + Chroma + Groq, with CLI, API, and Streamlit UI.

## Stack
- LangChain + Chroma (persistent vector store)
- LLM: Groq (default). Optional OpenAI.
- Embeddings: sentence-transformers (local)
- Config: `config.yaml` + `.env` (dotenv)
- CLI: Typer
- API: FastAPI (Uvicorn)
- UI: Streamlit
- Logging: Loguru

## Quickstart (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -U pip
pip install -r requirements.txt

Copy-Item .env.example .env
# set GROQ_API_KEY in .env

# Ingest documents in ./data
python cli.py ingest

# Ask a question
python cli.py query "What is this project about?"

# Run API
python cli.py serve

# Launch UI
python cli.py web

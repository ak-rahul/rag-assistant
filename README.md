
# RAG Assistant (Polished, v1-style)

A production-ready RAG assistant mirroring the stack and conventions of `rag-v1-main`.

## Stack
- LangChain + Chroma (vector store)
- LLM: **Groq** (default). Set `GROQ_API_KEY` in `.env`
- Embeddings: Sentence-Transformers (default, local) — switchable to OpenAI
- Config: `config.yaml` + `.env` (dotenv)
- CLI: Typer
- UI: Streamlit
- API: FastAPI
- Logging: Loguru (console + rotating file)
- Docker + Compose
- Dev tools: pytest, black, flake8, jupyter

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

cp .env.example .env
# set GROQ_API_KEY=... in .env

# ingest
python -m rag_v1_style.cli ingest --source ./data --pattern "**/*.*"

# ask
python -m rag_v1_style.cli ask "What is this project about?"

# api
python -m rag_v1_style.cli serve --host 0.0.0.0 --port 8000

# ui
python -m rag_v1_style.cli ui
```

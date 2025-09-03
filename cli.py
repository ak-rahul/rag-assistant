# cli.py
import typer
from src.pipeline.rag_pipeline import RAGPipeline
from src.config import load_config
import os
from src.utils.logger import configure
from loguru import logger
import requests
from dotenv import load_dotenv

load_dotenv()
app = typer.Typer()
pipeline = RAGPipeline()
cfg = load_config()

@app.command()
def ingest(path: str):
    """Ingest a file or folder into the vector store"""
    if os.path.isdir(path):
        count = pipeline.chroma.add_documents  # placeholder - we'll use ingest_folder imported
        from src.ingestion.ingest import ingest_folder
        n = ingest_folder(path, pipeline.chroma, chunk_size=cfg["ingestion"]["chunk_size"], chunk_overlap=cfg["ingestion"]["chunk_overlap"])
        typer.echo(f"Ingested {n} chunks from folder {path}")
    else:
        n = pipeline.ingest(path)
        typer.echo(f"Ingested {n} chunks from file {path}")

@app.command()
def query(question: str):
    """Query the RAG system: retrieve context and call LLM"""
    res = pipeline.query(question)
    context = res["context"]
    # Call GROQ or fallback LLM
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        prompt = f"{pipeline.prompt.template}\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
        # simple call to GROQ endpoint (wrapper would be better)
        url = "https://api.groq.ai/v1/generate"
        headers = {"Authorization": f"Bearer {groq_key}"}
        payload = {"prompt": prompt, "temperature": cfg.get("llm", {}).get("temperature", 0.2), "max_tokens": cfg.get("llm", {}).get("max_tokens", 512)}
        r = requests.post(url, json=payload, headers=headers, timeout=60)
        r.raise_for_status()
        output = r.json()
        answer = output.get("text") or output.get("output") or output
        typer.echo("Answer:\n")
        typer.echo(answer)
    else:
        typer.echo("GROQ_API_KEY not configured — returning context only.\n")
        typer.echo(context)

@app.command()
def web():
    """Run Streamlit UI"""
    os.system("streamlit run app.py")

@app.command()
def stats():
    s = pipeline.stats()
    typer.echo(s)

@app.command()
def clear():
    ok = pipeline.clear()
    typer.echo("Cleared DB" if ok else "Failed to clear DB")

if __name__ == "__main__":
    app()

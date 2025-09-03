# cli.py
import os
import typer
import streamlit.web.cli as stcli
import sys
from dotenv import load_dotenv
from src.pipeline.rag_pipeline import RAGPipeline
from src.config import load_config
from src.logger import configure

app = typer.Typer(add_completion=False)
load_dotenv()

@app.callback()
def _init():
    cfg = load_config()
    logcfg = cfg.get("logging", {})
    configure(
        log_dir=logcfg.get("dir", "./logs"),
        level=logcfg.get("level", "INFO"),
        json_logs=logcfg.get("json", False),
    )

@app.command(help="Ingest documents from the configured data folder.")
def ingest():
    pipe = RAGPipeline()
    count = pipe.ingest_folder()
    typer.echo(f"Ingested chunks: {count}")

@app.command(help="Query the RAG pipeline.")
def query(question: str):
    pipe = RAGPipeline()
    answer, sources = pipe.ask(question)
    typer.echo(answer)
    if sources:
        typer.echo("\nSources:")
        for s in sources:
            typer.echo(f"- {s.metadata.get('source', 'unknown')}")

@app.command(help="Run FastAPI server.")
def serve(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
    import uvicorn
    uvicorn.run("src.server:app", host=host, port=port, reload=reload)

@app.command(help="Open Streamlit UI.")
def web():
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())

@app.command(help="Show vector store stats.")
def stats():
    pipe = RAGPipeline()
    typer.echo(pipe.stats())

@app.command(help="Clear the vector store collection.")
def clear():
    pipe = RAGPipeline()
    ok = pipe.clear()
    typer.echo("Cleared DB" if ok else "Failed to clear DB")

if __name__ == "__main__":
    app()

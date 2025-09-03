
import typer, json, os
from typing import Optional
from .pipeline import RAGPipeline

app = typer.Typer(add_completion=False)
pipeline = RAGPipeline()

@app.command()
def ingest(source: Optional[str] = typer.Option(None, help="Directory of docs"),
           pattern: Optional[str] = typer.Option(None, help="Glob pattern, e.g. '**/*.pdf'")):
    n = pipeline.ingest(source, pattern)
    typer.echo(f"Ingested chunks: {n}")

@app.command()
def ask(question: str):
    result = pipeline.ask(question)
    typer.echo(json.dumps(result, indent=2))

@app.command()
def stats():
    typer.echo(json.dumps(pipeline.stats(), indent=2))

@app.command()
def clear():
    ok = pipeline.clear()
    typer.echo("Cleared" if ok else "Failed to clear")    

@app.command()
def serve(host: str = "0.0.0.0", port: int = 8000):
    import uvicorn
    from .server import app as fastapi_app
    uvicorn.run(fastapi_app, host=host, port=port)

@app.command()
def ui():
    os.system("streamlit run -m rag_v1_style.ui.app")

if __name__ == "__main__":
    app()

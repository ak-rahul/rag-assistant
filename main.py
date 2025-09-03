import typer
from src.utils.config_loader import ConfigLoader
from src.utils.log_manager import LogManager
from src.ingestion.document_loader import DocumentLoader
from src.rag_pipeline import RAGPipeline
from pathlib import Path

app = typer.Typer()
config = ConfigLoader()
logger = LogManager(log_dir=config.get("logging.log_dir"))
doc_loader = DocumentLoader(config.get("ingestion.supported_formats"))
rag_pipeline = RAGPipeline(config, logger)

@app.command()
def ingest(path: str):
    """Ingest document(s) into vector store"""
    path = Path(path)
    if path.is_dir():
        files = list(path.glob("*"))
    else:
        files = [path]
    docs = []
    for f in files:
        try:
            text = doc_loader.load_document(str(f))
            docs.append(text)
            logger.info(f"Ingested {f}")
        except Exception as e:
            logger.error(f"Failed to load {f}: {e}")
    rag_pipeline.add_documents(docs)

@app.command()
def query(question: str):
    """Ask a question to the RAG system"""
    result = rag_pipeline.query(question)
    print("Answer:", result.get("result"))
    print("Sources:", [doc.metadata for doc in result.get("source_documents", [])])

@app.command()
def interactive():
    """Interactive CLI mode"""
    while True:
        q = input("Enter your question (or 'exit' to quit): ")
        if q.lower() == "exit":
            break
        query(q)

if __name__ == "__main__":
    app()

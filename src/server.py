# src/server.py
from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline.rag_pipeline import RAGPipeline

app = FastAPI(title="RAG Assistant API", version="1.0.0")
pipe = RAGPipeline()

class AskRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/stats")
def stats():
    return pipe.stats()

@app.post("/ask")
def ask(req: AskRequest):
    answer, sources = pipe.ask(req.question)
    return {
        "answer": answer,
        "sources": [s.metadata.get("source", "unknown") for s in sources],
    }

@app.post("/ingest")
def ingest():
    count = pipe.ingest_folder()
    return {"ingested_chunks": count}


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .pipeline import RAGPipeline

app = FastAPI(title="RAG Assistant API", version="1.0.0")
pipeline = RAGPipeline()

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    sources: list[str]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
def ask(body: AskRequest):
    try:
        res = pipeline.ask(body.question)
        return AskResponse(**res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class IngestRequest(BaseModel):
    source: str | None = None
    pattern: str | None = None

@app.post("/ingest")
def ingest(body: IngestRequest):
    try:
        n = pipeline.ingest(body.source, body.pattern)
        return {"chunks": n}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

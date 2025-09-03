
from __future__ import annotations
from pathlib import Path
from typing import Optional, List, Literal
from pydantic import BaseModel
import yaml
from dotenv import load_dotenv

load_dotenv()

class DataCfg(BaseModel):
    source_dir: str = "./data"
    glob_pattern: str = "**/*.*"
    allowed_ext: List[str] = [".pdf", ".docx", ".txt", ".md"]
    chunk_size: int = 1200
    chunk_overlap: int = 150

class EmbeddingsCfg(BaseModel):
    provider: Literal["sentence-transformers","openai"] = "sentence-transformers"
    model: str = "sentence-transformers/all-MiniLM-L6-v2"
    device: str = "auto"

class VectorStoreCfg(BaseModel):
    type: Literal["chroma"] = "chroma"
    persist_dir: str = "./.chroma"
    collection: str = "rag-assistant"

class RetrieverCfg(BaseModel):
    k: int = 4
    search_type: Literal["similarity","mmr"] = "similarity"

class LLMCfg(BaseModel):
    provider: Literal["groq","openai"] = "groq"
    model: str = "llama-3.1-70b-versatile"
    temperature: float = 0.2
    max_tokens: int = 512

class MemoryCfg(BaseModel):
    enabled: bool = True
    k: int = 5

class LoggingCfg(BaseModel):
    level: str = "INFO"
    json: bool = False
    dir: str = "./logs"

class ServerCfg(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

class Settings(BaseModel):
    data: DataCfg = DataCfg()
    embeddings: EmbeddingsCfg = EmbeddingsCfg()
    vectorstore: VectorStoreCfg = VectorStoreCfg()
    retriever: RetrieverCfg = RetrieverCfg()
    llm: LLMCfg = LLMCfg()
    memory: MemoryCfg = MemoryCfg()
    logging: LoggingCfg = LoggingCfg()
    server: ServerCfg = ServerCfg()

def load_config(path: str = "config.yaml") -> Settings:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    with p.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return Settings(**raw)

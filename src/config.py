# src/config.py
from pathlib import Path
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

def load_config(path: str = "config.yaml"):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(p, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    # Allow .env overrides for a few keys
    cfg.setdefault("vector_store", {})
    cfg["vector_store"]["persist_directory"] = os.getenv("CHROMA_PERSIST_DIR", cfg["vector_store"].get("persist_directory"))
    cfg.setdefault("ingestion", {})
    cfg["ingestion"]["chunk_size"] = int(os.getenv("CHUNK_SIZE", cfg["ingestion"].get("chunk_size", 500)))
    cfg["ingestion"]["chunk_overlap"] = int(os.getenv("CHUNK_OVERLAP", cfg["ingestion"].get("chunk_overlap", 50)))
    cfg.setdefault("logging", {})
    cfg["logging"]["dir"] = os.getenv("LOG_DIR", cfg["logging"].get("dir", "./logs"))
    cfg["logging"]["level"] = os.getenv("LOG_LEVEL", cfg["logging"].get("level", "INFO"))
    cfg.setdefault("llm", {})
    return cfg

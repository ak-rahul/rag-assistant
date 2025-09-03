# src/config.py
from pathlib import Path
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

def _bool(x, default=False):
    if x is None:
        return default
    return str(x).lower() in {"1", "true", "yes", "on"}

def load_config(path: str = "config.yaml") -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with p.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    # Defaults
    cfg.setdefault("data", {})
    cfg.setdefault("vector_store", {})
    cfg.setdefault("ingestion", {})
    cfg.setdefault("logging", {})
    cfg.setdefault("llm", {})
    cfg.setdefault("memory", {"enabled": True, "k": 5})

    # .env overrides
    vs = cfg["vector_store"]
    vs["persist_directory"] = os.getenv("CHROMA_PERSIST_DIR", vs.get("persist_directory", "./.chroma"))

    ing = cfg["ingestion"]
    ing["chunk_size"] = int(os.getenv("CHUNK_SIZE", ing.get("chunk_size", 1200)))
    ing["chunk_overlap"] = int(os.getenv("CHUNK_OVERLAP", ing.get("chunk_overlap", 150)))

    log = cfg["logging"]
    log["dir"] = os.getenv("LOG_DIR", log.get("dir", "./logs"))
    log["level"] = os.getenv("LOG_LEVEL", log.get("level", "INFO"))
    log["json"] = _bool(os.getenv("LOG_JSON", log.get("json", False)))

    return cfg

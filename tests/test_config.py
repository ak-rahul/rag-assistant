
from rag_v1_style.config import load_config

def test_load_config():
    cfg = load_config("config.yaml")
    assert cfg.llm.provider in {"groq","openai"}
    assert cfg.vectorstore.type == "chroma"

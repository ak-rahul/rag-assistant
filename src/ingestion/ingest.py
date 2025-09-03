# src/ingestion/ingest.py
from pathlib import Path
from langchain.docstore.document import Document
from src.utils.file_loader import FileLoader
from src.utils.text_splitter import split_text
from loguru import logger

def ingest_file(path: str, chroma_handler, chunk_size: int = 500, chunk_overlap: int = 50):
    logger.info(f"Ingesting file: {path}")
    text = FileLoader.load(path)
    chunks = split_text(text, chunk_size=chunk_size, overlap=chunk_overlap)
    docs = [Document(page_content=c, metadata={"source": str(Path(path))}) for c in chunks if c.strip()]
    chroma_handler.add_documents(docs)
    logger.info(f"Added {len(docs)} chunks from {path}")
    return len(docs)

def ingest_folder(folder: str, chroma_handler, chunk_size: int = 500, chunk_overlap: int = 50):
    p = Path(folder)
    files = [f for f in p.rglob("*") if f.is_file()]
    total = 0
    for f in files:
        try:
            total += ingest_file(str(f), chroma_handler, chunk_size, chunk_overlap)
        except Exception as e:
            logger.error(f"Failed to ingest {f}: {e}")
    return total

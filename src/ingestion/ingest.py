# src/ingestion/ingest.py
import hashlib
from pathlib import Path
from typing import Iterable, List

# Compatibility with new/old LangChain core
try:
    from langchain_core.documents import Document
except Exception:
    from langchain.schema import Document  # type: ignore

from loguru import logger
from src.utils.file_loader import FileLoader
from src.utils.text_splitter import get_splitter


def file_hash(path: Path) -> str:
    """Return SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_files(root: Path, allowed_ext: Iterable[str]):
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in allowed_ext:
            yield p


def ingest_path(path: Path, chunk_size: int, chunk_overlap: int) -> List[Document]:
    text = FileLoader.load(str(path))
    splitter = get_splitter(chunk_size, chunk_overlap)
    chunks = splitter.split_text(text)
    filehash = file_hash(path)
    docs = [
        Document(
            page_content=c,
            metadata={"source": str(path), "filehash": filehash},
        )
        for c in chunks if c.strip()
    ]
    return docs


def ingest_folder(
    folder: str,
    chroma_handler,
    allowed_ext=None,
    chunk_size: int = 1200,
    chunk_overlap: int = 150,
) -> int:
    root = Path(folder)
    if allowed_ext is None:
        allowed_ext = FileLoader.SUPPORTED

    total = 0
    for f in iter_files(root, allowed_ext):
        try:
            # Check if this filehash already exists
            fhash = file_hash(f)
            existing = chroma_handler.vectordb.get(where={"filehash": fhash})
            if existing and len(existing["ids"]) > 0:
                logger.info(f"Skipped {f} (already ingested)")
                continue

            docs = ingest_path(f, chunk_size, chunk_overlap)
            if docs:
                chroma_handler.add_documents(docs)
                total += len(docs)
                logger.info(f"Added {len(docs)} chunks from {f}")
        except Exception as e:
            logger.error(f"Failed to ingest {f}: {e}")
    return total

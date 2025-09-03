
from pathlib import Path
from typing import Iterable, List
from langchain.schema import Document
from .document_loader import load_text
from utils.text_splitter import split_text

def iter_files(source_dir: Path, pattern: str, allowed_ext: Iterable[str]):
    allowed = {e.lower() for e in allowed_ext}
    return [p for p in source_dir.rglob(pattern) if p.is_file() and p.suffix.lower() in allowed]

def ingest_dir(source_dir: Path, pattern: str, allowed_ext, chunk_size: int, chunk_overlap: int) -> List[Document]:
    docs: List[Document] = []
    for p in iter_files(source_dir, pattern, allowed_ext):
        chunks = split_text(load_text(p), chunk_size, chunk_overlap)
        docs.extend([Document(page_content=c, metadata={"source": str(p), "chunk": i}) for i, c in enumerate(chunks)])
    return docs

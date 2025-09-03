# src/utils/file_loader.py
from pathlib import Path
from typing import Optional
from pypdf import PdfReader
import docx
import json

class FileLoader:
    SUPPORTED = {".pdf", ".docx", ".txt", ".md", ".json"}

    @staticmethod
    def load(path: str) -> str:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(path)
        ext = p.suffix.lower()
        if ext not in FileLoader.SUPPORTED:
            raise ValueError(f"Unsupported file type: {ext}")

        if ext == ".pdf":
            return FileLoader._load_pdf(p)
        if ext == ".docx":
            return FileLoader._load_docx(p)
        if ext in {".txt", ".md"}:
            return FileLoader._load_text(p)
        if ext == ".json":
            return FileLoader._load_json(p)
        raise ValueError(f"Unhandled file extension: {ext}")

    @staticmethod
    def _load_pdf(p: Path) -> str:
        reader = PdfReader(str(p))
        parts = []
        for page in reader.pages:
            text = page.extract_text() or ""
            if text.strip():
                parts.append(text)
        return "\n".join(parts)

    @staticmethod
    def _load_docx(p: Path) -> str:
        document = docx.Document(str(p))
        return "\n".join([para.text for para in document.paragraphs if para.text.strip()])

    @staticmethod
    def _load_text(p: Path) -> str:
        return p.read_text(encoding="utf-8", errors="ignore")

    @staticmethod
    def _load_json(p: Path) -> str:
        data = json.loads(p.read_text(encoding="utf-8"))
        return json.dumps(data, ensure_ascii=False, indent=2)

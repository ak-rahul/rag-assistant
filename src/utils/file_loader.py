# src/utils/file_loader.py
from pathlib import Path
from pypdf import PdfReader
import docx
import json

class FileLoader:
    SUPPORTED = ["pdf", "docx", "txt", "json"]

    @staticmethod
    def load(path: str) -> str:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(path)
        ext = p.suffix.lower().lstrip(".")
        if ext not in FileLoader.SUPPORTED:
            raise ValueError(f"Unsupported extension: {ext}")
        if ext == "pdf":
            return FileLoader._load_pdf(p)
        if ext == "docx":
            return FileLoader._load_docx(p)
        if ext == "txt":
            return FileLoader._load_txt(p)
        if ext == "json":
            return FileLoader._load_json(p)

    @staticmethod
    def _load_pdf(p: Path) -> str:
        text = []
        reader = PdfReader(p)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text.append(page_text)
        return "\n".join(text)

    @staticmethod
    def _load_docx(p: Path) -> str:
        doc = docx.Document(p)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

    @staticmethod
    def _load_txt(p: Path) -> str:
        return p.read_text(encoding="utf-8")

    @staticmethod
    def _load_json(p: Path) -> str:
        data = json.loads(p.read_text(encoding="utf-8"))
        return json.dumps(data, ensure_ascii=False)

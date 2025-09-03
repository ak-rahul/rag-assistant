
from pathlib import Path
from pypdf import PdfReader
from docx import Document as DocxDocument
import markdown

def load_text(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if ext == ".docx":
        doc = DocxDocument(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    if ext in {".txt", ".md"}:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if ext == ".md":
            text = markdown.markdown(text)
        return text
    raise ValueError(f"Unsupported file: {path}")

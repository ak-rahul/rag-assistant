from pathlib import Path
from typing import List
from PyPDF2 import PdfReader
import docx
import json

class DocumentLoader:
    def __init__(self, supported_formats=["pdf", "docx", "txt", "json"]):
        self.supported_formats = supported_formats

    def load_document(self, filepath: str) -> str:
        ext = Path(filepath).suffix.lower()[1:]
        if ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {ext}")
        if ext == "pdf":
            return self._load_pdf(filepath)
        elif ext == "docx":
            return self._load_docx(filepath)
        elif ext == "txt":
            return self._load_txt(filepath)
        elif ext == "json":
            return self._load_json(filepath)

    def _load_pdf(self, filepath):
        text = ""
        reader = PdfReader(filepath)
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def _load_docx(self, filepath):
        doc = docx.Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs])

    def _load_txt(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    def _load_json(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return json.dumps(data)
        elif isinstance(data, list):
            return "\n".join([json.dumps(d) for d in data])
        return str(data)

# src/utils/text_splitter.py
from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_splitter(chunk_size: int = 1200, chunk_overlap: int = 150):
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

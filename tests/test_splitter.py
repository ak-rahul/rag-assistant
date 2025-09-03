
from rag_v1_style.utils.text_splitter import split_text

def test_splitter():
    chunks = split_text("hello world " * 100, chunk_size=50, chunk_overlap=10)
    assert len(chunks) > 1

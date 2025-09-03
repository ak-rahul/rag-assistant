# src/db/chroma_handler.py
from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

class ChromaHandler:
    def __init__(self, persist_directory: str, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.vectordb = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
        )

    def add_documents(self, docs):
        self.vectordb.add_documents(docs)
        self.vectordb.persist()

    def as_retriever(self, k: int = 4):
        return self.vectordb.as_retriever(search_kwargs={"k": k})

    def persist(self):
        self.vectordb.persist()

    def clear(self) -> bool:
        try:
            self.vectordb._collection.delete()
            self.vectordb.persist()
            return True
        except Exception:
            return False

    def get_collection_info(self):
        try:
            col = self.vectordb._collection
            ids = col.get()["ids"]
            return {"n_vectors": len(ids)}
        except Exception:
            return {"n_vectors": "unknown"}

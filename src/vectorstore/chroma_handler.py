
from typing import Optional, List
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

class ChromaHandler:
    def __init__(self, persist_dir: str, collection: str, embedding_function):
        self.persist_dir = persist_dir
        self.collection = collection
        self.embedding_function = embedding_function
        self._vs: Optional[Chroma] = None

    @property
    def vs(self) -> Chroma:
        if self._vs is None:
            self._vs = Chroma(
                collection_name=self.collection,
                persist_directory=self.persist_dir,
                embedding_function=self.embedding_function,
            )
        return self._vs

    def add_documents(self, docs: List[Document]):
        self.vs.add_documents(docs)
        self.vs.persist()

    def as_retriever(self, k: int = 4, search_type: str = "similarity"):
        return self.vs.as_retriever(search_kwargs={"k": k}, search_type=search_type)

    def clear(self) -> bool:
        try:
            self.vs.delete_collection()
            self._vs = None
            return True
        except Exception:
            return False

    def stats(self):
        try:
            return {"collection": self.collection, "persist_dir": self.persist_dir, "count": self.vs._collection.count()}
        except Exception:
            return {"collection": self.collection, "persist_dir": self.persist_dir, "count": None}

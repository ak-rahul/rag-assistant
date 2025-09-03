# src/pipeline/rag_pipeline.py
from src.db.chroma_handler import ChromaHandler
from src.config import load_config
from src.utils import file_loader
from src.utils.text_splitter import split_text
from src.ingestion.ingest import ingest_file
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src.utils.logger import configure
from loguru import logger

class RAGPipeline:
    def __init__(self, config_path: str = "config.yaml"):
        cfg = load_config(config_path)
        logcfg = cfg.get("logging", {})
        configure(log_dir=logcfg.get("dir", "./logs"), level=logcfg.get("level", "INFO"), json_logs=logcfg.get("json", True))
        vs = cfg.get("vector_store", {})
        persist_dir = vs.get("persist_directory", "./data/processed")
        embedding_model = vs.get("embedding_model", "sentence-transformers/all-MiniLM-L6-v2")
        self.top_k = vs.get("top_k", 5)
        self.chroma = ChromaHandler(persist_directory=persist_dir, embedding_model=embedding_model)
        # simple prompt template
        self.prompt = PromptTemplate(input_variables=["context", "question"],
                                     template="Use the context to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:")

    def ingest(self, path: str):
        cfg = load_config()
        chunk_size = cfg.get("ingestion", {}).get("chunk_size", 500)
        chunk_overlap = cfg.get("ingestion", {}).get("chunk_overlap", 50)
        return ingest_file(path, self.chroma, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def query(self, question: str):
        retriever = self.chroma.as_retriever(k=self.top_k)
        qa = RetrievalQA.from_chain_type(llm=None, chain_type="stuff", retriever=retriever, return_source_documents=True, chain_type_kwargs={"prompt": self.prompt})
        # Note: llm is None — we will call GROQ separately using the retrieved context
        docs = retriever.get_relevant_documents(question)
        context = "\n---\n".join([d.page_content for d in docs])
        # return context and docs for external LLM call
        return {"context": context, "documents": docs}

    def clear(self):
        return self.chroma.clear()

    def stats(self):
        return self.chroma.get_collection_info()

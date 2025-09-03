
from pathlib import Path
from typing import Optional, Dict, Any
from loguru import logger
from .config import load_config, Settings
from .utils.logger import configure as configure_logger
from .utils.embeddings import build_embeddings
from .utils.llm import build_llm
from .vectorstore.chroma_handler import ChromaHandler
from .ingestion.ingest import ingest_dir
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

DEFAULT_PROMPT = PromptTemplate(
    input_variables=["context","question"],
    template=(
        "You are a helpful assistant. Use only the context to answer.\n\n"
        "Context:\n{context}\n\nQuestion: {question}\n\n"
        "Answer concisely and cite sources if relevant."
    ),
)

class RAGPipeline:
    def __init__(self, config_path: str = "config.yaml"):
        self.cfg: Settings = load_config(config_path)
        configure_logger(self.cfg.logging.level, self.cfg.logging.json, self.cfg.logging.dir)
        logger.info("Config loaded.")

        self.embeddings = build_embeddings(
            provider=self.cfg.embeddings.provider,
            model=self.cfg.embeddings.model,
            device=self.cfg.embeddings.device,
        )
        self.vs = ChromaHandler(
            persist_dir=self.cfg.vectorstore.persist_dir,
            collection=self.cfg.vectorstore.collection,
            embedding_function=self.embeddings,
        )
        self.llm = build_llm(
            provider=self.cfg.llm.provider,
            model=self.cfg.llm.model,
            temperature=self.cfg.llm.temperature,
            max_tokens=self.cfg.llm.max_tokens,
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True) if self.cfg.memory.enabled else None
        self._qa: Optional[RetrievalQA] = None

    def retriever(self):
        return self.vs.as_retriever(k=self.cfg.retriever.k, search_type=self.cfg.retriever.search_type)

    def chain(self) -> RetrievalQA:
        if self._qa is None:
            self._qa = RetrievalQA.from_chain_type(
                llm=self.llm,
                retriever=self.retriever(),
                chain_type="stuff",
                chain_type_kwargs={"prompt": DEFAULT_PROMPT},
                memory=self.memory,
                return_source_documents=True,
            )
        return self._qa

    def ingest(self, source_dir: Optional[str] = None, pattern: Optional[str] = None):
        source = Path(source_dir or self.cfg.data.source_dir)
        pat = pattern or self.cfg.data.glob_pattern
        docs = ingest_dir(
            source_dir=source,
            pattern=pat,
            allowed_ext=self.cfg.data.allowed_ext,
            chunk_size=self.cfg.data.chunk_size,
            chunk_overlap=self.cfg.data.chunk_overlap,
        )
        if docs:
            self.vs.add_documents(docs)
            logger.info(f"Ingested {len(docs)} chunks from {source}.")
        else:
            logger.warning("No documents found to ingest.")
        return len(docs)

    def ask(self, question: str) -> Dict[str, Any]:
        qa = self.chain()
        result = qa.invoke({"query": question})
        answer = result.get("result") or result.get("answer") or ""
        sources = []
        for doc in result.get("source_documents", []) or []:
            meta = getattr(doc, "metadata", {}) or {}
            src = meta.get("source") or meta.get("file_path") or "unknown"
            sources.append(src)
        return {"answer": answer, "sources": list(dict.fromkeys(sources))}

    def clear(self) -> bool:
        return self.vs.clear()

    def stats(self):
        return self.vs.stats()

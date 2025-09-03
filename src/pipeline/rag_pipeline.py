# src/pipeline/rag_pipeline.py
import os
from typing import Tuple, List

from loguru import logger
from dotenv import load_dotenv

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from src.config import load_config
from src.logger import configure
from src.db.chroma_handler import ChromaHandler
from src.ingestion.ingest import ingest_folder

load_dotenv()

DEFAULT_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a helpful assistant. Use ONLY the following context to answer the user.\n"
        "If the answer is not present, say you don't know.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    ),
)

class RAGPipeline:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = load_config(config_path)

        logcfg = self.config.get("logging", {})
        configure(
            log_dir=logcfg.get("dir", "./logs"),
            level=logcfg.get("level", "INFO"),
            json_logs=logcfg.get("json", False),
        )

        vscfg = self.config.get("vector_store", {})
        self.chroma = ChromaHandler(
            persist_directory=vscfg.get("persist_directory", "./.chroma"),
            embedding_model=vscfg.get("embedding_model", "sentence-transformers/all-MiniLM-L6-v2"),
        )
        self.top_k = int(vscfg.get("top_k", 4))

        self.prompt = DEFAULT_PROMPT

        # Memory
        memcfg = self.config.get("memory", {"enabled": True, "k": 5})
        self.memory = None
        if memcfg.get("enabled", True):
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                k=memcfg.get("k", 5),
                output_key="answer",   # 👈 Only log the answer
            )

        # LLM
        self.llm = self._build_llm()

        # Build chain
        self.retriever = self.chroma.as_retriever(k=self.top_k)
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            chain_type="stuff",
            combine_docs_chain_kwargs={"prompt": self.prompt},
            return_source_documents=True,
            output_key="answer",   # 👈 Added to fix ValueError
        )


    def _build_llm(self):
        llm_cfg = self.config.get("llm", {})
        provider = llm_cfg.get("provider", "groq").lower()
        model = llm_cfg.get("model")
        temperature = float(llm_cfg.get("temperature", 0.2))
        max_tokens = int(llm_cfg.get("max_tokens", 512))

        if provider == "groq":
            key = os.getenv("GROQ_API_KEY")
            if not key:
                raise RuntimeError("GROQ_API_KEY not set")
            return ChatGroq(
                api_key=key,
                model_name=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        elif provider == "openai":
            key = os.getenv("OPENAI_API_KEY")
            if not key:
                raise RuntimeError("OPENAI_API_KEY not set")
            return ChatOpenAI(
                api_key=key,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    # Public API

    def ingest_folder(self) -> int:
        datacfg = self.config.get("data", {})
        ingcfg = self.config.get("ingestion", {})
        count = ingest_folder(
            folder=datacfg.get("source_dir", "./data"),
            chroma_handler=self.chroma,
            allowed_ext=set(map(str.lower, datacfg.get("allowed_ext", [".pdf", ".docx", ".txt", ".md", ".json"]))),
            chunk_size=int(ingcfg.get("chunk_size", 1200)),
            chunk_overlap=int(ingcfg.get("chunk_overlap", 150)),
        )
        self.chroma.persist()
        return count

    def ask(self, question: str) -> Tuple[str, List]:
        """
        Returns (answer_text, source_documents)
        """
        res = self.chain.invoke({"question": question})
        answer = res.get("answer") or res.get("result") or ""
        sources = res.get("source_documents") or []
        return answer, sources

    def stats(self):
        return self.chroma.get_collection_info()

    def clear(self) -> bool:
        return self.chroma.clear()

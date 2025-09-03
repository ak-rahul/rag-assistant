from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src.utils.groq_client import GroqClient

class RAGPipeline:
    def __init__(self, config, logger):
        self.logger = logger
        self.config = config
        self.chroma_dir = config.get("vector_store.persist_directory")
        self.top_k = config.get("vector_store.top_k", 5)
        self.embedding_model = config.get("vector_store.embedding_model")
        self.retriever = self._init_vector_store()
        self.llm_client = GroqClient()
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="Use the following context to answer the question.\nContext: {context}\nQuestion: {question}\nAnswer:"
        )
        self.qa_chain = RetrievalQA(
            retriever=self.retriever,
            combine_documents_chain_kwargs={"prompt": self.prompt_template},
            return_source_documents=True
        )

    def _init_vector_store(self):
        embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        return Chroma(persist_directory=self.chroma_dir, embedding_function=embeddings).as_retriever(search_kwargs={"k": self.top_k})

    def add_documents(self, docs: list):
        from langchain.docstore.document import Document
        from langchain.vectorstores import Chroma
        embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        vectordb = Chroma(persist_directory=self.chroma_dir, embedding_function=embeddings)
        vectordb.add_documents([Document(page_content=d) for d in docs])
        vectordb.persist()
        self.logger.info(f"Added {len(docs)} documents to ChromaDB.")

    def query(self, question: str):
        result = self.qa_chain({"query": question})
        return result

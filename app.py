import streamlit as st
from src.utils.config_loader import ConfigLoader
from src.utils.log_manager import LogManager
from src.rag_pipeline import RAGPipeline
from src.ingestion.document_loader import DocumentLoader

config = ConfigLoader()
logger = LogManager(log_dir=config.get("logging.log_dir"))
doc_loader = DocumentLoader(config.get("ingestion.supported_formats"))
rag_pipeline = RAGPipeline(config, logger)

st.title("📚 RAG Document Assistant")

menu = ["Chat", "Ingest Document", "Stats"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Ingest Document":
    uploaded_files = st.file_uploader("Upload documents", accept_multiple_files=True)
    if st.button("Ingest"):
        docs = []
        for f in uploaded_files:
            text = doc_loader.load_document(f.name)
            docs.append(text)
        rag_pipeline.add_documents(docs)
        st.success(f"Ingested {len(docs)} documents!")

elif choice == "Chat":
    question = st.text_input("Ask a question:")
    if st.button("Submit"):
        result = rag_pipeline.query(question)
        st.write("**Answer:**", result.get("result"))
        st.write("**Sources:**", [doc.metadata for doc in result.get("source_documents", [])])

elif choice == "Stats":
    st.write("**Vector Store Directory:**", config.get("vector_store.persist_directory"))
    # Future: add real-time analytics

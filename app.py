# app.py
import os
import streamlit as st
from dotenv import load_dotenv

from src.pipeline.rag_pipeline import RAGPipeline

# Load environment variables
load_dotenv()

# Make sure ./data exists
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize session state
if "pipeline" not in st.session_state:
    st.session_state.pipeline = RAGPipeline()

st.set_page_config(page_title="RAG Assistant", layout="wide")
st.title("📚 RAG Assistant")

# Sidebar: Upload
st.sidebar.header("📂 Upload Documents")
uploaded_files = st.sidebar.file_uploader(
    "Upload one or more files",
    type=["pdf", "docx", "txt", "md", "json"],
    accept_multiple_files=True
)

if uploaded_files:
    for f in uploaded_files:
        file_path = os.path.join(DATA_DIR, f.name)
        with open(file_path, "wb") as out:
            out.write(f.read())
        st.sidebar.success(f"Saved {f.name} to {DATA_DIR}")

    # Ingest all files in ./data
    with st.spinner("🔄 Ingesting documents..."):
        count = st.session_state.pipeline.ingest_folder()
    st.sidebar.success(f"✅ Added {count} new chunks to Chroma")

# Chat interface
st.subheader("💬 Ask a Question")
query = st.text_input("Type your question here...")

if st.button("Submit") and query:
    with st.spinner("🤔 Thinking..."):
        answer, sources = st.session_state.pipeline.ask(query)

    st.markdown("### ✅ Answer")
    st.write(answer)

    if sources:
        st.markdown("### 📖 Sources")
        for s in sources:
            st.write(f"- {s.metadata.get('source', 'unknown')}")

# Sidebar: DB controls
st.sidebar.header("🗄️ Database Controls")

if st.sidebar.button("Show DB Stats"):
    stats = st.session_state.pipeline.stats()
    st.sidebar.json(stats)

if st.sidebar.button("Clear DB"):
    st.session_state.pipeline.clear()
    st.sidebar.success("🧹 Cleared Chroma DB")

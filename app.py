# app.py
import streamlit as st
from src.pipeline.rag_pipeline import RAGPipeline
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()
UI_API_KEY = os.getenv("UI_API_KEY", "")

if UI_API_KEY:
    st.sidebar.write("🔒 UI protected — enter API key")
    token = st.sidebar.text_input("API key", type="password")
    if token != UI_API_KEY:
        st.warning("Enter valid API key to continue")
        st.stop()

st.set_page_config(page_title="RAG Assistant", layout="wide")
st.title("RAG Document Assistant")

pipeline = RAGPipeline()

with st.sidebar:
    st.header("Controls")
    uploaded = st.file_uploader("Upload files (pdf/docx/txt/json)", accept_multiple_files=True)
    if st.button("Ingest Uploaded"):
        if not uploaded:
            st.warning("Upload at least one file")
        else:
            total = 0
            for f in uploaded:
                suffix = "." + f.name.split(".")[-1]
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                tmp.write(f.read())
                tmp.flush()
                total += pipeline.ingest(tmp.name)
            st.success(f"Ingested {total} chunks from uploaded files")
    if st.button("Clear DB"):
        if pipeline.clear():
            st.success("Cleared vector store")
        else:
            st.error("Failed to clear DB")
    st.markdown("---")
    st.write("DB stats:")
    st.json(pipeline.stats())

query = st.text_input("Ask a question:")
if st.button("Ask"):
    if query.strip():
        res = pipeline.query(query)
        context = res["context"]
        st.subheader("Retrieved Context")
        st.write(context[:4000])
        # Call LLM optionally
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            import requests
            cfg = pipeline.chroma  # pipeline.config usage avoided for brevity
            payload = {"prompt": f"Answer using context:\n\n{context}\n\nQuestion: {query}\nAnswer:", "temperature": 0.2, "max_tokens": 512}
            headers = {"Authorization": f"Bearer {groq_key}"}
            r = requests.post("https://api.groq.ai/v1/generate", json=payload, headers=headers, timeout=60)
            r.raise_for_status()
            out = r.json()
            answer = out.get("text") or out.get("output") or out
            st.subheader("Answer")
            st.write(answer)
        else:
            st.info("GROQ_API_KEY not set. Displaying retrieved context only.")

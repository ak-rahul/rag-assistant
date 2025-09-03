# app.py
import os
import streamlit as st
from dotenv import load_dotenv
from src.pipeline.rag_pipeline import RAGPipeline

load_dotenv()
UI_API_KEY = os.getenv("UI_API_KEY", "")

st.set_page_config(page_title="RAG Assistant", layout="wide")
st.title("📚 RAG Assistant")
st.caption("Ask questions to your custom knowledge base")

if UI_API_KEY:
    with st.sidebar:
        st.write("🔒 UI protected — enter API key")
        token = st.text_input("API key", type="password")
        if token != UI_API_KEY:
            st.warning("Enter a valid API key to continue.")
            st.stop()

if "pipeline" not in st.session_state:
    st.session_state.pipeline = RAGPipeline()
    st.session_state.history = []

query = st.chat_input("Ask a question...")
if query:
    with st.spinner("Thinking..."):
        answer, sources = st.session_state.pipeline.ask(query)
        st.session_state.history.append((query, answer, sources))

# render chat
for q, a, s in reversed(st.session_state.history):
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        st.write(a)
        if s:
            with st.expander("Sources"):
                for i, doc in enumerate(s, 1):
                    src = doc.metadata.get("source", "unknown")
                    st.write(f"{i}. {src}")

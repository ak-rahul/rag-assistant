
import streamlit as st
from pipeline import RAGPipeline

st.set_page_config(page_title="RAG Assistant", page_icon="🧠", layout="centered")
st.title("🧠 RAG Assistant (v1-style)")
st.caption("Ask questions about your local documents.")

if "pipeline" not in st.session_state:
    st.session_state.pipeline = RAGPipeline()

with st.form("ask_form", clear_on_submit=False):
    question = st.text_input("Question", placeholder="What is in these docs?")
    submitted = st.form_submit_button("Ask")
if submitted and question:
    res = st.session_state.pipeline.ask(question)
    st.markdown("### Answer")
    st.write(res["answer"])
    if res["sources"]:
        st.markdown("### Sources") 
        for s in res["sources"]:
            st.write("•", s)

with st.expander("Ingest Documents"):
    dir_ = st.text_input("Directory", value="./data")
    pattern = st.text_input("Glob", value="**/*.*")
    if st.button("Ingest"):
        n = st.session_state.pipeline.ingest(dir_, pattern)
        st.success(f"Ingested chunks: {n}")

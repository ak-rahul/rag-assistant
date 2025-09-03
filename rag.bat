@echo off
SET COMMAND=%1
SET ARG1=%2

IF "%COMMAND%"=="ingest" (
    echo 📥 Ingesting documents from %ARG1%
    python main.py ingest --path "%ARG1%"
) ELSE IF "%COMMAND%"=="query" (
    echo 💬 Querying: %ARG1%
    python main.py query "%ARG1%"
) ELSE IF "%COMMAND%"=="interactive" (
    echo 🖥️ Starting interactive CLI mode...
    python main.py interactive
) ELSE IF "%COMMAND%"=="web" (
    echo 🌐 Launching Streamlit Web UI...
    streamlit run app.py
) ELSE (
    echo Usage: rag.bat [ingest|query|interactive|web] [argument]
)

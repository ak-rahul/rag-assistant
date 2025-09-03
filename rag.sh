#!/bin/bash

# Ensure virtual environment is activated
if [ -d "venv" ]; then
    source venv/bin/activate
fi

COMMAND=$1
ARG1=$2

case $COMMAND in
    ingest)
        echo "📥 Ingesting documents from $ARG1..."
        python main.py ingest --path "$ARG1"
        ;;
    query)
        echo "💬 Querying: $ARG1"
        python main.py query "$ARG1"
        ;;
    interactive)
        echo "🖥️ Starting interactive CLI mode..."
        python main.py interactive
        ;;
    web)
        echo "🌐 Launching Streamlit Web UI..."
        streamlit run app.py
        ;;
    *)
        echo "Usage: ./rag.sh [ingest|query|interactive|web] [argument]"
        ;;
esac

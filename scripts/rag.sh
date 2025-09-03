#!/bin/bash
# optional: activate venv if present
if [ -d "venv" ]; then
    source venv/bin/activate
fi
cmd=$1
arg=$2
case "$cmd" in
  ingest) python cli.py ingest "$arg" ;;
  query) python cli.py query "$arg" ;;
  web) python cli.py web ;;
  stats) python cli.py stats ;;
  clear) python cli.py clear ;;
  *) echo "Usage: rag.sh [ingest|query|web|stats|clear]" ;;
esac

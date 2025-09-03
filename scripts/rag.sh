#!/usr/bin/env bash
set -e
case "$1" in
  ingest) python cli.py ingest ;;
  query) shift; python cli.py query "$@" ;;
  web) python cli.py web ;;
  stats) python cli.py stats ;;
  clear) python cli.py clear ;;
  serve) python cli.py serve ;;
  *)
    echo "Usage: rag.sh {ingest|query|web|stats|clear|serve}"
    exit 1
  ;;
esac

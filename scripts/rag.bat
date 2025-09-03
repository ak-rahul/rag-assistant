@echo off
set cmd=%1
set arg=%2
if "%cmd%"=="ingest" python cli.py ingest %arg%
if "%cmd%"=="query" python cli.py query %*
if "%cmd%"=="web" python cli.py web
if "%cmd%"=="stats" python cli.py stats
if "%cmd%"=="clear" python cli.py clear
if "%cmd%"=="serve" python cli.py serve

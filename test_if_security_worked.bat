@echo off
setlocal enabledelayedexpansion

REM Send 10 requests to the Flask application
for /l %%i in (1,1,10000) do (
    curl http://127.0.0.1:5000/
)

@echo off
setlocal
cd /d "%~dp0"
python tools\apply_sr039_final_consolidated.py || exit /b 1
python -m pytest

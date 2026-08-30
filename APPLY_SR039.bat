@echo off
setlocal
cd /d "%~dp0"
python tools\apply_sr039_release_gate.py || exit /b 1
python -m pytest

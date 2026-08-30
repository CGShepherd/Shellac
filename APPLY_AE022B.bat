@echo off
setlocal
cd /d "%~dp0"
python tools\apply_ae022b_routing_closure.py || exit /b 1
python -m pytest

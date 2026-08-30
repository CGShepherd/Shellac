@echo off
setlocal
cd /d "%~dp0"
python tools\apply_ae021c_population_closure.py || exit /b 1
python -m pytest

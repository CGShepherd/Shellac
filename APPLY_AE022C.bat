@echo off
setlocal
cd /d "%~dp0"
python tools\apply_ae022c_pin_crossing_closure.py || exit /b 1
python -m pytest

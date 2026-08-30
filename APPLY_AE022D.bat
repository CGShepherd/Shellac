@echo off
setlocal
cd /d "%~dp0"
python tools\apply_ae022d_exact_fix.py || exit /b 1
python tools\apply_ae022d_regression.py || exit /b 1
python tools\trace_sch101_nets.py
python -m pytest

@echo off
setlocal
cd /d "%~dp0"
python tools\apply_ae022e_named_net_converter.py || exit /b 1
python tools\apply_ae022e_regressions.py || exit /b 1
python tools\trace_sch101_nets.py || exit /b 1
python -m pytest

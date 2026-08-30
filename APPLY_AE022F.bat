@echo off
setlocal
cd /d "%~dp0"
python tools\apply_ae022f_symbol_contract.py || exit /b 1
python tools\apply_ae022f_tracer_cleanup.py || exit /b 1
python tools\trace_sch101_nets.py || exit /b 1
python -m pytest

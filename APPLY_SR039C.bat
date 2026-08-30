@echo off
setlocal
cd /d "%~dp0"
python tools\apply_sr039c_decision_test.py || exit /b 1
python -m pytest

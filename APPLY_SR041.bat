@echo off
setlocal
cd /d "%~dp0"
python -m pytest || exit /b 1
python tools\report_sr041.py || exit /b 1

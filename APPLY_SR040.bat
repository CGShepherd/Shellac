@echo off
setlocal
cd /d "%~dp0"
python tools\apply_sr040.py || exit /b 1
python -m pytest || exit /b 1
python tools\report_sr040.py || exit /b 1

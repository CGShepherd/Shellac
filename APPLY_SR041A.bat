@echo off
setlocal
cd /d "%~dp0"
python tools\apply_sr041a_mounting_clearance.py || exit /b 1
python -m pytest || exit /b 1
python -m tools.report_sr041 || exit /b 1

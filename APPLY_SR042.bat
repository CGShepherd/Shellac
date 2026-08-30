@echo off
setlocal
cd /d "%~dp0"
python -m pytest || exit /b 1
python -m tools.report_sr042 || exit /b 1

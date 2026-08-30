@echo off
setlocal
cd /d "%~dp0"
python tools\apply_dr038_definitive_fix.py || exit /b 1
python tools\check_sch101_after_fix.py || exit /b 1
python -m pytest

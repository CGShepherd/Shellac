@echo off
setlocal
cd /d "%~dp0"
python tools\apply_dr038_full_migration.py || exit /b 1
python -m pytest

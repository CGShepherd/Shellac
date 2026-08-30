@echo off
setlocal
cd /d "%~dp0"
python tools\apply_sr039a_no_pyyaml.py || exit /b 1
python -m pytest

@echo off
python tools\repair_ae021_import.py || exit /b 1
python -m pytest

@echo off
python tools\apply_dr039_full_closure.py || exit /b 1
python -m pytest

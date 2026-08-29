@echo off
setlocal
cd /d "%~dp0"
python RESTORE_SCH103_BASELINE.py || exit /b 1
python REPAIR_SIGNAL_CHAIN.py || exit /b 1
echo AE-016B staging repair applied.
echo Now run: python -m pytest
endlocal

@echo off
setlocal
cd /d "%~dp0"
python APPLY_DECISION_INDEX_RECONCILIATION.py || exit /b 1
python tools\audit_current_decision_index.py || exit /b 1
echo AE-023 reconciliation applied. Now run: python -m pytest
endlocal

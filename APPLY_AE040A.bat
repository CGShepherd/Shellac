@echo off
setlocal
echo ============================================================
echo AE-040A Production Integrity Reconciliation
echo ============================================================
if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Run from Shellac repository root.
  exit /b 1
)
".venv\Scripts\python.exe" tools\apply_ae040a_production_integrity_reconciliation.py
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m pytest tests\test_production_integrity_audit.py -v
if errorlevel 1 exit /b 1
echo.
echo AE-040A targeted tests passed.
endlocal

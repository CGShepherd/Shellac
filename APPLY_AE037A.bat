@echo off
setlocal
if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Run from Shellac repository root.
  exit /b 1
)
".venv\Scripts\python.exe" tools\apply_ae037a_placement_reconciliation.py
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m pytest tests\test_ae037a_placement_reconciliation.py tests\test_cluster_placement_baseline.py tests\test_preliminary_placement.py tests\test_real_footprint_audit.py -v
if errorlevel 1 exit /b 1
echo AE-037A targeted reconciliation tests passed.
endlocal

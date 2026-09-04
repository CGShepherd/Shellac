@echo off
setlocal
if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Run from Shellac repository root.
  exit /b 1
)
".venv\Scripts\python.exe" tools\apply_ae036b_native_pcb_protection.py
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m pytest tests\test_clean_output.py -v
if errorlevel 1 exit /b 1
echo AE-036B completed successfully.
endlocal

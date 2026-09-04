@echo off
setlocal
echo ============================================================
echo AE-039B Physical Op-Amp Population Migration
echo ============================================================
if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Run from Shellac repository root.
  exit /b 1
)
".venv\Scripts\python.exe" tools\apply_ae039b_physical_opamp_population.py
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m pytest ^
 tests\test_ae039b_physical_opamp_population.py ^
 tests\test_footprint_contract.py ^
 tests\test_cluster_placement_baseline.py ^
 tests\test_preliminary_placement.py ^
 tests\test_real_footprint_audit.py -v
if errorlevel 1 exit /b 1
echo AE-039B targeted tests passed.
endlocal

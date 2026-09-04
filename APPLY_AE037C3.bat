@echo off
setlocal
echo ============================================================
echo AE-037C3 Deterministic Mounting Reconciliation
echo ============================================================
if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Run from Shellac repository root.
  exit /b 1
)

".venv\Scripts\python.exe" -u tools\apply_ae037c3_deterministic_mounting_reconciliation.py
if errorlevel 1 exit /b 1

echo.
echo Checking SR-041 directly...
".venv\Scripts\python.exe" -c "from generator.layout.sr041_routing_release import build_sr041_routing_release; g=build_sr041_routing_release(); print(g.status); print('collisions=',g.mounting_collision_count); print(g.release_checks[-2])"
if errorlevel 1 exit /b 1

echo.
echo Running targeted placement/routing tests...
".venv\Scripts\python.exe" -m pytest ^
 tests\test_detailed_placement_readiness.py ^
 tests\test_kicad_native_pipeline.py ^
 tests\test_sr041_routing_release.py ^
 tests\test_sr042_native_routing_bootstrap.py ^
 tests\test_preliminary_placement.py ^
 tests\test_ae037a_placement_reconciliation.py ^
 tests\test_real_footprint_audit.py -v
if errorlevel 1 exit /b 1

echo.
echo AE-037C3 targeted tests passed.
endlocal

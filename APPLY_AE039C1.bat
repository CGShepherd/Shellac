@echo off
setlocal
echo ============================================================
echo AE-039C1 Buffer Synthetic-0VA Cleanup
echo ============================================================
if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Run from Shellac repository root.
  exit /b 1
)

".venv\Scripts\python.exe" tools\apply_ae039c1_buffer_0va_cleanup.py
if errorlevel 1 exit /b 1

".venv\Scripts\python.exe" -m pytest ^
 tests\test_ae039c1_buffer_0va_cleanup.py ^
 tests\test_ae039c_real_kicad_opamp_units.py ^
 tests\test_pin_connectivity.py ^
 tests\test_kicad_writer_instances.py ^
 tests\test_ae039b_physical_opamp_population.py ^
 tests\test_opamp_package_allocation.py -v
if errorlevel 1 exit /b 1

echo.
echo AE-039C1 targeted tests passed.
endlocal

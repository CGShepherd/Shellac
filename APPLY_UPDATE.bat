@echo off
setlocal
cd /d "%~dp0"

echo Applying DR-037 rollback package to current repository...
echo.
echo IMPORTANT: run this batch file from the extracted package after copying
echo the package contents into the Shellac repository root.
echo.

if not exist "generator\model" (
  echo ERROR: generator\model not found. Extract the ZIP at the Shellac repository root.
  exit /b 1
)

del /q "generator\model\riaa_optional_pole.py" 2>nul
del /q "generator\model\riaa_optional_pole_realisation.py" 2>nul
del /q "generator\model\riaa_integration_audit.py" 2>nul
del /q "tests\test_riaa_optional_pole.py" 2>nul
del /q "tests\test_riaa_optional_pole_realisation.py" 2>nul
del /q "tests\test_riaa_integration_audit.py" 2>nul

echo Superseded optional-RIAA model and test files removed.
echo Run: python -m pytest
endlocal

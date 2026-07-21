@echo off
setlocal

echo.
echo ============================================================
echo  Project Shellac Build
echo ============================================================
echo.

if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found.
    echo Run this batch file from the Project Shellac repo root.
    exit /b 1
)

if not exist "generator" (
    echo ERROR: generator folder not found.
    echo Run this batch file from the Project Shellac repo root.
    exit /b 1
)

if not exist "scripts" (
    echo ERROR: scripts folder not found.
    echo Run this batch file from the Project Shellac repo root.
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        exit /b 1
    )
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
    exit /b 1
)

echo.
echo Python interpreter:
where python
python --version

echo.
echo Installing/updating dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Dependency installation failed.
    exit /b 1
)

echo.
echo Running tests...
python -m pytest
if errorlevel 1 (
    echo ERROR: Tests failed. Build stopped.
    exit /b 1
)

echo.
echo Generating KiCad project...
python scripts\build_shellac_from_model.py
if errorlevel 1 (
    echo ERROR: KiCad generation failed.
    exit /b 1
)

echo.
echo ============================================================
echo  Build complete.
echo ============================================================
echo.
echo Open this file in KiCad:
echo   out\kicad\ProjectShellac.kicad_pro
echo.
echo Generated output folder:
dir out\kicad
echo.

endlocal

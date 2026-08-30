@echo off
setlocal
cd /d "%~dp0"
python -m pytest || exit /b 1
python -m tools.apply_sr043_native_board || exit /b 1
echo.
echo Native placement and mechanical geometry applied.
echo Open out\kicad\ProjectShellac.kicad_pcb in KiCad and configure FOUR copper layers.
echo Then save and run VALIDATE_SR043.bat.

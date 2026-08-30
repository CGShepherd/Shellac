@echo off
setlocal
cd /d "%~dp0"
python -m generator.layout.sr043_native_board_audit || exit /b 1
set "KICADCLI="
where kicad-cli >nul 2>nul
if not errorlevel 1 set "KICADCLI=kicad-cli"
if not defined KICADCLI if exist "C:\Program Files\KiCad\9.0\bin\kicad-cli.exe" set "KICADCLI=C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"
if not defined KICADCLI (echo ERROR: KiCad CLI not found.& exit /b 1)
"%KICADCLI%" pcb drc --exit-code-violations --output out\kicad\ProjectShellac_DRC.rpt out\kicad\ProjectShellac.kicad_pcb
if errorlevel 1 (type out\kicad\ProjectShellac_DRC.rpt & exit /b 1)
type out\kicad\ProjectShellac_DRC.rpt

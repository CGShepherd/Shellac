@echo off
setlocal
cd /d "%~dp0"

call build_shellac.bat
if errorlevel 1 exit /b 1

set "KICADCLI="
where kicad-cli >nul 2>nul
if not errorlevel 1 set "KICADCLI=kicad-cli"
if not defined KICADCLI if exist "C:\Program Files\KiCad\9.0\bin\kicad-cli.exe" set "KICADCLI=C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

if not defined KICADCLI (
  echo ERROR: KiCad CLI not found in PATH or standard KiCad 9 installation.
  exit /b 1
)

"%KICADCLI%" sch erc --severity-all --exit-code-violations --output out\kicad\ProjectShellac_ERC.rpt out\kicad\ProjectShellac.kicad_sch
if errorlevel 1 (
  type out\kicad\ProjectShellac_ERC.rpt
  exit /b 1
)

type out\kicad\ProjectShellac_ERC.rpt
python -c "from generator.layout.schematic_release_gate import build_schematic_to_layout_release_gate; import json; print(json.dumps(build_schematic_to_layout_release_gate().to_dict(), indent=2))"

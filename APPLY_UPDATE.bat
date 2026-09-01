@echo off
setlocal
cd /d "%~dp0"
echo AE-025B test-only repair is applied by file extraction.
echo Run:
echo   python tools\ae024_design_record_audit.py
echo   python -m pytest
endlocal

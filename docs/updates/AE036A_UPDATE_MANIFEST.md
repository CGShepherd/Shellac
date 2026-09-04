# AE-036A update manifest

Run from repository root:

`python tools/apply_ae036a_native_pcb_protection.py`

Then:

`python -m pytest tests/test_clean_output.py -v`

`python -m pytest`

High-value local verification:
1. calculate SHA256 of `out/kicad/ProjectShellac.kicad_pcb`;
2. run `build_shellac.bat`;
3. calculate SHA256 again and confirm it is unchanged.

No manual source editing is required.

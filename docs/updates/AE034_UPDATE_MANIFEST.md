# AE-034 update manifest

Add the package files. Then replace the current header/import section of `generator/layout/sr043_native_board_audit.py` with `generator/layout/sr043_native_board_audit.py.replacement_header.txt`, removing duplicate imports.

Run:
1. `python generator/layout/sr043_native_board_audit.py`
2. `python -m generator.layout.sr043_native_board_audit`
3. `python tools/ae034_native_copper_preflight.py`
4. `python -m pytest`

Commit the generated `docs/design_pack/AE-034_Generated_Native_Copper_Preflight.json` with the package.

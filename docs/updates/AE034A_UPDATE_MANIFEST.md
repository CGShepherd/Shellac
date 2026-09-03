# AE-034A update manifest

This package replaces the previous manual SR-043 header-edit instruction.

Run from the Shellac repository root:

`python tools/apply_ae034a_sr043_repair.py`

Then verify:

`python generator/layout/sr043_native_board_audit.py`

`python -m generator.layout.sr043_native_board_audit`

`python tools/ae034_native_copper_preflight.py`

`python -m pytest`

No manual source editing is required.

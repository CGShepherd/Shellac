# AE-039A update manifest

Adds package-allocation authority only.

Run:
`python -m pytest tests/test_opamp_package_allocation.py tests/test_opamp_package_audit.py -v`

Then:
`python -m pytest`

No existing generator, schematic, BOM, placement or PCB file is changed by
AE-039A. AE-039B will perform the atomic physical-CAD migration.

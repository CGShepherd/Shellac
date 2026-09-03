# AE-029 update manifest

Adds:
- generator/model/production_acceptance.py
- tests/test_production_acceptance.py
- docs/design_pack/AE-029_Production_Commissioning_and_Acceptance_Closure_Rev_A0.md
- docs/maintenance/Prototype_Commissioning_Acceptance_Matrix_Rev_A0.md
- docs/updates/AE029_UPDATE_MANIFEST.md

No live circuit, BOM, CAD, footprint or panel geometry changes.

Run:
`python -m pytest`

AE-029 is intended to close analytical questions and define the first-hardware
measurement programme. Provisional physical limits should only become FROZEN
production acceptance values after representative prototype evidence exists.

# AE-024 update manifest

Base GitHub commit inspected:
`dce5c0ec36e12f979338d8c46106c44a79c7a023`

Adds only:
- tools/ae024_design_record_audit.py
- tests/test_ae024_design_record_audit.py
- docs/design_pack/AE-024_Project_Wide_Design_Record_Reconciliation_Audit_Rev_A0.md
- docs/updates/AE024_UPDATE_MANIFEST.md

No active circuit, CAD, BOM, decision index, or README is modified.

Run:
`python tools/ae024_design_record_audit.py`
`python -m pytest`

The generated audit should also be committed once reviewed:
`docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md`

AE-023 should be validated/committed first if it is currently present only in
the local working tree.

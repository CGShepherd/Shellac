# AE-036 update manifest

Read-only production-integrity audit.

Adds:
- docs/design_pack/AE-036_Repository_Wide_Production_Integrity_Audit_Rev_A0.md
- generator/model/production_integrity_audit.py
- tests/test_production_integrity_audit.py
- docs/updates/AE036_UPDATE_MANIFEST.md

No circuit, PCB, BOM or mechanical geometry is changed by AE-036.

Run:
`python -m pytest`

AE-036 establishes a routing hold until F01/F02/F03 are closed.

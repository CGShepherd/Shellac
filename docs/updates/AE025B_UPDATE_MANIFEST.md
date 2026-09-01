# AE-025B update manifest

Apply over the current uncommitted AE-025 + AE-025A working tree.

Replaces only:
- tests/test_ae025_authority_reconciliation.py

Adds:
- docs/design_pack/AE-025B_Test_Fixture_Repair_Rev_A0.md
- docs/updates/AE025B_UPDATE_MANIFEST.md

No production/configuration files are changed.

Run:
`python tools/ae024_design_record_audit.py`
`python -m pytest`

Expected:
- Vocabulary findings: 0
- Potential status contradictions: 0
- Full test suite passes

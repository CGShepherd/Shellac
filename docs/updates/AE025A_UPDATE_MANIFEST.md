# AE-025A update manifest

Apply over the current uncommitted AE-025 working tree.

Replaces:
- config/decisions/decision_status.yaml

Adds:
- APPLY_AE025A_INDEX_REPAIR.py
- tests/test_ae025a_regression_repair.py
- docs/design_pack/AE-025A_Authority_Reconciliation_Regression_Repair_Rev_A0.md
- docs/updates/AE025A_UPDATE_MANIFEST.md

Run:
`APPLY_UPDATE.bat`
`python tools/ae024_design_record_audit.py`
`python -m pytest`

Expected:
- Vocabulary findings: 0
- Potential status contradictions: 0
- Full test suite passes

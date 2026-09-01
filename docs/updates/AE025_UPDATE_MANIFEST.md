# AE-025 update manifest

Base: develop `47a5fcabfef4239fcfe78bf97901dce75b4e7301`

Replaces:
- README.md
- config/decisions/decision_status.yaml
- docs/knowledge/DESIGN_PACK_INDEX.md
- docs/maintenance/MAINTENANCE_GUIDE_SKELETON.md

Adds:
- config/decisions/document_authority.yaml
- tests/test_ae025_authority_reconciliation.py
- docs/design_pack/AE-025_Current_Authority_and_Design_Pack_Reconciliation_Rev_A0.md

Patches:
- config/decisions/current_decision_index.yaml
- tools/ae024_design_record_audit.py

Run:
APPLY_UPDATE.bat
python tools/ae024_design_record_audit.py
python -m pytest

Do not commit unless tests pass and the regenerated audit has no unexpected
current-authority contradictions.

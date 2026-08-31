# AE-023 update manifest

Base commit: `dce5c0ec36e12f979338d8c46106c44a79c7a023`

Adds:
- generator/model/production_cmrr.py
- generator/model/production_signal_chain_closure.py
- tests/test_production_signal_chain_closure.py
- tools/audit_current_decision_index.py
- tests/test_decision_index_status_audit.py
- docs/AE-023_Production_Signal_Chain_Assurance_Closure_Rev_A0.md
- docs/maintenance/Signal_Chain_Commissioning_and_Maintenance_Baseline_Rev_A0.md
- docs/updates/AE023_UPDATE_MANIFEST.md

Patches:
- config/decisions/current_decision_index.yaml

Apply:
`python APPLY_DECISION_INDEX_RECONCILIATION.py`
`python tools/audit_current_decision_index.py`
`python -m pytest`

Do not commit unless the suite is clean.

Suggested commit:
`git add -A`
`git commit -m "analysis(signal-chain): close production assurance baseline"`
`git push`

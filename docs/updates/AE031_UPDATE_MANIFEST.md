# AE-031 update manifest

Apply over the current all-green AE-030/030A/030B working tree.

Replaces:
- config/bom/shellac_cost_ledger.yaml
- generator/model/bom_cost.py
- tools/ae030a_bom_cost_audit.py

Adds:
- generator/model/prerouting_readiness.py
- tools/ae031_prerouting_control_audit.py
- tests/test_ae031_prerouting_cost.py
- docs/design_pack/AE-031_PreRouting_Decoupling_and_Verified_Cost_Baseline_Rev_A0.md
- docs/updates/AE031_UPDATE_MANIFEST.md

Run:
1. python tools/ae030a_bom_cost_audit.py
2. python tools/ae031_prerouting_control_audit.py
3. python -m pytest

Expected cost dashboard:
- design subtotal £233.67 ex VAT
- 4/5 ledger lines priced
- 80.0% line coverage

This is line coverage of the current high-level cost ledger, not 80% of the
eventual component-level BOM.

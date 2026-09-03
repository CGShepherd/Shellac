# AE-030B update manifest

Apply over the current AE-030 / AE-030A working tree.

Replaces:
- requirements.txt

Adds:
- tests/test_tooling_dependencies.py
- docs/design_pack/AE-030B_Tooling_Dependency_Baseline_Repair_Rev_A0.md
- docs/updates/AE030B_UPDATE_MANIFEST.md

Run:
1. `python -m pip install -r requirements.txt`
2. `python tools/ae030_production_readiness_audit.py`
3. `python tools/ae030a_bom_cost_audit.py`
4. `python -m pytest`

Expected PyYAML version: 6.0.3

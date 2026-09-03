# AE-030A update manifest

Add:
- config/bom/shellac_cost_ledger.yaml
- generator/model/bom_cost.py
- tools/ae030a_bom_cost_audit.py
- tests/test_bom_cost.py
- docs/design_pack/AE-030A_Tooling_Repair_and_Running_BOM_Cost_Rev_A0.md
- docs/updates/AE030A_UPDATE_MANIFEST.md

Also apply:
- tools/ae030_production_readiness_audit.py.patch

Then run:
1. `python tools/ae030_production_readiness_audit.py`
2. `python -m tools.ae030_production_readiness_audit`
3. `python tools/ae030a_bom_cost_audit.py`
4. `python -m pytest`

Generated cost report:
- docs/procurement/Shellac_Running_BOM_Cost.md

Commit the generated AE-030 and BOM-cost reports with the package.

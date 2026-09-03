# AE-032 update manifest

Adds:
- generator/layout/production_routing_contract.py
- tests/test_production_routing_contract.py
- docs/design_pack/AE-032_Four_Layer_Native_Routing_Preparation_Rev_A0.md
- docs/updates/AE032_UPDATE_MANIFEST.md

No native KiCad board is modified by AE-032.

Run:
`python -m pytest`

After this package is green, the next phase may modify the native board layer
stack and routing setup while preserving the explicit rotary hold regions.

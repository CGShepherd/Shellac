# AE-027 update manifest

Adds analysis/procurement gate only:
- generator/model/rotary_switch_procurement_gate.py
- tests/test_rotary_switch_procurement_gate.py
- docs/design_pack/AE-027_Lorlin_PT_Exact_Procurement_Gate_Rev_A0.md
- docs/procurement/Lorlin_PT_Exact_Configuration_Request_Rev_A0.md
- docs/updates/AE027_UPDATE_MANIFEST.md

No BOM, PCB, footprint or panel geometry changes.

Run:
`python -m pytest`

Do not perform the switch BOM ECO until Lorlin confirms exact gold-contact MPNs
and drawings.

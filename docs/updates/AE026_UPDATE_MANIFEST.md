# AE-026 update manifest

Adds analysis/contracts only:
- generator/model/rotary_switch_platform.py
- tests/test_rotary_switch_platform.py
- docs/design_pack/AE-026_Lorlin_PT_Rotary_Platform_Downselect_Rev_A0.md
- docs/procurement/Lorlin_PT_Shellac_RFQ_Rev_A0.md
- docs/updates/AE026_UPDATE_MANIFEST.md

No live BOM, PCB footprint or panel geometry is changed yet.

Run:
`python -m pytest`

Only after exact Lorlin order codes and sample geometry are verified should the
Grayhill BOM entries be replaced and PCB/panel mechanics migrated.

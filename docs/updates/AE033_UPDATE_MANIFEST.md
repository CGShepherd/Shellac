# AE-033 update manifest

Adds native four-layer configuration tooling and tests.

Run from repository root:
1. `python tools/apply_ae033_four_layer.py`
2. `python tools/ae033_native_four_layer_audit.py`
3. `python generator/layout/sr043_native_board_audit.py`
4. `python -m pytest`

Expected: F.Cu/In1.Cu/In2.Cu/B.Cu present, SR-043 routing-ready true, board still unrouted.

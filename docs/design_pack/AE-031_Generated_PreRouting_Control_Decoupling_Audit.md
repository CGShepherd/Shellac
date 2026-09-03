# AE-031 Generated Pre-Routing / Control-Decoupling Audit

- live Grayhill-reference files: **6**
- routing rules independent of rotary geometry: **8**
- routing rules gated by rotary geometry: **2**

## Live Grayhill references

- `config/bom/shellac_bom.yaml`
- `config/procurement/sourcing_snapshot_2026-08-24.yaml`
- `generator/mechanical/control_hardware.py`
- `generator/mechanical/top_cover_stack.py`
- `generator/model/controls.py`
- `generator/model/production_readiness.py`

## Pre-routing rules

| ID | Requirement | Rotary-geometry dependent? |
|---|---|---|
| LAYER-COUNT | Four copper layers: F.Cu / In1.Cu / In2.Cu / B.Cu | NO |
| IN1-0VA | In1.Cu reserved as substantially continuous 0VA reference plane | NO |
| IN2-POWER | In2.Cu used for controlled power distribution / rail spine | NO |
| INPUT-SYMMETRY | SCH101 differential input/RF paths routed as a symmetric matched pair | NO |
| LT5400-LOCAL | LT5400 ratio-network connections remain short and local; no autorouting | NO |
| EQ-LOCAL | EQ timing components and selector nets kept local and away from output/rail switching loops | YES |
| OUTPUT-BALANCE | THAT1646 balanced-output legs and return paths kept symmetric | NO |
| NO-PLANE-SPLIT | No high-impedance or precision analogue route crosses a 0VA-plane discontinuity | NO |
| DECOUPLING | Every active device decoupled to the local reference with minimum loop area | NO |
| ROTARY-KEEP-OUT | Final rotary footprints/keep-outs remain gated by AE-027/AE-028 | YES |

## Disposition

Proceed now with all geometry-independent four-layer routing preparation.
Do not freeze EQ-selector routing endpoints, rotary footprints, keep-outs or top-panel machining until AE-027/AE-028 closes.
Historical Grayhill evidence may remain; current BOM/mechanical authority must migrate atomically during the later control-hardware ECO.

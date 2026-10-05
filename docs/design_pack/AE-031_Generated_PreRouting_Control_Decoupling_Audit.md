# AE-031 Generated Pre-Routing / Control-Geometry Audit

**Current reconciliation:** AE-076D

- unexpected live Grayhill-reference files: **0**
- routing rules independent of control geometry: **9**
- routing rules gated by control geometry: **2**

## Unexpected live Grayhill references

- None. Historical/provenance references are excluded by explicit allow-list.

## Pre-routing rules

| ID | Requirement | Control-geometry dependent? |
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
| CONTROL-GEOMETRY | Exact NKK/C&K B.Cu footprints, pin/pad orientation, keep-outs, upper-cover apertures and six-support service-module stack remain gated by current AE071-B03 | YES |
| PERSONALITY-LOCAL | Future H120/H220 per-channel personality sockets remain local to differential load nodes with short symmetric shunt geometry; exact interface parasitics remain RUN10-open | NO |

## Disposition

Analysis and non-binding placement preparation may continue.
Do not freeze control routing endpoints, exact B.Cu control footprints/keep-outs, top-cover apertures or the six-support stack until current AE071-B03 closes.
This audit does not grant routing authority; config/release/ae071_prerouting_hold.yaml remains the current fail-closed release authority.

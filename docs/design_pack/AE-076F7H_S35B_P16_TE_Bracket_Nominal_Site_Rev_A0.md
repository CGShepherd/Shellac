# S35B-P16 — TE matrix bracket nominal support-site qualification

**Classification:** READ-ONLY NOMINAL SITING PASS / SELECTED-NEXT DEVELOPMENT / NOT FOR FABRICATION.
**Date of checkpoint:** 23 November 2026.
**Pinned source `develop`:** `33494f18b610571a2ed3cabea402a306c8781aeb`.
**Primary evidence:** P16 report `31E2878CDE5CE70C2AA6C65C6A693F7D8753785DB8AF2BDC84C5A5B83287DBE1` (SHA-256). P16 manifest `8230C1DE6CA3279ECA261FCAD6C47D50846159E526F64EC8EF0CF350E7883FA3` (SHA-256).

## Design-site disposition

The TE MRJE3404 electrical selection and P14 physical static mapping stay unchanged. The 1.5 mm three-pillar aluminium spider remains the selected-next bracket architecture. The following positions are **development coordinates only** (KiCad XY, millimetres):

| Site | X | Y | Status |
|---|---:|---:|---|
| TE shaft | 130.000 | 118.000 | Selected-next datum, not native migrated |
| MHTE1 | 145.343 | 149.458 | Unchanged, nominal site pass |
| MHTE2 | 91.085 | 125.059 | Revised from F4Z, nominal site pass |
| MHTE3 | 149.572 | 88.984 | Unchanged, nominal site pass with thin DFM margin |

A valid FreeCAD one-solid 1.5 mm plate with three nominal 8 mm-wide arms and 12 mm lands was generated. The TE axis is inside the support triangle. No nominal Metcase intersection was found for the plate, posts, or proposed shadow PCB using the historical conditional enclosure registration. These are *nominal* geometric witnesses, not finished assembly or tolerance qualification.

| Site | Pad-to-Ø10 mm void gap (mm) | Courtyard-to-Ø8 mm passage gap (mm) |
|---|---:|---:|
| MHTE1 | 6.592881 | 7.369216 |
| MHTE2 | 2.549380 | 2.765000 |
| MHTE3 | 1.664993 | 2.371501 |

P16 screened ±0.25 mm XY around **MHTE2 only** (nine samples): minimum pad gap 2.263783 mm, minimum courtyard gap 2.515000 mm. This does not establish fabricated tolerance margins for any post. In particular, MHTE3 exceeds the provisional 1.5 mm pad-gap criterion by just 0.164993 mm; do not claim a manufacturing pass.

The old MHTE2 position failed and the new one passed, without moving existing PCB components. This closes the *nominal candidate post-site selection* only, not its physical installation or final DFM acceptance.

## Unresolved mechanical authority

- The 108.392536 mm³ TE/plate intersection is with the source STEP's **fused retainer hardware**, not demonstrated bare-switch collision or permissible interference.
- Selected-next PCB 220×148×1.6 mm and carrier assembly have not been implemented; current board 220×140 mm. Actual copper zones, control pads and native 4-layer DRC are not covered by this screen.
- TE exact anti-rotation double-D machining, clamp/bearing/washer, screws and heads, load/torque, tolerances and relative hardware disassembly remain unqualified.
- Seven installed native switches and H801/H802/H901 mated bodies/harness, Metcase cover apertures and service insertion remain unqualified.
- Current AE-076B upper-cover PCB-support authority remains live, notwithstanding the selected-next lower-G1 carrier. This record is **not** a mechanical-authority supersession.
- All four release gates remain false: `final_routing`, `layout_freeze`, `bom_freeze`, `manufacturing_release`.

**Next:** one bounded, manufacturer-numbered TE 15-pad B.Cu anti-mirror contract, followed by the fully populated seven-control MCAD. No additional general bracket-site sweep is authorised by this evidence alone.

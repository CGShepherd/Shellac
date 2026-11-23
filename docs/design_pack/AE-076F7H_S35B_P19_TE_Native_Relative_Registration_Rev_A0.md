# AE-076F7H — S35B-P19 TE native KiCad/STEP relative-registration checkpoint — Rev A0

**Date:** 23 November 2026.
**Status:** USER-EXECUTED NATIVE RELATIVE 15-PAD REGISTRATION PASS / ABSOLUTE MOUNTING ANGLE OPEN / **NOT FOR FABRICATION**.
**Parent governed `develop`:** `aee870b668144ea28df21399607fe6bc4ed95ed1` (P17/P18 merge, PR #12).
**Component:** TE Connectivity MRJE3404, manufacturer 1825537-3; 3P4T; customer drawing Rev A3, configuration 3-4.

## Accepted evidence and precise limits

- The user ran the P19 read-only qualification on Windows. Native **FreeCAD 1.1.4** loaded the authenticated TE OEM STEP as one valid fused solid and independently located the **15 actual terminal-tip centres**. The maximum reported difference from the source-numbered candidate coordinate sites was **0.000006 mm**. This proves relative tip-centre/footprint position alignment, NOT independent terminal labels or finished manufactured part tolerances.
- Native FreeCAD independently detected two opposite nominal bushing flat planes at local **Y = -2.54 mm** and **Y = +2.54 mm** (5.08 mm across flats). The bushing/flat geometry is identified in STEP coordinates, but its selected final angle relative to the G1 carrier, PCB B.Cu, cut-out and cover is **not yet qualified**.
- Native **KiCad pcbnew 10.0.7** imported the 15 uniquely labelled through-hole pads, completed an isolated shadow-PCB save/load roundtrip and exercised the actual native B.Cu flip; the tested flip reflected X. This verifies the software transform in the isolated candidate, **not** the final real-world mounting side or component rotation.
- P19 retained **47** mirror/rotation negative controls. Best incorrect transform and 180-degree wrong candidate each match **14/15** hole centres, not 15. Historical P14 user-reported switch-detent sequence and P17 drawing-derived pole labels are unchanged; CAD tip-centre matching is not an independent electrical-terminal labelling measurement.
- The tested analytical footprint origin **(130,118) mm**, zero rotation, F.Cu/B.Cu viewing transform and drawing-derived net assignments remain **candidate only**. No registered installation of the TE model with the full three-pillar frame, real motherboard, lid or all seven controls has been performed.

## Evidence and source hashes (SHA-256)

- `Shellac_Engineering_Staging/reports/S35B_P19_TE_NATIVE_STEP_KICAD_REGISTRATION/P19_REPORT.json`: `A49815B8808DC946569D2D65E41A4FD272CABC9CBE93A5A4FCF56F464F3A3005`.
- P19 `P19_MANIFEST.json` lists individually authenticated native worker, result and shadow-PCB hashes. The original temporary shadow board was retained under the P19 report directory; its purpose is evidence, not a production board.
- Native input TE original STEP: `24E75B2DD8187E63EE200F278DD84016C8E705525980846CD78B37AA4FDEB3D9`; TE STEP archive: `F0E56322F0737FB334D19C33B3BFD6E056ECEFFBAAC3556D76B330CE0732F25C`; Rev A3 manufacturer PDF: `F4319D2A91999BB09C6C9F036AB5E9585ED62F552CD2682D82F9AF2BFD90EA6B`.
- P17 report `B6038C73605AEF594D437B1A865339CC555F9FFA91B056AE1091F01871A7884C`; P18 report `ECBF48E3C6E52167505111A44C9167166C2BE6169EDEB68AE686D5D884FD4C0A`; P18 isolated KiCad 15-pad candidate `9F2CC841DE1A2692A9C461B72E5B1F9A55199A3C690BCD21078D5CCBED8913B3`.

## Unresolved qualifications and release holds

- Absolute placement: map the **STEP's double-D bushing-flat axis** to the proposed actual bracket/cover apertures and PCB side/angle, using a common physical datum; distinguish native F.Cu view and physical solder-side B.Cu assembly view. No new continuity measurement is required unless contradictory evidence arises.
- Exact manufactured lead insertion, finished plated-hole sizes, copper annular ring, mask bridges, four-layer DRC, tolerance stack and mechanical strength remain open. The previous P18 Ø1.42 mm copper/Ø0.762 mm hole is an enquiry-only nominal, with minimum calculated adjacent nominal copper gap of 0.144852 mm, **not** fabricated acceptance.
- Current governed PCB, generator, schematic, BOM, upper-cover mechanical authority and panel drilling are unchanged. Selected-next lower G1 carrier and 220x148 mm board, three-pillar TE bracket, NKK UB2 replacements and full seven-control assembly are still unimplemented. P16 MHTE3 narrow provisional clearance persists.
- `final_routing=false`, `layout_freeze=false`, `bom_freeze=false`, `manufacturing_release=false` are unchanged.

**ONE next engineering transaction after this checkpoint merges and CI passes:** lock the **specific TE double-D bushing-flat / PCB board-side / panel-angle registration** against native STEP and the existing bracket model, using an isolated shadow model and explicit mirrored/180-degree negative controls. Do not repeat the proven 15 terminal-tip survey. Once that angular registration is qualified, proceed to the seven-control native assembly. No design-source change or release permission is granted by this document.

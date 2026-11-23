# AE-076F7H — S35B-P17/P18 TE MRJE3404 terminal/footprint candidate checkpoint — Rev A0

**Date:** 23 November 2026.
**Classification:** DRAWING-DERIVED 15-TERMINAL RELATIVE GEOMETRY AND OUT-OF-REPO KICAD CANDIDATE ACCEPTED; **NO NATIVE BOARD INSTALLATION; NOT FOR FABRICATION**.
**Parent governed `develop`:** `3961f3f0b276c1c538c79592b00b672225ac292d` (merged P16).
**Component:** TE Connectivity / Alcoswitch MRJE3404; manufacturer part `1825537-3` (3P4T, Rev A3 drawing 3-4).

## Evidence disposition

- The user-run P17 read-only check matched all 15 manufacturer-drawing-derived C1/C2/C3/throw positions to 15 distinct anonymous TE STEP terminal locations (PCD 11.9888 mm). The unmirrored 0-degree candidate matches 15/15 sites; a 180-degree rotation matches only 14/15; the best reflected rotation also matches 14/15. Geometry is a **relative** source correspondence, not an independently fixed housing/bushing angular datum.
- P18 generated an **isolated out-of-repository** KiCad `.kicad_mod` with all 15 unique named through-hole pads. Re-read verified 15 source pads and 47 intentional wrong mirror/rotation configurations. The manufacturer's recommended shaft-end layout (X right, Y up) was converted to candidate KiCad F.Cu component view (X right, Y down); reversing visual X in an underside diagram is a display transform, **not** a second mirror applied to drilled holes.
- Candidate datum `(130,118)` mm, rotation 0 degrees, is analytical only. There is **no native KiCad import or STEP mating/overlaid physical registration**, and no confirmed housing-flat-to-pad rotational registration.
- P14 user-measured detents D1..D4 at full CCW to full CW select numbered throws 1..4 for each of C1, C2 and C3. The terminal-to-net truth table remains proposed, not live PCB/schematic authority. C3 unused throws 1/2/4 remain NC, never 0VA.
- Provisional 15x Ø1.42 mm pads / Ø0.762 mm hole produce a minimum 0.144852 mm nominal pad gap; this is **fabricator enquiry only**. Neither finished plated-drill tolerances nor annular ring, mask web, insertion or four-layer DRC is approved.

## Source evidence and hashes (SHA-256)

- TE Rev A3 manufacturer drawing `source_evidence/ENG_CD_1825537_A3 (2).pdf`: `F4319D2A91999BB09C6C9F036AB5E9585ED62F552CD2682D82F9AF2BFD90EA6B`.
- TE manufacturer archive `source_evidence/ENG_CVM_CVM_1825537-3_A.3d_stp (1).zip`: `F0E56322F0737FB334D19C33B3BFD6E056ECEFFBAAC3556D76B330CE0732F25C`.
- P14 governed static-continuity record `docs/design_pack/AE-076F7H_S35B_P14_TE_Matrix_Physical_Continuity_Rev_A0.md`: `790AC58FDC7B02730C0D79E999B427FF13621F476811C74D1389346E25FB77DC`.
- P16 `reports/S35B_P16_TE_BRACKET_SITE/P16_REPORT.json`: `31E2878CDE5CE70C2AA6C65C6A693F7D8753785DB8AF2BDC84C5A5B83287DBE1`.
- P17 `reports/S35B_P17_TE_15_TERMINAL_ANTIMIRROR/P17_REPORT.json`: `B6038C73605AEF594D437B1A865339CC555F9FFA91B056AE1091F01871A7884C`.
- P17 `reports/S35B_P17_TE_15_TERMINAL_ANTIMIRROR/P17_CONTACT_SITE_TABLE.txt`: `BEA68B16B710EF8B15A3B2EAC4B417D02AFADEBDA0158EC802B2B7DDA11E11F2`.
- P18 `reports/S35B_P18_TE_15PAD_KICAD_CANDIDATE/P18_REPORT.json`: `ECBF48E3C6E52167505111A44C9167166C2BE6169EDEB68AE686D5D884FD4C0A`.
- P18 `.pretty/` candidate footprint: `9F2CC841DE1A2692A9C461B72E5B1F9A55199A3C690BCD21078D5CCBED8913B3` (path under P18 report directory as recorded in its manifest).

These reports and binary source artefacts remain in `Shellac_Engineering_Staging/` (Dropbox), not tracked design files. P17/P18 are **user-executed** read-only results corroborated here by their source manifests/hashes, not fresh native KiCad or STEP qualifications.

## Authority and next gate

Current governed PCB, generator, BOM and current AE-076B upper-cover mechanical authority are **unchanged**. The selected-next lower carrier, 220x148 mm PCB and three-post independent TE support remain unimplemented. P16 MHTE3 marginal DFM and all other physical stack-ups remain OPEN. `final_routing=false`, `layout_freeze=false`, `bom_freeze=false`, `manufacturing_release=false` remain HELD.

**ONE next bounded engineering transaction after this checkpoint merges and CI passes:** use a native KiCad parser / PCB editor plus the authenticated TE STEP (FreeCAD 1.1.4) to register all 15 P18 through-holes to real TE terminal axes and independently establish the housing/bushing double-flat, board-side and rotation datum. Reject mirrored and 180-degree candidate placements. Preserve an isolated shadow/test PCB and do **not** install the footprint or open routing/DFM holds until native registration passes. Afterwards qualify the seven-control assembly.

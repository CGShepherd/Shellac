# AE-076F4C — TE MRJE3404 Matrix Selection and C&K Supersession — Rev A0

**Date:** 13 October 2026
**Status:** SELECTED PART; PHYSICAL / ELECTRICAL IMPLEMENTATION QUALIFICATION OPEN
**Parent:** `482c7bb37eb8ccaf3e23d80f6871885bc6273bad` (AE-076F4B)

## Decision

Select **TE Connectivity / Alcoswitch MRJE3404, manufacturer part 1825537-3**, as the **single production Channel Matrix rotary switch SW903**. Supersede **C&K A30403RNCB** for the current product. The C&K part is historical evidence only, **not** a procurable current option, preferred selection, or live fallback. It may only be reconsidered by a new governed decision with genuinely contradictory evidence. The selected TE matrix is not to be confused with the separately selected **C&K 7201SYCBE** Rumble and Mute toggles, which remain unchanged.

The TE selection is based on the accepted F3-series engineering downselect, actual manufacturer STEP provenance, 15 physical terminal locations, and the selected development mechanism of a **separate three-pillar aluminium plate** transferring switch actuation forces to the frame rather than the audio PCB. This is a **part-selection decision**, not approval of mounting dimensions, copper/drills, knobs, fasteners, or manufacturing.

## Electrical architecture retained unchanged

SW903 remains **3P4T, four-position BBM/non-shorting**, low-level contact duty, with operator CCW-to-CW mode sequence **DUAL L, STEREO, L+R, DUAL R**. Pole C connects `MONO_R_LEG` to `MONO_AVG` only in L+R. Both 4.7 kOhm / 0.1% averaging resistors and their SCH104 placement are unchanged. Operational MUTE → MATRIX → RUN is retained pending RUN12/bench. The AE-041 Rev A1 functional truth table and AE-068 RUN05 nominal matrix qualification remain electrical evidence; the former C&K physical part choice in those earlier records is now **superseded** by this decision, without rewriting the historical record.

## Live authority migration

This record takes precedence **only for the matrix part identity**, and is indexed alongside the AE-041 electrical truth-table authority. Controlled BOM, generator control/matrix models, mechanical evidence/current selection, top-cover stack, AE071-B03 routing hold, risk register and current-facing index are changed together. The TE shaft and knob assembly is **OPEN**; the previous KN900B1/4 knob must not be assumed physically compatible with the different TE shaft. No alternative Matrix part is authorised. The proposed single-G1 reinforced rail carrier, six separate PCB supports and three-pillar TE plate remain selected engineering **development direction**, not yet superseding the currently governed upper-cover support architecture.

## Conditions — CLOSE_BEFORE_FAB

1. Reconcile the exact TE 1825537-3 Rev A3 numbered 15-terminal drawing with physical B.Cu pad/terminal mapping, detents and anti-mirroring evidence; perform sample continuity if the exact drawing alone does not close the ambiguity.
2. Qualify manufacturer TE bushing, retainer, shaft/knob, true switch seating, pin-root/tip, PTH/solder strain and independent plate load path. No C&K physical dimensions may substitute for TE.
3. Reconcile TE and four genuine NKK seated planes and the two C&K 7201SYCBE toggles, lid aperture/knob clearances, positive tolerance allowance, servicing access and commercially obtainable spacer/fastener lengths. AE-076F4B rejects the unmodified direct 18/28 mm arrangement.
4. Qualify authentic chassis/rail carrier retention and stiffness, correct native PCB coordinates, five proposed support XY locations, all-layer copper isolation, 4-layer DRC/DFM, real connector service envelopes and deliberate CHASSIS/0VA isolation.
5. Complete outstanding RUN10/RUN12, full design assurance and all other recorded pre-routing blockers; the selected part does not constitute physical footprint implementation or clearance of any release gate.

**Release:** ROUTING HELD; layout freeze FALSE; BOM freeze FALSE; manufacturing release FALSE; PDR/CDR candidate freeze FALSE. Native PCB and panel drilling unchanged.

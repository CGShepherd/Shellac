# Project Shellac — Persistent Working State

**Purpose:** cross-chat continuity and execution index.
**Authority status:** NON-AUTHORITATIVE SUMMARY. If this file conflicts with controlled current authority, the controlled authority wins and this file must be corrected before further major work.
**Refresh rule:** update after every material engineering review, qualification pass, governed transaction, commit/push, or change to the critical path.

## 1. Repository baseline

- Branch: `develop`
- Last independently verified governed parent baseline before the AE-076F3N index reconciliation: `c578f460e9c1804b1c4699109cbd5b86434d5422` (AE-076F1F, checked 2026-10-12). For the actual promoted HEAD, inspect Git history; this entry is provenance, not a self-referential current commit claim.
- Governed subject at verified parent: `AE-076F1F: reconcile native control and mechanical evidence` (AE-076F0 `24899753d05597aedd7a2ced6a482e6e1001c705` retained as historical promoted baseline).
- Promotion parent (historical AE-076E-A): `258751f56f536cc28e836c2d013dbde46aaf4cb6`
- Historical AE-076E-B / AE-076F0 parent: `2a912eac1c63313443f99dc87f86e07232f1a40b`
- Current working phase: `AE-076F — post-F3L mechanical concept downselect, physical qualification and candidate-only implementation; mechanical authority NOT superseded`.
- AE-076F1A–F1E read-only MCAD/native-CAD qualification: authenticated Metcase rail profiles and corrected provisional cover datum, carrier-only nominal sampled insertion, 256 F.Cu footprints, interim MH1–MH4 and zero mounted control footprints. Latest evidence disposition: `docs/design_pack/AE-076F1F_Native_Control_and_Mechanical_Evidence_Rev_A0.md`; no support architecture supersession.
- Historical transaction state: AE076E_B_PROMOTED_AE076F_QUALIFICATION_AND_MCAD_HELD — AE-076E-B promotion and AE-076F startup; preserved as continuity provenance.
- Current transaction state: AE076F1F_EVIDENCE_RECONCILED_PHYSICAL_QUALIFICATION_HELD — six-upper-cover-support and C&K matrix current authority unchanged; all routing/layout/BOM/manufacturing holds remain. Later AE-076F3J FIX2 and AE-076F3K/L are informational analysis, NOT promoted design-authority transactions.
- Routing: HELD
- Layout freeze: FALSE
- BOM freeze: FALSE
- Manufacturing release: FALSE

## 2. Current design essentials

- Regulated rails: `+17.0 V / 0VA / -17.0 V`.
- One main audio PCB carries all seven controls directly.
- PCB orientation: F.Cu down / B.Cu up toward removable upper cover.
- **Current controlled support authority:** six PCB-to-removable-upper-cover primary supports; exact XY/Z/hardware/tolerances open, native footprint migration unauthorised. **Selected-next engineering concept (AE-076F3L, not authority):** stiffened open rail-engaged lower frame, independently supported main PCB on 20 mm M3 spacers, and flat three-arm TE switch plate on three separate 30 mm M3 metal pillars passing freely through three provisional PCB clearance holes. Conceptual carrier fit, actual holes and all control CAD remain CLOSE_BEFORE_FAB; no formal support supersession authorised.
- Bass: NKK `NR01105ANG13-2C` x2.
- Treble: NKK `NR01105ANG13-2A` x2.
- Channel Matrix production part: C&K `A30403RNCB`; MRJE3404 is provenance/considered alternative only.
- Rumble/Mute: C&K `7201SYCBE`.
- SCH101 LT5400: `LT5400BIMS8E-7#PBF`; EP9 to quiet 0VA implemented.
- Gain programming: TSW-104-07-G-D / MNT-104-BK-G, approximately 14/18/22 dB; no LOW/HIGH shunt = fail-safe ~18 dB.
- Cartridge loading: live dual per-channel main-board sockets, separate service cards remain qualification-open; no card=BASE; matched +47 pF and +100 pF L/R service pairs; audio path does not pass through card.
- AE-076E-A exact primitive: Samtec `SLW-102-01-G-D`, controlled 2x2 PTH footprint, pins 1/4=POS and 2/3=NEG; no generic 3D model substituted.
- Live generator and native PCB now implement per-channel H120/H220; H121/H122/C103/C104/C203/C204 are absent from the PCB, while H120 retains pins 1/4=POS and 2/3=NEG.
- DR-039 current implementation: branch-local 1 uF / 330 kOhm only in DIRECT/BYPASS; FILTER uses intrinsic SCH107 high-pass DC blocking.
- Grounding population: R909=0 ohm fitted; C909/D901/D902 DNP.
- H801/H802 output harness is HOT/COLD only with no 0VA conductor.
- Five-pole regulated-DC interface: pin1=0VA, pin2=+17 V, pin3=-17 V, pin4=CHASSIS, pin5 NC_RESERVED; pin1-shell bond prohibited.

## 3. Current one-off build philosophy

Shellac is expected to be a one-off build, not an iterative prototype-to-production programme.

Before fabrication, unresolved items must be classified as:
- `CLOSE_BEFORE_FAB`;
- `ESCAPE_ROUTE_REQUIRED`;
- `BENCH_ONLY_ACCEPTABLE`.

Where a residual uncertainty could otherwise require board or mechanical respin, provide a controlled low-impact recovery mechanism when technically sensible. Do not add speculative flexibility, especially in the cartridge/SCH101 low-level region.

Controlled standard:
`docs/knowledge/ONE_OFF_BUILD_RECOVERABILITY_STANDARD.md`

## 4. Current pre-layout critical path

1. Verified parent of the AE-076F3N index-only reconciliation is AE-076F1F `c578f460e9c1804b1c4699109cbd5b86434d5422`; preceding AE-076F0 `24899753d05597aedd7a2ced6a482e6e1001c705`, AE-076E-B `2a912eac1c63313443f99dc87f86e07232f1a40b` and immutable AE-076E-A `258751f56f536cc28e836c2d013dbde46aaf4cb6` are historical provenance. F3J FIX2 was locally run and informationally staged; F3L is an engineering concept downselect, not a native/authority promotion.
2. Perform bounded preliminary RUN10 design-driving tolerance/parasitic assessment at current `+17.0 V / 0VA / -17.0 V`, especially LT5400/CMRR, gain shunts, Grado 78C cable/loading and H120/H220 service-card parasitics, and SCH103 timing-component source/value choices. This is not full RUN10 closure.
3. Qualify the F3L preferred-next stiffened/open rail-engaged lower subframe and independent TE plate/pillar concept against authenticated Metcase and populated PCB models: measure G1 groove throat, check ~2.257 mm nominal downstand from G1 sheet-top to proposed frame bearing face, all switches/fasteners, H802/H120/H220 service envelopes, underside access, chassis capture/stiffness, tolerances, cover installation and grounding. The earlier six-cover-support concept remains CURRENT CONTROLLED authority pending deliberate supersession; no carrier geometry is yet released.
4. Complete RUN08-RUN14 under the current AE-076D qualification delta; preserve the AE-070 vendor THAT1646 full-chain AC model composition limit and prohibit transferring AC surrogate validity to nonlinear/noise/fault gates.
5. Resolve RUN10-driven SCH103 timing-cap decomposition and SCH108 ferrite selection before layout as justified; retain bench correlation where defensible.
6. Qualify exact physical seven-switch B.Cu terminal numbering, mirroring, common plane, contact truth, solderability, full Metcase assembly and cover apertures; assess TE MRJE3404 as a preferred engineering **candidate** against the still-governed C&K A30403RNCB. Screen three pillar clearance holes (investigative Ø7.0 mm and Ø9.5 mm all-layer copper voids) and independently located 6+ PCB supports. AE-076F3J confirms zero native switch footprints and interim MH1–MH4; no native PCB/support hole migration or panel drilling before evidence and governed approval.
7. Qualify ±17 V physical PSU set-point/dropout/ripple/startup/thermal behaviour, system rail fault-energy response and deliberate CHASSIS/0VA interfaces before system sign-off.
8. Freeze bounded four-layer fabrication stack, quantitative DRC/netclasses and instantiate/audit In1 0VA plane.
9. Conduct block-by-block independent design assurance, with explicit one-off recoverability classifications and documented dissent.
10. Consider routing release only after every relevant design-driving HOLD is resolved and a controlled permission transition is authorised.

## 5. Formal block-review sequence

Review in this order:
1. cartridge / input XLR / harness;
2. SCH101 RF, loading, gain and precision front end;
3. SCH103 replay EQ;
4. SCH107 rumble/direct path/DC blocking;
5. SCH104 isolation and mono preparation;
6. SCH105 channel Matrix;
7. SCH108 mute, THAT1646, ferrites, clamps and output interface;
8. 0VA / CHASSIS / earthing;
9. +17 V / 0VA / -17 V distribution;
10. external PSU: mains inlet through transformer, rectification, regulation, protection and DC cable.

Each block must end as:
- `PASS_FOR_LAYOUT`;
- `PASS_WITH_CONTROLLED_RECOVERY`;
- `HOLD`.

For every block review: implementation, evidence, component authority, PCB/MCAD, interfaces, FMEA/fault behaviour, procurement, serviceability, recovery path and residual qualification must be explicit.

## 6. Known open design-driving items

- AE-076F preliminary RUN10, full RUN08-RUN14, and full Metcase/PCB/seven-switch dimensional implementation of selected-next lower-subframe/TE-spider concept; AE-076E-B promotion is complete;
- exact SLW/TSW mated mechanical envelope and RUN10 interface parasitics/matching;
- exact component-specific capacitor body/mechanical fit and full MCAD collision assessment after successful H901/C30060/C35060 solid STEP export;
- gain-shunt physical pairing/orientation;
- RUN08 overload/clipping/recovery;
- RUN09 full-system noise;
- RUN10 tolerance/sensitivity/value engineering/parasitics;
- RUN11 Monte Carlo;
- RUN12 switching transients;
- RUN13 rail variation/ripple/start-up;
- RUN14 phantom/fault energy;
- SCH103 timing-cap source/value decomposition;
- SCH108 ferrite selection;
- exact seven-control B.Cu pin/pad/orientation mapping;
- controlled six-upper-cover-support authority supersession pending full MCAD and independent assurance; F3L three-point flat plate / independent 20/30 mm spacer alternative downselected for development only; TE retention/15-pin map/knob, PCB holes/all-layer copper/DRC, G1 rail downstand, full-chassis assembly, fasteners and service clearances remain CLOSE_BEFORE_FAB;
- bounded fabrication stack, In1 plane and quantitative DRC/netclasses;
- Grado 20-50 kHz model-validity/measurement disposition;
- PSU powered set-point/dropout/ripple/startup/thermal qualification.

## 7. Explicitly deferred to build/commissioning where presently acceptable

These remain subject to the recoverability standard and may move back to pre-fabrication closure if review shows respin risk:

- physical harness/crimp continuity;
- actual cartridge body/return continuity measurement;
- measured noise/CMRR/distortion correlation where no PCB change is expected;
- final hum/grounding confirmation with controlled R909/C909/D901/D902 population options;
- thermal measurements with the final assembled enclosure;
- load/cable stability and high-level PRE90 confirmation where design margin/recovery remains adequate.

## 8. Validation

- AE-076C governed baseline full suite: 743 passed.
- AE-076D governed baseline commit: `4975fba11a12f25744e35ea61e11578c66f3d50f`; promotion validated with 754 tests.
- AE-076E-A governed baseline: `258751f56f536cc28e836c2d013dbde46aaf4cb6`; promotion verified with 761 tests.
- AE-076E-B source-phase focused validation: PASS — 64 tests; current-decision audit and generated-SCH101 discriminator PASS.
- AE-076E-B native board SHA-256 `a5b519a21a2bbe2c9f3ad751134d43292a5b32184487100512ab045b6258861c`; H901 model `40cd349dcd35a3aa04844d09e13f92a40d90f1a664e1ad8baec2cd010259e87a`; capacitor model `35659ae3b9a50ddeb0aa5add4edfaea1770d99f3a8c2db7320eb8fb13be8ee1b`; actual-board STEP `84fae4cfe2fa5edc3436a36792f3da41c8f71d29e9cd711f469631b37200fe61`; KiCad CLI rc0 and no missing models, DNP excluded.
- AE-076E-B intermediate regression history: 764 passed/1 failed at superseded pre-F8 board assertion; subsequent 766 passed/1 failed at obsolete DR-038 wording. Both test contracts were reconciled to the live implementation.
- Full AE-076E-B governance-candidate regression on 2026-10-08: 767 passed in 45.34 seconds; decision/configuration authority audit PASS. Promoted Git `develop` baseline `2a912eac1c63313443f99dc87f86e07232f1a40b` was subsequently verified by read-only AE-076F startup on 2026-10-09: 767 passed in 47.46 seconds, authority audit PASS, hashes matched, local HEAD=origin/develop, clean index/tree. No routing/layout/BOM/manufacturing authorisation conferred.
- Reproducibility: the governed native PCB remains CRLF and SHA-256-pinned; .gitattributes uses a single-file -text -eol whitespace=cr-at-eol exception so staged/checked-out bytes remain identical without weakening Git whitespace verification.

- AE-076F0 governed commit `24899753d05597aedd7a2ced6a482e6e1001c705` promoted after 767 tests/decision audit; later read-only AE-076F1E reverified GitHub `develop` and clean index/tree.
- AE-076F1D authenticated Metcase and populated-PCB STEP models (FreeCAD 1.0.2), corrected the cover underside Y to -33.911678 mm, reported nominal populated-board-to-G1-carrier clearance 7.657547 mm, and sampled unobstructed carrier-only insertion with relevant end panel removed. No complete installation qualification.
- AE-076F1E controlled native PCB SHA-256 `a5b519a21a2bbe2c9f3ad751134d43292a5b32184487100512ab045b6258861c`: 256 F.Cu footprints; MH1–MH4 at (25,28), (235,28), (235,152), (25,152) mm; no physical seven-control footprints and no dedicated control CAD discovered by filename. Informational disposition `docs/design_pack/AE-076F1F_Native_Control_and_Mechanical_Evidence_Rev_A0.md`. Release held.

## 9. AE-076F3J–F3L mechanical implementation status (INFORMATIONAL, 2026-10-12)

- **Native baseline reverified by user-run F3J FIX2:** 1.60 mm board, SHA-256 `a5b519a21a2bbe2c9f3ad751134d43292a5b32184487100512ab045b6258861c`; 256 F.Cu footprints; 598 pads, comprising 592 other pads, four Ø3.2 mm interim MH1–MH4 NPTH supports and two Ø3.0 mm H901 connector locator NPTH holes; 12 F.Cu route/pour keepouts, no routed tracks or vias. Report/JSON/SVG staged outside Git under `Shellac_Engineering_Staging`; this is not layout or manufacturing approval.
- **Three-point mechanical downselect, user delegated:** TE candidate centre `(165,126) mm`; independent metal-post candidate centres LEFT `(143,144)`, RIGHT `(189,124)`, FRONT `(165,104) mm`. F3J native 2D Ø8 mm hypothetical hardware-to-nearest-courtyard gaps: +3.390 / +1.4705 / +1.506 mm. These are NOT authorised drill coordinates or 3D fastener/copper clearance.
- **F3L concept (non-governed):** 1.5 mm flat aluminium three-arm spider; TE MRJE3404 preferred development candidate mounted to three independent 30 mm M3 female/female pillars through provisional Ø7 mm non-plated PCB openings, with provisional Ø9.5 mm all-layer copper keepouts. Main 220×140×1.60 mm PCB independently supported by 20 mm M3 hex spacers at separate board fixing positions (4 perimeter plus at least 2 independently screened additional supports is an investigative target, NOT installed). Actual Harwin drawings, threads, spacing tolerances and procurement unqualified.
- **Nominal stack at cover underside datum 0:** PCB B.Cu +12.30 mm, F.Cu +13.90 mm; frame face +33.90 mm; 30 mm matrix pillars put plate lower surface / TE shoulder at +3.90 mm and 1.5 mm plate top +2.40 mm; TE housing gap 2.40 mm, pin-root gap 0.78 mm, pin tip projection 1.176 mm beyond F.Cu. These are conceptual model arithmetic, not qualified manufacturer solder/fastener/tolerance limits. Nominal G1 frame face ~2.257 mm below earlier guide-sheet top: unresolved true chassis fit.
- **Selected concept only, NOT full physical closure:** earlier bent top-hat, stacked-nut and PCB-clamping/shared-stud constructions no longer lead development unless contradictory evidence arises. The 3J real native 2D screen and F3L synthetic CadQuery coupon/STEP checks do not amount to a complete Metcase + true TE + real hardware + all seven controls assembly or electrical footprint acceptance.
- **Already resolved handling procedure:** C&K `7201SYCBE` Rumble/Mute toggle levers temporarily held upright during cover fitting/removal; do not reopen the tilted-lever clearance concern without contradictory physical evidence. This handling decision does NOT certify every other cover collision/fastener clearance.
- **Required CLOSE_BEFORE_FAB:** true TE 15 numbered pin/clockwise mode map; C&K-vs-TE formal downselect and stock; TE real retaining nut, shaft/knob and plate clearances; board holes/4-layer copper/mask/DFM with full DRC; full authentic chassis STEP plus populated PCB and all seven switch/mated harness 3D fit; G1 bearing/rail stiffness and retention; neutral assembly/shim design; measured fastener tolerances and safe 0VA/CHASSIS isolation. Release gates remain ROUTING HELD, LAYOUT/BOM FREEZE FALSE, MANUFACTURING RELEASE FALSE. Sole intended 0VA–CHASSIS link remains `R909=0Ω`.
- **Authority boundary:** current controlled documents still specify six removable-upper-cover supports and C&K `A30403RNCB` as the preferred matrix. This index records development preference only; no current configuration index, BOM, PCB, mechanical YAML or release record is superseded by these notes. F3L report/package is a ChatGPT local generated artefact; it has NOT been committed to Git or automatically saved in Dropbox.

## 10. Continuity rule

Do not begin a major new Shellac phase from conversation memory alone.

At the start of a new chat:
1. read this file in full;
2. read `PROJECT_GUIDANCE.md`;
3. verify Git branch/HEAD/origin/working-tree state;
4. inspect the current authority files referenced by this summary for the task at hand;
5. update this file again before the next major phase transition.

This file is an index, not a substitute for controlled design records.

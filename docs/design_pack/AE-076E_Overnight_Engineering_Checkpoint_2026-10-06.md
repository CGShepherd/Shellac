# Project Shellac — AE-076E Overnight Engineering Checkpoint — 2026-10-06

**Status:** NON-AUTHORITATIVE CONTINUITY CHECKPOINT\
**Purpose:** preserve the read-only engineering progress performed after AE-076D promotion while the governed repository remains unchanged.\
**Does not supersede:** `PROJECT_SHELLAC_WORKING_STATE.md` or any controlled current authority.

## 1. Governed Git state at start of this review

- branch: `develop`
- HEAD: `4975fba11a12f25744e35ea61e11578c66f3d50f`
- origin/develop: `4975fba11a12f25744e35ea61e11578c66f3d50f`
- subject: `AE-076D: reconcile executable authority and one-off build governance`
- working tree after push: clean
- AE-076D full regression before promotion: 754 passed
- routing: HELD
- layout freeze: FALSE
- BOM freeze: FALSE
- manufacturing release: FALSE

No governed repository modification, Git commit or push was made during the AE-076E overnight review.

## 2. Next critical-path phase

`AE-076E — SCH101 personality / native-CAD migration`

This phase combines two related closures:

1. migrate the AE-076C per-channel cartridge personality architecture into the live SCH101 source and native PCB;
2. close the H901/C30060/C35060 native 3D model-path defect already bounded by AE-076B2C evidence.

The implementation should be resumable around a deliberate human KiCad F8 checkpoint rather than using a fragile whole-board text rewrite.

## 3. Main electrical implementation finding

The selected AE-076C architecture is not merely a replacement of the old load header.

The current live main board includes:

- `C103` +47 pF left selectable load;
- `C104` +100 pF left selectable load;
- `C203` +47 pF right selectable load;
- `C204` +100 pF right selectable load;
- legacy ganged headers `H120/H121/H122`.

In the selected personality-card architecture the selectable capacitance belongs on the removable cards.

Correct main-board migration intent:

### Remove

- `C103`
- `C104`
- `C203`
- `C204`
- `H121`
- `H122`

### Retain/redefine

- `H120` — left local `SLW-102-01-G-D` personality socket

### Add

- `H220` — right local `SLW-102-01-G-D` personality socket

Net product population change: **-5 references**.

The main board continues to carry:

- 23.7 kΩ per leg to 0VA;
- fixed 47 pF per leg to CHASSIS RF;
- matched 100 Ω RF series isolation.

Gain programming H110/H111/H112 remains unchanged.

## 4. Personality pin map

Selected interface:

- pins 1 and 4 = POS;
- pins 2 and 3 = NEG.

Official Samtec SLW and TSW manufacturing prints were reviewed.

The 2x2 numbering geometry supports the intended 180-degree anti-reversal property:

- 1 ↔ 4;
- 2 ↔ 3.

Remaining `CLOSE_BEFORE_FAB` check:

- prove the exact KiCad main-board SLW footprint and card-side TSW footprint mating-face correspondence;
- prove actual native pad/net assignment after F8.

## 5. Exact connector evidence

Main-board socket:
`Samtec SLW-102-01-G-D`

- 2 rows x 2 positions;
- 2.54 mm pitch;
- 2.54 mm row spacing;
- manufacturer recommended 0.86 mm PTH;
- 20 µin / 0.51 µm gold contact;
- body height 4.57 mm;
- tail length 2.92 mm;
- double-row body width 4.95 mm.

Card-side header:
`Samtec TSW-102-07-G-D`

- 2 rows x 2 positions;
- 2.54 mm pitch;
- manufacturer recommended 1.02 mm PCB hole;
- 0.635 mm square post;
- 5.84 mm mating post;
- 10.92 mm overall;
- 10 µin gold contact-area plating.

Important: do **not** use one generic footprint for both parts; their recommended hole diameters differ.

## 6. Service-card direction

Selected card states:

- BASE = no card;
- +47 pF;
- +100 pF.

For +47/+100 use matched L/R card pairs.

Recommended simple production card:

- exact TSW-102-07-G-D;
- pins 1/4 common POS;
- pins 2/3 common NEG;
- one precision C0G/NP0 capacitor directly across POS/NEG;
- minimal loop/board area;
- capacitance value on silkscreen;
- optionally record measured capacitance/pair identity.

Do not include a speculative resistor footprint on normal cards unless RUN10 identifies a concrete need. A separate resistor-load service/development card can be made later without changing the main PCB.

Exact capacitor MPN/tolerance remains RUN10 work.

## 7. Placement migration

Current legacy ownership:

- left CLU-101-A includes C103/C104;
- right CLU-101-C includes C203/C204;
- CLU-101-F owns H120/H121/H122.

Selected ownership:

- H120 local to `CLU-101-A`;
- H220 local to `CLU-101-C`;
- remove C103/C104/C203/C204;
- retire empty CLU-101-F.

H120/H220 remain manual/local low-level placement items.

## 8. Native-board / F8 boundary

KiCad owns the live `.kicad_pcb`.

Recommended execution:

### E1 automated source/intent migration

- generator/component/pin/symbol changes;
- exact SLW footprint;
- SCH101 population/net changes;
- placement ownership;
- BOM/config/test updates;
- generated schematic;
- full source regression;
- explicit state `SOURCE_INTENT_MIGRATED_NATIVE_F8_REQUIRED`.

### Human F8 checkpoint

Expected product-reference delta only:

- remove C103/C104/C203/C204/H121/H122;
- retain/redefine H120;
- add H220.

Preserve:

- MH1–MH4;
- Edge.Cuts;
- locked board-only mechanical state;
- all unrelated footprints;
- unrouted state/no accidental segments or vias.

### E2 automated validation

- exact native reference delta;
- H120/H220 footprint/pad/net proof;
- board-owned geometry preservation;
- native integrity;
- H901/C30060/C35060 3D-path correction;
- STEP export;
- zero missing-model-path errors;
- full regression and authority audit.

Do not confuse `ZERO_MISSING_MODEL_PATHS` with final `FULL_MCAD_GEOMETRY_COMPLETE` if H120/H220 lacks an exact verified 3D body.

## 9. H901 / capacitor model closure

Existing evidence shows the live PCB refers to missing `.step` paths.

Recommended reproducible native bindings:

H901:
`${KICAD9_3DMODEL_DIR}/Connector_Molex.3dshapes/Molex_Mini-Fit_Jr_5566-06A2_2x03_P4.20mm_Vertical.wrl`

C30060/C35060:
`${KICAD9_3DMODEL_DIR}/Capacitor_THT.3dshapes/C_Rect_L7.2mm_W5.0mm_P5.00mm.wrl`

Controlled capacitor WRL expected SHA-256:
`f0e906df4774a169dbde3a20df6ce50381217ec0185b90547a241c5bd2fe68aa`

Exact H901 installed WRL hash remains to be captured locally before implementation.

## 10. Local evidence still required before E1/E2 freeze

A read-only probe has been prepared:

`SHELLAC_AE076E_PERSONALITY_NATIVE_READONLY_PROBE.py`

It requires:

- clean `develop`;
- HEAD/origin exactly `4975fba11a12f25744e35ea61e11578c66f3d50f`.

It makes no changes.

It captures:

- native board SHA and size;
- segment/via count and layer presence;
- exact H120/H121/H122/H220/C103/C104/C203/C204 footprint blocks;
- H901/C30060/C35060 model paths;
- MH1–MH4 footprint hashes;
- Edge.Cuts hash;
- pad/net/pose details;
- current generator population/cluster ownership;
- installed KiCad WRL/STEP existence and hashes.

This is the first local action required before implementation.

## 11. RUN08–RUN14 forward-readiness finding

The governed executable campaign currently stops at RUN07. Dedicated RUN08–RUN14 scripts/configs are not implemented.

Historical AE-050 still contains stale execution constants including:

- Grado 78E wording;
- ±18 V-era RUN13 sweep.

These must not be copied into new runners.

Current execution conditions must use:

- Grado Prestige 78C;
- ±17.0 V nominal rails;
- BASE/+47/+100 load states;
- branch-local DR-039;
- THAT1646 25 Ω/leg / 50 Ω differential semantics;
- S1G clamps;
- current output harness.

### Important RUN08 prerequisite

AE-070 proves the full upstream chain and isolated THAT1646 solve independently but the full vendor-THAT1646 composition times out.

The RUN07 surrogate is small-signal only and cannot support overload/recovery.

Therefore implement a controlled large-signal composition discriminator before RUN08. The preferred route for evaluation is a cascade-partitioned nonlinear method under stiff ±17 V rails:

- qualify upstream clipping/recovery to SCH108 input;
- drive isolated controlled SCH108/THAT1646 with the boundary waveform;
- correlate nominal cascade;
- leave rail interaction to RUN13 if relevant.

### RUN10 importance

RUN10 is likely the strongest remaining layout-driving run and must include:

- personality-interface/card parasitics and L/R mismatch;
- LT5400 complete-stage tolerance/CMRR;
- gain shunt;
- SCH103 timing-cap decomposition;
- DR-039/SCH107 tolerances/noise;
- 4.7 kΩ mono-pair matching;
- SCH108 ferrite/value sensitivity.

### RUN13

Do not reuse historical ±17.5–18.5 V as current nominal band.

Nominal is ±17.0 V. Exact robustness sweep around it remains to be explicitly frozen; physical PSU set-point/dropout/ripple/startup/thermal qualification remains separate.

### RUN14

Must use S1G/current ±17 V/current output semantics and a credible non-ideal PSU reverse-energy model or conservative surrogate. Do not trust forward-regulator macromodel convergence as proof of reverse-fault survival.

## 12. Provisional Dropbox documents added during this review

New, non-Git, pre-implementation documents in `docs/design_pack/`:

1. `AE-076E_Personality_and_Native_CAD_Engineering_Review_Rev_A0.md`
2. `AE-076E_Personality_and_Native_CAD_Execution_Manifest_Rev_A0.md`
3. `AE-076E_Forward_Qualification_Readiness_RUN08_RUN14_Rev_A0.md`
4. `AE-076E_Samtec_Personality_Pin_Numbering_Evidence_Addendum_Rev_A0.md`
5. this checkpoint.

These are deliberately not yet registered as current authority or pushed to GitHub.

## 13. Resume instruction

At the next Shellac session:

1. verify live Git still equals governed `4975fba...`;
2. read governed `PROJECT_SHELLAC_WORKING_STATE.md`;
3. read the four AE-076E provisional design-pack records listed above;
4. run the read-only AE-076E local probe and return its complete log;
5. reconcile any contradiction;
6. only then generate/apply E1 source migration;
7. stop for guarded KiCad F8;
8. complete E2 native/model validation;
9. keep release permissions false;
10. proceed to current-delta RUN08–RUN14 infrastructure after AE-076E closes.

## 14. Provisional disposition

**AE-076E architecture:** proceed.\
**AE-076E implementation:** HOLD pending local native-board/model probe.\
**Routing/layout:** HOLD.\
**No architecture abandonment indicated.**

The overnight review has reduced ambiguity but intentionally does not substitute documentation for implementation evidence.

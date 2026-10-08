# AE-076E — SCH101 Personality / Native-CAD Migration Engineering Review and Plan — Rev A0

**Parent governed baseline:** `4975fba11a12f25744e35ea61e11578c66f3d50f`\
**Parent authority:** AE-076D\
**Status:** PROVISIONAL PRE-IMPLEMENTATION ENGINEERING RECORD — NO PRODUCT MIGRATION EXECUTED\
**Release effect:** NONE — routing/layout/BOM/manufacturing permissions remain FALSE

## 1. Purpose

This record captures the post-AE-076D engineering review of the next pre-layout critical-path activity:

1. migrate the AE-076C selected per-channel cartridge-personality architecture into live SCH101 source and native CAD;
2. close the known H901 / C30060 / C35060 missing-3D-model bindings;
3. preserve the one-off-build recoverability discipline introduced by AE-076D;
4. define the controlled human-in-the-loop boundary required by KiCad native-board ownership.

This record is deliberately pre-implementation. It does not claim that the live generator, native PCB, BOM, or qualification campaign has changed.

## 2. Evidence reviewed

### 2.1 Governed Shellac authority

Reviewed current governed state at `4975fba11a12f25744e35ea61e11578c66f3d50f`, including:

- `PROJECT_SHELLAC_WORKING_STATE.md`;
- `config/decisions/ae076c_cartridge_personality.yaml`;
- `config/decisions/ae076d_qualification_delta.yaml`;
- `config/release/ae071_prerouting_hold.yaml`;
- `config/mechanical/ae076b2c_mcad_sources.yaml`;
- `generator/blocks/balanced_input.py`;
- `generator/core/components.py`;
- `generator/core/pins.py`;
- `generator/layout/placement_clusters.py`;
- `generator/layout/preliminary_placement.py`;
- `generator/layout/footprint_contract.py`;
- `generator/layout/kicad_native_pipeline.py`;
- current BOM and relevant SCH101/native tests;
- AE-071A, AE-075B, AE-076B2C, AE-076C and AE-076D assurance records.

### 2.2 External component evidence

Samtec / distributor evidence was checked for the exact selected interface:

- main-board receptacle: Samtec `SLW-102-01-G-D`;
- personality-card header: Samtec `TSW-102-07-G-D`.

Evidence supports:

- 4 contacts, two rows, 2.54 mm pitch and 2.54 mm row spacing;
- through-hole vertical interface;
- exact parts are listed as mating products;
- SLW-102-01-G-D mating-contact finish is 20 µin / 0.51 µm gold;
- SLW insulation height is 4.57 mm and post/tail length is 2.92 mm;
- published mated stacking height is 6.09 mm for the exact SLW product family entry;
- SLW recommended PCB hole diameter is 0.86 mm;
- TSW-102-07-G-D uses 0.635 mm square posts, 5.84 mm mating post and 10.92 mm overall length.

The exact service-card mechanical envelope still requires native/MCAD correlation before fabrication.

## 3. Key finding — the migration is not a header rename

The live SCH101 implementation currently puts the switchable cartridge-loading capacitance on the **main PCB**:

- left: `C103 = 47 pF`, `C104 = 100 pF`;
- right: `C203 = 47 pF`, `C204 = 100 pF`;
- ganged service headers: `H120`, `H121`, `H122`.

AE-076C selected a different physical mechanism:

- one local main-board personality socket per channel;
- `H120` left and `H220` right;
- no card = BASE;
- +47 pF and +100 pF are supplied by removable passive cards;
- the cartridge audio path never traverses the card; the card is only a differential shunt.

Therefore the correct live migration must remove the following **main-board** product objects:

`C103 C104 C203 C204 H121 H122`

and repurpose/replace `H120` as the left exact SLW socket while adding `H220` as the right exact SLW socket.

The four selectable capacitances must not remain on the main PCB after migration. Retaining them would create two competing personality mechanisms and would violate AE-076C's selected architecture.

Expected main-board product-population delta: **-5 references net** (remove six objects while adding H220; H120 persists as a reference but changes physical/electrical identity).

Gain programming `H110/H111/H112` is independent and is not changed by this migration.

## 4. Electrical interface contract

Per channel:

- main-board pins 1 and 4: local `LOAD_POS`;
- main-board pins 2 and 3: local `LOAD_NEG`;
- no other electrical node is present on the personality interface;
- no series audio connection passes through the connector.

The duplicate-node map is:

| Pin | Node |
|---|---|
| 1 | POS |
| 2 | NEG |
| 3 | NEG |
| 4 | POS |

For a rectangular 2x2 connector, 180° inversion exchanges 1↔4 and 2↔3. The selected map therefore preserves electrical polarity under 180° insertion.

No-card state leaves only the fixed main-board load:

- 23.7 kΩ per leg to quiet 0VA (~47.4 kΩ differential);
- 47 pF per leg to CHASSIS as the fixed RF shunt;
- 100 Ω matched RF series isolation.

This is inherently fail-safe with respect to cartridge signal continuity.

## 5. Service-card design intent

Two card values are currently selected:

- `+47 pF`;
- `+100 pF`.

For each value, use a matched left/right pair.

Recommended production-card implementation:

- exact `TSW-102-07-G-D` 2x2 THT header;
- pins 1/4 copper-connected as POS;
- pins 2/3 copper-connected as NEG;
- one C0G/NP0 precision capacitor directly across POS and NEG;
- minimum practical loop area;
- no series signal path;
- capacitance value clearly marked on silkscreen;
- pair identity / measured capacitance may be recorded for L/R matching;
- no cartridge-name-specific labelling.

AE-076C permits optional resistor positions on development cards, but the one-off recoverability review recommends **omitting an unused resistor footprint from normal production cards unless RUN10 establishes a specific need**. A later resistor-load service card can be fabricated without changing the main PCB, avoiding unnecessary leakage/parasitic area in the default one-off build.

Exact capacitor MPN/tolerance/footprint is intentionally not frozen by this record; it remains a RUN10/value-engineering item.

## 6. Placement ownership

The current central/ganged `CLU-101-F` load-programming ownership is no longer appropriate once the personality interface is per-channel.

Selected migration intent:

- `H120` becomes a member of the left local SCH101 input/load cluster (`CLU-101-A`);
- `H220` becomes a member of the right local SCH101 input/load cluster (`CLU-101-C`);
- remove `C103/C104` from `CLU-101-A`;
- remove `C203/C204` from `CLU-101-C`;
- retire `CLU-101-F` if it has no remaining members.

Both socket placements remain MANUAL placement authority and must be kept close to their corresponding `LOAD_POS/LOAD_NEG` nodes.

The interface remains on the electronics side of the main PCB unless later MCAD evidence requires otherwise. No B.Cu control-side migration is selected here.

## 7. Exact footprint intent

### Main-board SLW socket

Create a ProjectShellac-controlled footprint for `SLW-102-01-G-D` rather than reusing the generic pin-header footprint.

Required controlled dimensions:

- 2.54 mm pitch;
- 2.54 mm row spacing;
- 0.86 mm recommended PTH;
- 2x2 four-pad pattern;
- explicit pin-1 marker;
- courtyard based on the 4.95 mm double-row body width and the two-position body length;
- no guessed 3D body.

The footprint pin numbering must be validated against the exact Samtec drawing before native migration. The intended electrical invariant is the diagonal duplicate-node contract, not a particular drawing orientation.

### Personality-card TSW header

The service card must use an exact TSW-102-07-G-D footprint, with the manufacturer-recommended THT hole geometry. Do not reuse the SLW drill size for the male header.

## 8. Native-CAD / F8 boundary

KiCad owns `out/kicad/ProjectShellac.kicad_pcb`; the Shellac engineering model owns schematic/footprint/placement intent.

The official KiCad 9 workflow for synchronising schematic changes to the board is **Tools -> Update PCB from Schematic (F8)**. There is no governed Shellac reason to replace this with a fragile whole-board text rewrite.

AE-076E should therefore be executed in two controlled phases:

### E1 — source/intent migration

Automated:

- introduce exact personality symbol/pin contract;
- introduce exact SLW footprint;
- migrate SCH101 source to H120/H220;
- remove main-board selectable capacitors;
- reconcile placement ownership;
- reconcile current BOM/status;
- add AE-076E source-migration tests;
- regenerate generated schematic;
- run source-focused regression;
- stop with native PCB explicitly OPEN.

### Human F8 checkpoint

With KiCad closed before generation and then opened for F8:

- re-link by reference designator if required to preserve current H120 ownership/position;
- replace footprints from schematic;
- delete product footprints that no longer have symbols;
- do **not** override locked board-owned mechanical objects;
- inspect the exact change list before applying;
- save the native board;
- place new H220 within its governed local/manual placement region;
- retain MH1–MH4 board-only/locked objects unchanged.

Expected product-reference change set:

- remove: `C103 C104 C203 C204 H121 H122`;
- retain/redefine: `H120`;
- add: `H220`.

Anything materially outside that set requires review before proceeding.

### E2 — native validation/model closure

Automated/read-only-plus-bounded model binding:

- prove expected reference set;
- prove MH1–MH4 byte/geometry ownership unchanged;
- prove Edge.Cuts unchanged;
- prove no routed segments/vias were introduced;
- prove H120/H220 exact footprint/pad map;
- bind H901 and C30060/C35060 to the already-proven KiCad-library WRL geometry;
- execute native structural audit;
- export a fresh STEP;
- fail if any `Could not add 3D model` / `File not found` remains;
- run full regression and `git diff --check`.

## 9. H901 / C30060 / C35060 3D-model disposition

AE-076B2C already proves the geometry; the remaining problem is the live native model path.

Current export evidence records:

- H901 asks for the canonical Mini-Fit Jr model with `.step` extension and fails;
- C30060/C35060 ask for `C_Rect_L7.2mm_W5.0mm_P5.00mm.step` and fail.

Controlled evidence proves usable WRL geometry:

- C30060/C35060 installed WRL SHA-256:
  `f0e906df4774a169dbde3a20df6ce50381217ec0185b90547a241c5bd2fe68aa`;
- H901 exact Molex vendor model identity/geometry was separately probed and controlled;
- current KiCad canonical Mini-Fit Jr footprint references the KiCad 9 WRL model.

Recommended runtime binding:

- use reproducible KiCad 9 library WRL paths in the native board;
- retain the exact vendor H901 STEP only as geometry/provenance corroboration;
- do not make a clean clone depend on an untracked local vendor STEP.

This closes a reproducibility weakness without weakening source provenance.

## 10. Recoverability classification

| Item | Disposition before fabrication | Rationale |
|---|---|---|
| H120/H220 pin map and 180° benignity | CLOSE_BEFORE_FAB | Wrong map can mis-load the cartridge; fully closable analytically/native |
| Exact SLW/TSW footprint drill/pitch | CLOSE_BEFORE_FAB | Fabrication-driving geometry |
| Interface/card parasitic capacitance | CLOSE_BEFORE_FAB | Low-level HF loading; RUN10 must bound it |
| L/R card capacitance matching | CLOSE_BEFORE_FAB for card build; BENCH_SELECTABLE thereafter | Cards are removable/matchable without main-board respin |
| Cartridge+cable total capacitance choice | BENCH_ONLY_ACCEPTABLE | Select BASE/+47/+100 after measurement; no PCB respin |
| Exact card capacitor MPN | CLOSE_BEFORE_FAB for card fabrication | Value/tolerance/dielectric drive matching |
| Optional resistive loading | BENCH_ONLY_ACCEPTABLE via dedicated service card if later justified | No main-board change needed; omit speculative default footprint |
| Exact mated socket/header Z and clearance | CLOSE_BEFORE_FAB | Mechanical interference risk |
| H901/C30060/C35060 model binding | CLOSE_BEFORE_FAB | Required for trustworthy full MCAD |
| Powered cartridge/body isolation measurement | BENCH_ONLY_ACCEPTABLE | No expected PCB change if current interface remains isolated as designed |

## 11. FMEA / hostile-review observations

### Reversed personality card

Mitigation: diagonal duplicate-node map. Expected effect: none electrically.

### No card fitted

Effect: BASE state. Signal path remains intact. Safe/default configuration.

### Wrong-value card fitted

Effect: cartridge HF loading differs from intended service setting. Non-destructive and reversible. Label cards by capacitance and record measured pair values.

### One channel card omitted

Effect: L/R capacitance mismatch. Detect by visual inspection / commissioning capacitance record. No signal interruption.

### Connector contact resistance

Because the audio path is not routed in series through the card, contact resistance is not a first-order signal-series error. Leakage/contact contamination and parasitic capacitance remain relevant and belong in RUN10/inspection.

### Connector/card parasitic capacitance

This is the dominant unresolved low-level concern. It remains `CLOSE_BEFORE_FAB`; the selected architecture is not released for layout merely because the topology is fail-safe.

### Daughtercard mechanical leverage

Small 2x2 cards should remain compact. Exact board envelope and mated Z must be included in the full service-module MCAD. Avoid unnecessarily tall/heavy card structures.

## 12. Independent-panel provisional disposition

**Principal analogue design:** architecture remains sound; migrate as selected.\
**Hostile reviewer:** do not leave the four selectable capacitors on the main PCB.\
**PCB/EMC:** local per-channel socket ownership is preferable to the present central ganged service cluster. RUN10 parasitic bound remains mandatory.\
**Mechanical/integration:** published mating geometry materially reduces uncertainty, but exact card envelope/clearance remains pre-fabrication work.\
**Reliability/service:** no-card BASE and non-series contacts are strong one-off-service properties.\
**Configuration/release:** source migration and native F8 must be one governed AE-076E chain; no partial state may be promoted.\
**Independent chief-engineer disposition:** **HOLD before layout; proceed with AE-076E controlled migration.**

## 13. Expected closure from AE-076E

AE-076E should be allowed to close:

- live H120/H220 personality implementation;
- removal of legacy main-board selectable load capacitors/headers;
- exact personality socket 2D footprint and pin map;
- local placement ownership;
- H901/C30060/C35060 live 3D model-path defect;
- zero-missing-model native STEP export, subject to exact personality-card 3D completeness being explicitly reported rather than hidden.

AE-076E must **not** close:

- RUN10 personality-interface capacitance/matching;
- gain-shunt physical pairing/orientation;
- exact service-card capacitor MPN/tolerance;
- full six-support/control-plane/chassis MCAD;
- exact control footprints;
- RUN08–RUN14;
- routing/layout/BOM/manufacturing release.

## 14. Next action

Run the companion read-only probe against the clean governed `4975fba...` baseline. Use its native-board and installed-model output to freeze the exact AE-076E transaction preflight and F8 expected-delta guard before applying any product change.

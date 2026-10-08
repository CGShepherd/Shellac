# AE-076E — Personality / Native-CAD Migration Execution Manifest — Rev A0

**Parent governed baseline:** `4975fba11a12f25744e35ea61e11578c66f3d50f`\
**Status:** PROVISIONAL EXECUTION MANIFEST — PRE-IMPLEMENTATION\
**Companion engineering record:** `docs/design_pack/AE-076E_Personality_and_Native_CAD_Engineering_Review_Rev_A0.md`\
**Release effect:** NONE

## 1. Purpose

This manifest converts the AE-076E engineering review into a bounded, resumable implementation transaction. It exists to prevent scope creep and to make the KiCad F8 checkpoint auditable.

No source, native PCB, release authority, or qualification state is changed merely by this document.

## 2. Governed starting state

Required before any AE-076E implementation:

- branch `develop`;
- `HEAD == origin/develop == 4975fba11a12f25744e35ea61e11578c66f3d50f`;
- working tree clean;
- no staged changes;
- KiCad closed and no Shellac lock files;
- routing/layout/BOM/manufacturing permissions all false.

If any precondition fails, stop.

## 3. E1 — source/intent migration: expected source scope

### 3.1 Electrical generator

Expected modifications:

- `generator/blocks/balanced_input.py`
  - remove live main-board switchable load capacitors `C103/C104/C203/C204`;
  - remove legacy ganged load service headers `H121/H122`;
  - repurpose `H120` as the left per-channel personality socket;
  - add `H220` as the right per-channel personality socket;
  - connect H120 pins 1/4 to `SCH101_L_LOAD_POS`, 2/3 to `SCH101_L_LOAD_NEG`;
  - connect H220 pins 1/4 to `SCH101_R_LOAD_POS`, 2/3 to `SCH101_R_LOAD_NEG`;
  - keep fixed 23.7 kΩ/leg, fixed 47 pF/leg-to-CHASSIS and 100 Ω RF isolation unchanged;
  - keep H110/H111/H112 gain programming unchanged.

- `generator/core/components.py`
  - add an exact personality-socket component helper;
  - exact main-board MPN `SLW-102-01-G-D`;
  - exact ProjectShellac footprint;
  - no legacy MNT-102 shunt semantics on the main-board socket.

- `generator/core/pins.py`
  - add semantic pin contract for the new 2x2 personality socket;
  - preserve physical pin numbers 1–4 exactly.

- `generator/writers/kicad9.py`
  - embed the new symbol and pin count;
  - retain deterministic generated-symbol behaviour;
  - do not disturb existing service-header symbols used by gain programming or historical evidence.

### 3.2 Controlled footprint

Expected new file:

- `generator/footprints/ProjectShellac.pretty/Samtec_SLW-102-01-G-D_2x02_P2.54mm_Vertical.kicad_mod`

Mandatory footprint invariants:

- 2x2 THT;
- 2.54 mm pitch;
- 2.54 mm row spacing;
- 0.86 mm recommended finished/drill-hole basis from Samtec footprint evidence, subject to normal KiCad pad annulus rule;
- pin 1 visibly marked;
- explicit exact MPN/value metadata where supported;
- courtyard based on manufacturer body dimensions, not generic pin-header assumptions;
- no guessed/unverified 3D model embedded merely to make STEP export look complete.

### 3.3 Placement intent

Expected modification:

- `generator/layout/placement_clusters.py`
  - `CLU-101-A`: remove C103/C104, add H120;
  - `CLU-101-C`: remove C203/C204, add H220;
  - retire empty legacy `CLU-101-F`;
  - H120/H220 remain manual/local low-level placement items.

Potential modification if needed for accurate envelope only:

- `generator/layout/preliminary_placement.py`
  - add an explicit envelope hint for the exact SLW footprint;
  - do not alter global board architecture.

### 3.4 BOM / current-state configuration

Expected modification:

- `config/bom/shellac_bom.yaml`
  - legacy MNT-102 load shunt: superseded/not fitted;
  - legacy three TSW-102 main-board load headers: superseded/not fitted;
  - two SLW main sockets: current implemented after source migration;
  - personality-card TSW headers remain service artefacts with exact card layout / RUN10 open.

Expected modification during final E2 closure, not prematurely in E1:

- `config/decisions/ae076c_cartridge_personality.yaml`
  - record live migration complete only after generated schematic + native board reconcile;
  - retain RUN10 and physical-card qualification open.

- `config/decisions/current_decision_index.yaml`
  - update DR-038 implementation wording only after E2 native validation.

- `config/decisions/document_authority.yaml`
  - register AE-076E assurance record only after E2 closure.

- `config/release/ae071_prerouting_hold.yaml`
  - advance authority only after complete E2 validation;
  - B08 remains OPEN for gain-shunt physical pairing/orientation and RUN10 interface parasitics/matching;
  - all release permissions remain false.

## 4. E1 regression files expected to change

Expected updates/new tests:

- `tests/test_balanced_input.py`
  - assert C103/C104/C203/C204 absent;
  - assert H121/H122 absent;
  - assert H120/H220 present;
  - assert exact SLW footprint/MPN;
  - assert diagonal POS/NEG pin contract.

- `tests/test_ae071a_sch101_migration.py`
  - preserve historical AE-071A gain-migration assertions;
  - replace current-population expectations that are superseded by AE-076E;
  - retain regression that old series links remain absent.

- `tests/test_ae076c_cartridge_personality.py`
  - preserve selected architecture invariants;
  - later assert implementation status only after E2.

Recommended new test:

- `tests/test_ae076e_personality_native_migration.py`
  - explicit source population delta;
  - electrical pin-map invariant;
  - no-card BASE invariant;
  - placement ownership;
  - BOM state;
  - fail-closed release state.

Potential dynamic tests expected to continue passing without semantic rewrite:

- `tests/test_footprint_contract.py`;
- `tests/test_preliminary_placement.py`;
- `tests/test_cluster_placement_baseline.py`;
- `tests/test_real_footprint_audit.py`;
- `tests/test_sch101_human_readable.py`.

Any unrelated test change requires justification.

## 5. E1 generated-output boundary

After source migration:

- regenerate the KiCad schematic/project source;
- verify generated provenance;
- run native hierarchical ERC on the schematic;
- run the full Python regression suite;
- run authority audit and `git diff --check`.

At this point **do not** claim native PCB migration complete.

E1 should deliberately stop with an explicit state equivalent to:

`SOURCE_INTENT_MIGRATED_NATIVE_F8_REQUIRED`

No commit/push should occur between E1 and E2 unless a deliberately controlled intermediate checkpoint is judged necessary.

## 6. Human KiCad F8 checkpoint

KiCad is the owner of the native PCB document.

Expected product reference delta:

### Remove

- `C103`
- `C104`
- `C203`
- `C204`
- `H121`
- `H122`

### Retain but redefine

- `H120`

### Add

- `H220`

No other product reference deletion/addition is expected from the SCH101 personality migration.

Before accepting F8 changes:

- inspect the change list;
- re-link H120 by reference if KiCad asks rather than creating a duplicate identity;
- replace H120 footprint with the exact SLW footprint;
- add H220;
- delete only genuinely orphaned C103/C104/C203/C204/H121/H122;
- do not remove or unlock MH1–MH4;
- do not introduce routed segments or vias;
- do not accept unrelated footprint substitutions.

Save the board only after this review.

## 7. Native-board preservation fingerprints

The companion read-only probe records before-F8 fingerprints for:

- native board whole-file SHA-256;
- Edge.Cuts blocks;
- MH1–MH4 footprint blocks;
- H120/H121/H122;
- C103/C104/C203/C204;
- H901;
- C30060/C35060;
- current segment/via count.

E2 must compare the post-F8 board against these fingerprints.

Required unchanged:

- Edge.Cuts geometry;
- MH1–MH4 identity, pose, locked state and board-only/BOM/POS exclusions;
- all unrelated routed-copper state;
- unrelated connector/control/reference identities.

## 8. E2 — native 3D model closure

The existing AE-076B2C evidence is sufficient to define the intended fixes, but the local read-only probe must confirm actual installed paths/hashes first.

Expected bounded model-path corrections:

- H901:
  `${KICAD9_3DMODEL_DIR}/Connector_Molex.3dshapes/Molex_Mini-Fit_Jr_5566-06A2_2x03_P4.20mm_Vertical.wrl`

- C30060/C35060:
  `${KICAD9_3DMODEL_DIR}/Capacitor_THT.3dshapes/C_Rect_L7.2mm_W5.0mm_P5.00mm.wrl`

Controlled capacitor WRL SHA-256 expected:

`f0e906df4774a169dbde3a20df6ce50381217ec0185b90547a241c5bd2fe68aa`

H901 installed WRL hash is to be captured by the read-only probe before it becomes an implementation assertion.

Do not substitute an untracked local vendor STEP as a runtime board dependency.

## 9. E2 validation requirements

After F8/model binding:

1. exact product-reference delta matches section 6;
2. H120/H220 exact footprint and pin/net mapping pass;
3. H121/H122 and C103/C104/C203/C204 absent from live PCB;
4. MH1–MH4 preservation passes;
5. Edge.Cuts preservation passes;
6. no copper segment/via regression;
7. native board structural audit passes;
8. generated schematic/native reference populations reconcile;
9. KiCad DRC/ERC expectations remain fail-closed;
10. STEP export runs with no missing-file/model-path error;
11. STEP evidence explicitly distinguishes:
    - `ZERO_MISSING_MODEL_PATHS`;
    - from `FULL_MCAD_GEOMETRY_COMPLETE`.
12. full Python suite passes;
13. current-decision audit passes;
14. `git diff --check` passes.

The lack of a verified exact 3D model for H120/H220 must not be hidden. If the exact SLW socket is intentionally left without a model, the STEP may have zero missing **paths** while remaining incomplete for final interference analysis. That condition remains a mechanical pre-fabrication blocker.

## 10. Recoverability and release

The personality architecture remains a good one-off recovery mechanism because:

- no card = safe BASE;
- card contacts are not in series with the audio path;
- value changes are reversible without main-board rework;
- matched L/R cards can be measured and selected.

However, before fabrication the following remain `CLOSE_BEFORE_FAB`:

- exact footprint/pin map;
- connector/card parasitic capacitance bound;
- service-card capacitor MPN/tolerance/matching;
- exact mated mechanical envelope.

No routing/layout/BOM/manufacturing permission may be enabled by AE-076E.

## 11. Expected AE-076E closure statement

If and only if E1 + F8 + E2 all pass:

- personality **implementation** may move from selected-next to live;
- native H901/C30060/C35060 missing-path defect may close;
- B08 must remain OPEN but narrowed to:
  - gain-shunt physical pairing/orientation;
  - RUN10 personality-interface capacitance/LR matching;
  - any remaining exact card/mechanical evidence.

Next design-driving activity then becomes RUN08–RUN14, with RUN10 specifically allowed to drive value/footprint changes before routing.

## 12. No-regression rule

If the local probe, F8 delta, native audit or RUN10 evidence contradicts this manifest, stop and revise AE-076E. Do not force the implementation to match this plan merely because it has been documented.

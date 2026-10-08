# AE-076E-B — Source Migration and Native Reconciliation — Rev A0

**Parent governed baseline:** `258751f56f536cc28e836c2d013dbde46aaf4cb6`
**Parent subject:** `AE-076E-A: qualify SCH101 personality interface primitive`
**Status:** SOURCE_MIGRATED_NATIVE_F8_REQUIRED
**Release effect:** NONE — routing/layout/BOM/manufacturing permissions remain FALSE

## 1. Purpose

AE-076E-B completes the controlled migration selected by AE-076C and prepared
by AE-076E-A. This record is resumable across the mandatory native-KiCad F8
checkpoint. Do not commit while this record has source-only status.

## 2. B0 evidence frozen before mutation

- source board population: 257;
- native footprint blocks: 261 including MH1-MH4;
- native board SHA-256: `2e8934d9357f85cda82a47e7a19524c5fd76b1d8357f6c2a95cfaa559b0b1417`;
- Edge.Cuts SHA-256:
  `fb572761a9e679405cb8aa43dbaa45b80848eccb9d6ba5733de39de341f80091`;
- zero segments / zero vias;
- H901 vendor STEP ZIP SHA-256:
  `448ccc66ed709367f5016aebf1118f7ced04726d4d3b5b1bb076387f30647f5d`;
- H901 extracted STEP SHA-256:
  `40cd349dcd35a3aa04844d09e13f92a40d90f1a664e1ad8baec2cd010259e87a`;
- capacitor WRL SHA-256:
  `f0e906df4774a169dbde3a20df6ce50381217ec0185b90547a241c5bd2fe68aa`.

## 3. Source migration

Legacy source:
`H120 H121 H122 C103 C104 C203 C204`

Current source:
`H120 H220`

H120/H220 use exact `SLW-102-01-G-D`. Pins 1/4 are POS and 2/3 are NEG.
No card is BASE. +47/+100 pF is provided by matched removable L/R cards.

Projected PCB-owned source population: 252.

## 4. Placement

- H120 -> CLU-101-A;
- H220 -> CLU-101-C;
- CLU-101-F retired.

## 5. Required F8 delta

Remove:
`C103 C104 C203 C204 H121 H122`

Retain/redefine:
`H120`

Add:
`H220`

Expected native footprint blocks including MH1-MH4: 261 -> 256.

Post-F8 H120 pads 1/4 -> `SCH101_L_LOAD_POS`; 2/3 -> `SCH101_L_LOAD_NEG`.
Post-F8 H220 pads 1/4 -> `SCH101_R_LOAD_POS`; 2/3 -> `SCH101_R_LOAD_NEG`.

Obsolete LOAD47/LOAD100 branch nets must disappear.

## 6. Preservation

F8 must preserve Edge.Cuts, MH1-MH4, zero segments, zero vias and unrelated
product references.

## 7. 3D policy

- H901: exact controlled project-local vendor STEP only.
- C30060/C35060: controlled installed KiCad WRL after hash verification.
- H120/H220: no generic 2x2 3D model; exact SLW/TSW mated geometry remains
  CLOSE_BEFORE_FAB.

`ZERO_MISSING_MODEL_PATHS` is not the same claim as
`FULL_MCAD_GEOMETRY_COMPLETE`.

## 8. Current hold

Source migration is complete. Native F8, 3D binding, exact mated MCAD and RUN10
interface parasitic/matching work remain open. Release permissions remain
FALSE.

## 9. Source-phase validation

- focused source regression: PASS — 64 tests;
- current-decision audit: PASS;
- generated SCH101 discriminator: PASS;
- native PCB SHA: unchanged;
- `git diff --check`: PASS;
- release permissions: FALSE.

## 10. Resume rule

Do not stage, commit or push this source checkpoint. Next action is guarded
KiCad F8 followed by the AE-076E-B native resume/validation transaction.

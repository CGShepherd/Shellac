# AE-076F5Y — KiCad 10 native configuration migration — Rev A0

**Date:** 26 October 2026
**Baseline:** `develop` `b6f2c0644efcfe87e0b17b2c4ead02970ebb9654` before promotion.
**Classification:** Governed toolchain-path migration ONLY; no schematic,
physical footprint, netlist, stack-up, outline, routing or mechanical selection change.

## Decision and bounded implementation

- Make KiCad 10.0.7 the active version-specific CLI fallback and footprint/3D model lookup.
- `generator/kicad_erc.py`: KiCad 10.0 binary fallback and accompanying error text.
- `generator/writers/kicad9.py`: substitute the generated footprint library variable
  `KICAD10_FOOTPRINT_DIR` for `KICAD9_FOOTPRINT_DIR` once in the generator template.
  Its historical Python module name is intentionally preserved.
- `out/kicad/ProjectShellac.kicad_pcb`: substitute **197** standard 3D-model
  references to `KICAD10_3DMODEL_DIR`, preserving **three** project-relative STEP
  references and all other bytes.
- Update two exact regression-test expectations, retaining the SHA-256 pin and the
  KiCad library version assertion; neither test is skipped nor relaxed.
- Native PCB SHA-256 changes from `a5b519a21a2bbe2c9f3ad751134d43292a5b32184487100512ab045b6258861c` to `6824b2c311173046e0fd8ec782d8a61ba017ca2cc359cc7a17179252b28f81a2` solely because of
  model-path token substitutions. This is NOT a PCB electrical/physical revision.

## Qualification — isolated candidate

- AE-076F5Y FIX2 self-test and candidate preflight PASSED.
- Baseline and candidate KiCad 10.0.7 ERC categories identical: 14 findings
  (8 dangling labels, 4 unconnected pins, 2 wire endpoints).
- Baseline and candidate KiCad 10.0.7 DRC categories identical: 336 findings
  plus 432 unconnected items. These are NOT fabrication acceptance results.
- Exported STEP native topology witness identical: 14 MANIFOLD_SOLID_BREP,
  16 CLOSED_SHELL, 1112 ADVANCED_FACE, 7229 CARTESIAN_POINT.
- Qualified candidate: **771 pytest passed**, decision/configuration authority audit PASS.
- Evidence ZIP SHA-256: `809be290cf6a069b173ee24318b6eb42b0a02bd325b6d61232269f1b8689a1d8`.
- Full transaction scope: five implementation/test files, this record, and the
  persistent non-authoritative working-state summary. Nothing else approved.

## Maintained holds

- Native PCB still 220 × 140 mm. 220 × 148 mm candidate, switch footprints,
  independent TE 1.5 mm three-pillar plate and six 17 mm PCB supports remain
  selected-next, not fabrication authority.
- The F4T seven-switch mounting selection remains unchanged.
- All ERC/DRC/unconnected, tolerance, TE bearing/retainer, C&K keying,
  NKK flange, registration, G1 carrier, PDR/CDR, layout/routing/BOM/fabrication
  qualifications retain their pre-existing holds.
- Keep KiCad 9 installed until a separately evidenced dependency inventory
  confirms safe removal. FreeCAD–KiCad integration plugin remains DEFERRED.
- No change to GitHub/Dropbox operating process or the previous read-only
  Dropbox checkout.

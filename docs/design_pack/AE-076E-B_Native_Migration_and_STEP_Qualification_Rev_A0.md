# AE-076E-B — Native Personality Migration and Solid STEP Qualification — Rev A0

**Governed parent:** `258751f56f536cc28e836c2d013dbde46aaf4cb6` (`develop`).\
**Current transaction:** source/native implementation verified; 767-test regression and decision audit PASS; staged review and commit/push pending.\
**Release:** ROUTING HELD; layout/BOM/manufacturing permissions FALSE.

## Native electrical and placement evidence

- Current native PCB SHA-256: `a5b519a21a2bbe2c9f3ad751134d43292a5b32184487100512ab045b6258861c`.
- Exactly 256 native footprint blocks including board-only MH1-MH4; zero segments/vias.
- Live main-board sockets H120 (L) and H220 (R), exact Samtec `SLW-102-01-G-D` 2x2 PTH footprint.
- Pad contract on each socket: pins 1/4 = corresponding `SCH101_*_LOAD_POS`; 2/3 = corresponding `SCH101_*_LOAD_NEG`.
- H121/H122 and C103/C104/C203/C204 are absent from current native board. Historical H120 identity is repurposed.
- H120/H220 deliberately have no substitute 3D model: exact mated SLW/TSW geometry remains OPEN.
- Native board remains provisional for physical layout/routing. This evidence does not authorise either.

## Solid model sources and export

- H901 Molex `39-29-9063` (`0039299063`, `5566-06A2`), project-local vendor STEP SHA-256 `40cd349dcd35a3aa04844d09e13f92a40d90f1a664e1ad8baec2cd010259e87a`. Original manufacturer ZIP SHA-256 `448ccc66ed709367f5016aebf1118f7ced04726d4d3b5b1bb076387f30647f5d`.
- C30060/C35060 share the project-local **KiCad 10.0.6** `C_Rect_L7.2mm_W5.0mm_P5.00mm.step`, SHA-256 `35659ae3b9a50ddeb0aa5add4edfaea1770d99f3a8c2db7320eb8fb13be8ee1b`, 18,352 bytes. KiCad 9.0.7 installed WRL alone was not STEP-exportable.
- Final actual-board export `mechanical/mcad/pcb/generated/ProjectShellac_AE076EB_CapSTEP_FINAL_FIX2.step`: SHA-256 `84fae4cfe2fa5edc3436a36792f3da41c8f71d29e9cd711f469631b37200fe61`, 1,912,481 bytes.
- Final native export used KiCad CLI `pcb export step --subst-models --no-dnp`; exit 0; H901/C30060/C35060 enumerated; no missing-model or VRML diagnostic; D901/D902/C909 omitted as DNP.
- The temporary candidate FIX1 incorrectly resolved `${KIPRJMOD}` in a different project context; FIX2 qualified disposable absolute-path candidate and actual relative-path native export independently. Failure is retained as evidence, not concealed.
- **Scope of PASS:** these three STEP bindings resolve and export in KiCad. **Not demonstrated:** exact purchased capacitor MPN/body correspondence, Samtec mated geometry, whole-assembly interferences, Metcase internal rail geometry or fabrication-ready placement.

## PCB byte-preservation qualification

- The actual KiCad 9.0.7 board is CRLF, while the historical Git index was LF. The exact model/export test locks the actual native bytes.
- `.gitattributes` explicitly pins `out/kicad/ProjectShellac.kicad_pcb -text -eol whitespace=cr-at-eol` to preserve the KiCad-authored bytes and retain correct Git whitespace checking.
- Staged blob identity must equal `git hash-object --no-filters` and `git hash-object` for the PCB before commit; clean-checkout verification remains part of promotion.

## Pending verification before AE-076E-B governed promotion

1. Current-state YAML/BOM/decision index/release-hold/working-state reconciliation, with no historical AE-076B2B/B2C or AE-076E-A evidence rewriting.
2. Full pytest regression (767 passed), current-decision audit and Git whitespace checks PASS on 2026-10-08; staged-diff review and committed checkout reproducibility remain OPEN.
3. Exact untracked artefact ownership; unrelated zero-byte `cls` file is **not** part of this change and must remain unstaged until separately resolved.
4. Explicit commit/push only after verified green checks and user's review. This record itself is not a release approval.

## Open design-driving obligations

- RUN08–RUN14 (especially RUN10 capacitance, left/right matching and SCH101 precision/CMRR).
- Exact SLW/TSW mated assembly and service-card PCB design.
- Gain service-shunt physical pairing/orientation.
- Exact capacitor-body sourcing and full upper-cover/Metcase mechanical datum/clearance study.
- Seven PCB-mounted control footprints and support-plane XY/Z/tolerance closure.
- Full independent engineering/assurance review before routing and manufacturing release.

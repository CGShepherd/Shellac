# AE-076F7G — Nonbinding mechanical evidence and regression boundary (Rev A0)

**Status:** INFORMATIONAL IMPLEMENTATION / NOT AN ENGINEERING RELEASE. Does not supersede AE-076B, change the native PCB or allow routing, layout, BOM or manufacturing release.

## Purpose

The historical F7G-I7C-U1/U2/U3/U4R/U5 native FreeCAD studies passed narrow shadow screens for the gain-shunt access concept. They were executed on a historical F6H carrier (228 × 156 mm PCB assumption) and do not establish physical serviceability or correct registration to the selected-next 220 × 148 mm PCB. The current governed PCB remains 220 × 140 mm. A `PASS` from a historical native study is **not** evidence that the present design can be fabricated.

## Tier 1: ordinary pytest / GitHub CI

`generator/mechanical/qualification_register.py` and `tests/test_ae076f7g_shunt_access_evidence.py` provide a fast, deterministic record-and-authority gate. Existing `.github/workflows/ci.yml` runs all pytest files automatically on each push and PR. No FreeCAD or Dropbox environment is needed.

Checks include the current native PCB content hash; exact five-study evidence names, expected result statuses and SHA-256 references; cross-check of the Metcase SHA against the governed mechanical source; current AE-076B authority; explicit differentiation of 220 × 140, 220 × 148 and 228 × 156 mm outlines; U5 nominal access-gauge result including the PARK negative control; and all current release/qualification holds. Negative tests prove changes to these claims fail closed.

The recorded U5 R3 cutter `(145, 12)–(211, 60)` is **historical nonbinding evidence**; it is not a controlled mechanical feature or fabricator cut file. Any live PCB or authority change requires reconciliation and requalification, not automatic substitution of a report SHA.

## Tier 2: native CAD / complete-assembly qualification (NOT CLOSED)

Native FreeCAD requalification must use the current to-be-promoted PCB, actual carrier/reinforcement solids, accurate seven-switch models/shafts, Metcase rails and panels, all supports/bolts, connector mating and harness bend/strain-relief geometry. Check true Boolean intersections, connected metal, support-web and edge dimensions, tolerance stack, assembly/removal, service access, and loss of the W8/W2 cable web. Retain source hashes, tool versions, negative controls and native reports in the reproducible evidence pack. **Do not convert Tier 1 source-hash checks into claims of native CAD passage.**

Optional source-byte validation of the five historical reports on the local Windows system:

`python -m generator.mechanical.qualification_register --reports-dir "C:\Users\chris\Dropbox\000_Projects\000_Audio\Shellac_Engineering_Staging\reports"`

This validates exact SHA-256 bytes and reported statuses, but it does not rerun FreeCAD. All five reports must be present. Without `--reports-dir`, Tier 1 validates the checked-in register only and explicitly reports that report bytes were not verified.

## Physical and independent assurance (NOT CLOSED)

Finger/shunt pinch, shunt contact pairing and retention force, suitable pliers or service tools, sheet stiffness and fatigue, retaining fasteners, switch-knob-in-place maintenance, complete enclosure insertion, harness strain relief and electrical acceptance remain open. Record measured proof or a controlled one-off build recoverability disposition before the applicable release gate. Independent review, RUN08–RUN14 and final governed design approval remain required.

## Promotion rules

1. Never infer product authority from this evidence register, provisional U5 opening or historical BREP result.
2. Promote the selected-next architecture only through explicit AE-076B supersession and controlled model/PCB revision with fresh native proof.
3. Update the register and tests atomically when governed sources change; do not silently relax failing tests.
4. Require an authenticated complete-assembly qualification report and independent design review for mechanical release; final routing, layout, BOM and manufacturing permissions remain `false` until their separate authorities approve.

# AE-071B — Native PCB Mechanical Ownership Hardening — Rev A0

**Project:** Shellac
**Baseline:** `6067c6535cc40694a45b496c287c8068978fba8a` (AE-071A)
**Status:** QUALIFIED / READY FOR CONTROLLED COMMIT

## Trigger

During the AE-071A native-PCB reconciliation, KiCad F8 was intentionally run with
**Delete footprints with no symbols** enabled so obsolete product footprints could be
removed deterministically. The four frozen mechanical mounting holes `MH1`–`MH4`
were also deleted because they are board-owned footprints with no schematic symbols
and did not carry KiCad's board-only ownership attribute.

The holes were restored exactly from the committed SR-043 native board before
AE-071A qualification. AE-071A then proved their identity and native coordinates
were unchanged.

## AE-071A native-migration provenance carried forward

AE-071B preserves the detailed native-PCB reconciliation evidence without rewriting
the already-published AE-071A record:

- the first F8 attempt using stale UUID associations was rejected because it produced
  destructive cross-association/duplication behaviour; the board was not accepted
  from that attempt;
- the successful reconciliation used **re-link footprints to schematic symbols based
  on reference designators**;
- the controlled product migration was exactly **+23 / -18** references, leaving
  **255 current product footprints**;
- the native PCB contains those 255 product footprints plus the four board-owned
  mechanical references `MH1`–`MH4`, for **259 unique native references**;
- **232 / 232 retained product footprint poses** were unchanged;
- native `Edge.Cuts` geometry was unchanged;
- the semantic connectivity audit compared **578 / 578 connected comparable pads**
  exactly;
- package-only no-connect pads remained without PCB nets as intended;
- the board remained unrouted;
- an intermediate operator `git restore` returned the PCB to the committed baseline
  during reconciliation; this was a state-management event, not a design change;
- when obsolete product footprints were subsequently deleted by F8, `MH1`–`MH4`
  were also removed because they lacked board-only ownership. They were restored
  exactly from the committed SR-043 native-board authority before AE-071A closure.

This chronology is retained as configuration evidence because it explains why
mechanical footprint ownership required an explicit hardening increment.

## Decision

`MH1`–`MH4` are controlled PCB/mechanical objects, not electrical product
components. Their native KiCad footprints shall carry all of:

- `board_only` — KiCad **Not in schematic** ownership, protecting the board-owned
  footprint from schematic-driven deletion;
- `exclude_from_pos_files` — NPTH mechanical holes are not placement-machine parts;
- `exclude_from_bom` — the holes are mechanical board features, not BOM line items;
- `locked yes` — preserves the frozen SR-040/SR-043 mechanical datum against
  accidental interactive movement.

The frozen footprint identity remains
`MountingHole:MountingHole_3.2mm_M3`; the four existing coordinates are unchanged.

## Coordinate authority

SR-040 expresses the mounting-hole centres in the **board-local coordinate frame**.
The native KiCad document uses a non-zero drawing origin. Therefore the controlled
native relationship is:

`native footprint coordinate = native Edge.Cuts lower-left + SR-040 board-local hole centre`

For the current board, Edge.Cuts lower-left is `(20,20)` mm and SR-040 `MH1` is
`(5,8)` mm board-local, giving native `MH1=(25,28)` mm. The audit derives this
translation from the live Edge.Cuts geometry rather than hardcoding the document
origin.

## Configuration enforcement

`generator/layout/sr043_native_board_audit.py` is extended so native-board
integrity fails unless every frozen mounting hole is:

- present;
- at the SR-040 board-local location transformed through the live native Edge.Cuts origin;
- board-only;
- locked;
- excluded from BOM/POS output.

The audit explicitly separates `native_board_integrity_ok` from
`routing_authorized`. At AE-071B closure the required state is:

- `native_board_integrity_ok = true`;
- `routing_authorized = false`.

This prevents native-board structural readiness from being mistaken for configuration
authority to perform final routing.

Dedicated AE-071B regression tests independently verify:

- mechanical references remain outside the 255-reference product footprint contract;
- board ownership/lock/output-exclusion attributes exist for all four holes;
- native positions agree with SR-040 after the coordinate-frame translation;
- native-board integrity is good while final-routing authority remains held.

## Qualification evidence

The final read-only AE-071B qualification was executed against the exact controlled
14-file working state derived from AE-071A baseline
`6067c6535cc40694a45b496c287c8068978fba8a`.

Evidence at qualification:

- direct mechanical semantic checks:
  - native `Edge.Cuts` origin `(20,20)` mm;
  - board size `220 x 140` mm;
  - `MH1=(25,28)`, `MH2=(235,28)`, `MH3=(235,152)`, `MH4=(25,152)` after
    board-local-to-native coordinate translation;
- focused governance regression: **18 passed**;
- focused AE-071B/native regression: **12 passed**;
- native-board audit: product population, board outline, mounting-hole presence,
  pose, board ownership, locks, output exclusions, unrouted state and four-layer
  presence all passed;
- KiCad 9 native PCB read/parse gate: PASS, with project PCB SHA-256 unchanged by
  the parse operation;
- KiCad reported **198 DRC violations and 430 unconnected items** during that
  parse-only gate; these are not DRC-closure evidence and are expected while the
  board is deliberately unrouted;
- configuration authority audit: PASS;
- full repository regression: **633 passed**;
- integrated preflight: PASS through the currently qualified RUN00–RUN07 evidence;
  RUN08–RUN14 and the remaining RUN06 bench gates remain open;
- `git diff --check`: PASS;
- final dirty scope: exact controlled 14-file AE-071B state;
- no files were staged, committed or pushed by the qualification validator.

## Scope boundary

AE-071B changes no signal-chain topology, component value, product-footprint
identity, pad/net assignment, board outline, mounting-hole coordinate, copper
layer, route, or DR-039 state.

This hardening does **not** release routing, layout freeze, BOM freeze or
manufacturing release. Final mechanical/drilling release remains governed by the
existing open mechanical gates and AE-072 final design assurance.

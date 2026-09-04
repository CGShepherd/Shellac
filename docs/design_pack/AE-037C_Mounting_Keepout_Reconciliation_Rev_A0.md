# AE-037C — Mounting Keepout Reconciliation

**Revision:** A0  
**Parent:** AE-037/037A/037B  
**Status:** PHYSICAL PLACEMENT RECONCILIATION

## Problem

The four new SCH101 23.7 kΩ load/bias resistors increased the native PCB
population from 250 to 254. Placement ownership was repaired by AE-037A, but the
changed deterministic packing caused SR-041 to detect a frozen mounting-hole
keepout collision.

The frozen holes are at:
- MH1: (5, 8) mm;
- MH2: (215, 8) mm;
- MH3: (215, 132) mm;
- MH4: (5, 132) mm;

with 8 mm keepout diameter.

## Resolution philosophy

Do not override SR-041 and do not hard-code one component coordinate.

AE-037C adds a controlled minimum packing margin only to the two microvolt
front-input clusters (`CLU-101-A`, `CLU-101-C`). The apply tool evaluates
candidate margins from 1.5 to 8.0 mm and retains the **smallest** margin for
which the authoritative SR-041 collision audit returns:

- `ROUTING_RELEASED`;
- zero mounting collisions.

If no candidate succeeds, the tool restores 1.5 mm and aborts rather than
inventing a placement.

## Population-test reconciliation

Remaining duplicated `250` expectations are replaced with relational checks
against the live footprint contract where practical.

This patch changes physical proposal geometry only; AE-037 electrical values and
topology are unchanged.

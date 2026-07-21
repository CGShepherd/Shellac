# SR-019 — Deterministic Junction Dots — Rev A

## Purpose

Make true multi-wire joins visually unambiguous in every generated schematic
without changing the validated electrical design.

## Implemented rule

The KiCad writer now emits an explicit junction object where three or more
generated conductor directions meet at a common wire endpoint.

- A T-branch or four-way electrical branch receives one dot.
- A straight two-wire join or ordinary bend does not receive a dot.
- Two wires that merely cross do not receive a dot.
- A wire endpoint that happens to touch the middle of an unrelated wire is not
  silently converted into an electrical connection. Intentional branches must
  be represented by explicit coincident wire endpoints.

Junction UUIDs derive deterministically from the sheet identity and snapped
electrical coordinate.

## Engineering scope

No component, value, net name, analogue topology, gain, or connectivity decision
was changed. The change is entirely in schematic presentation metadata.

## Evidence

- 138 automated tests pass.
- The engineering model validates: 8 blocks and 27 signals.
- Native KiCad 9 hierarchical ERC reports zero violations.
- Gate 2A machine readiness remains passed at 8/8 blocks.
- SCH101 produces six explicit junction objects and its rendered PDF shows the
  conventional filled dots at true branch nodes.
- Gate 2B remains open at 2/8 human-reviewable sheets; SR-019 does not claim a
  new sheet-level readability conversion.

## Status

Accepted for installation subject to validation on the live Windows repository.


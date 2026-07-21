# SR-017 - Standalone Annotation and Human-Review Proof Rev A

## Purpose

SR-017 responds to review of the generated SCH101 sheet in KiCad.  The review
identified two separate shortcomings:

1. child sheets opened directly displayed placeholder references such as `R?`,
   `C?` and `U?`; and
2. electrically valid sheets used repeated labelled wire stubs rather than a
   conventional, human-readable circuit flow.

No analogue topology, component value, gain, replay curve, power or control
decision is changed by this increment.

## Standalone annotation correction

Every emitted component now carries two deterministic KiCad instance records:

- its authoritative path beneath the generated root hierarchy; and
- the child schematic's own root UUID path.

The second path allows a generated child sheet to retain its controlled
references when opened directly.  The hierarchy path remains unchanged.

## Human-readable proof sheet

SCH104 is the bounded presentation proof because its unity buffer signal path
is simple enough to assess without ambiguity.  It now uses:

- one hierarchical label at each true sheet boundary;
- continuous left-to-right signal conductors;
- test-point pins placed directly in the conductor;
- visible OPA1656-to-100-ohm-resistor connectivity; and
- short net labels only for power and analogue-reference connections.

This pattern is not yet claimed for the other seven sheets.

## Readiness interpretation

The readiness audit now reports two independent gates:

- **Gate 2A machine readiness** - hierarchy, pin connectivity, symbol
  resolution and native KiCad ERC;
- **Gate 2B human-review readiness** - conventional capture suitable for
  visual engineering review.

At SR-017 Rev A:

```text
Gate 2A machine readiness: PASS
Gate 2B human-review readiness: FAIL
Human-reviewable blocks: 1/8
```

The design must not move to PCB layout until Gate 2B passes and the resulting
schematics have been reviewed in KiCad.

## Acceptance evidence

- 129 Python tests pass.
- Engineering Model Rev A validates: 8 blocks, 27 signals.
- Model-driven build generates 8 implemented blocks and no pending blocks.
- Native KiCad hierarchical ERC reports zero violations.
- Standalone SCH104 PDF inspection shows controlled component references.
- Standalone SCH104 visual inspection shows continuous signal paths for both
  channels.

## Next increment

Apply the proven presentation pattern to the remaining sheets, starting with
SCH101 because it supplied the original review evidence.  Complex blocks may
use local net labels where a long wire would reduce clarity, but labels must no
longer substitute for showing the circuit's functional relationships.

# Project Shellac — SR-010 Annotation and Symbol Closure Rev A

## Objective

Close the two deterministic project-generation gaps identified after SR-009:

1. project-wide component annotation; and
2. resolution of every emitted schematic symbol without relying on an external KiCad library installation.

No analogue topology, component value, gain, replay characteristic, or control decision is changed by this revision.

## Annotation closure

All generated component references now:

- are unique across the complete nine-sheet hierarchy;
- use a conventional alphabetic prefix followed by a numeric identifier;
- are validated before any schematic file is written; and
- fail the build with an actionable diagnostic if a duplicate or invalid reference is introduced.

Legacy unit-style suffixes such as `U101A`, descriptive references such as `RBOND`, and cross-sheet test-point collisions have been replaced with deterministic numeric references.

## Symbol closure

The generated schematics now embed the minimal deterministic symbol definitions needed by the project for:

- resistors;
- capacitors;
- diodes;
- ferrite beads;
- three-pin and five-pin generic connectors; and
- the existing Project Shellac custom symbols.

The readiness audit checks every emitted symbol identifier against this embedded set.

## Renderer correction

The THAT1646 `SNS-` and `SNS+` pins now have distinct schematic coordinates. This corrects a renderer representation defect while preserving the validated electrical connection of each sense capacitor to its corresponding output leg.

## Validation evidence

- Python regression suite: 107 tests passed.
- Engineering Model: validation passed.
- Functional sheets: 8/8 CAD-ready.
- Root hierarchy: 8 child sheets, 66 hierarchical pins, 19 cross-sheet signals.
- KiCad 9 netlist export: passed.
- KiCad hierarchy: 9 sheets, 239 components, 82 nets.
- Duplicate references reported by KiCad netlist: zero.

KiCad electrical-rules checking remains open. Individual child-sheet ERC reports can be generated, but full hierarchical ERC currently terminates abnormally in the installed KiCad 9 command-line tool. Gate 2 therefore remains open until hierarchical ERC is made reliable and its findings are resolved.


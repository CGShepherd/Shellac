# SR-021A — Exact-Coordinate ERC Correction

**Trigger:** Native KiCad ERC dated 15 July 2026  
**Observed result:** 27 errors, 26 warnings  
**Scope:** renderer correction only

## Finding

The Python model was internally connected, but the KiCad serializer snapped
symbols, wires and labels independently. A small change in origin or endpoint
could therefore disconnect an otherwise valid named-pin connection.

## Correction

Child-sheet electrical entities are now written at the exact coordinates held
by the builder, to two-decimal KiCad precision. Junction detection uses the
same rendered precision.

The root schematic remains on its explicitly designed grid.

No analogue values or functional topology are changed.

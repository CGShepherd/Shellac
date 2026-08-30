# AE-022D — Exact Net-Conflict Closure

The remaining short is caused by the AE-022C pin-4 route crossing the vertical
0VA stub from LT5400 pin 5. AE-022D keeps pin 4 to the left of the package until
it reaches the Ux03 IN+ Y-level, then routes horizontally to IN+.

A reusable SCH101 net tracer is added so future named-net conflicts can be
diagnosed directly from connected components rather than inferred from pytest
output.

No electrical values or architecture decisions change.

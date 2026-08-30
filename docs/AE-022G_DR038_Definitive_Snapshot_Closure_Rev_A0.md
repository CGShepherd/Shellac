# AE-022G — DR-038 Definitive Snapshot Closure

Basis: full repository snapshot `6c9290e` on `temp/dr038-debug-snapshot`.

The repeated SCH101 conflict had two structural causes:

1. LT5400 right-side pins 5–8 share an X coordinate, while previous routing
   used vertical conductors along that pin column, necessarily passing through
   other semantic terminals.
2. The internal electrical audit did not model KiCad local-label equivalence,
   although the writer emits ordinary KiCad `(label ...)` objects.

The closure removes long LT5400 converter routes. Every functional terminal gets
only a short horizontal stub; intended nodes are expressed with same-name KiCad
local labels. `PRE_EQ_L/R` is used directly for the feedback/output node.

The electrical audit now unions identical local labels before checking conflicts
and termination, matching serialized KiCad schematic semantics.

No DR-038 electrical values, gain settings, physical footprint, or pin numbers
change in this closure.

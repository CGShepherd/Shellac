# SR-025B — Root-Hierarchy Physical-Net Closure

**Trigger:** SR-025A native ERC: 0 errors, 6 `label_multiple_wires` warnings  
**Scope:** root hierarchy only

## Root cause

The root sheet used one hidden local label at every hierarchical pin. Signals
with more than one endpoint therefore relied on repeated local labels to form
the net. KiCad regarded the connectivity as valid but warned that labels such
as +18V and 0VA resolved onto multiple separate conductors.

## Correction

Hierarchy endpoints are grouped by authoritative signal name.

- Signals with two or more endpoints are joined by deterministic physical
  point-to-point root wires.
- Signals with exactly one endpoint retain one outward stub and one hidden
  local label.
- Shared nets no longer use repeated local labels.

This makes the root connectivity explicit and removes the warning mechanism
instead of suppressing it.

## Design impact

None. The child sheets, hierarchical pin names, electrical topology, analogue
values, controls, grounding domains and power architecture are unchanged.

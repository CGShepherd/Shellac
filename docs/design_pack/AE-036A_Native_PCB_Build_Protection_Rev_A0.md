# AE-036A — Native PCB Build Protection

**Revision:** A0  
**Closes:** AE036-F01 immediate hazard  
**Status:** INTERIM OWNERSHIP PROTECTION

## Problem

The schematic generator's clean operation recursively deletes `out/kicad`,
which is also where the editor-owned native PCB currently lives.

## Interim correction

`clean_output()` is changed to preserve:
- `*.kicad_pcb`
- `*.kicad_dru`

while deleting/rebuilding generator-owned output.

Regression tests prove:
- a native PCB sentinel survives clean;
- generated schematic output is removed;
- native design-rule data survives.

## Long-term correction

This is an interim safety fix. Before production release, native PCB authority
should move to a dedicated source-controlled CAD directory and `out/` should
become fully disposable.

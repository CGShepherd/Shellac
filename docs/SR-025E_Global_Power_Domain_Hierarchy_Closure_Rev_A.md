# SR-025E — Global Power-Domain Hierarchy Closure

**Trigger:** SR-025D native ERC: 0 errors, 6 warnings  
**Scope:** hierarchy semantics for +18V, -18V, 0VA, and CHASSIS

## Root cause

Project-wide power domains were still represented as hierarchical sheet interfaces. KiCad then treated the repeated power pin names and global net joins as labels associated with multiple virtual wires on the root sheet.

## Correction

- +18V, -18V, 0VA, and CHASSIS are global labels in child sheets.
- These domains are omitted from child hierarchical labels.
- These domains are omitted from root sheet pins and stubs.
- The root hierarchy now carries only functional signal and control interfaces.

## Design impact

None. This is a CAD hierarchy correction only. The electrical nets, rail values, grounding domains, and functional circuitry are unchanged.

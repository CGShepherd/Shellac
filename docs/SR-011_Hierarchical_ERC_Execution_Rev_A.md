# Project Shellac — SR-011 Hierarchical ERC Execution Rev A

## Objective

Make KiCad 9 hierarchical electrical-rules checking execute reliably against the generated Project Shellac project and turn its output into deterministic engineering evidence.

No analogue topology, component value, gain, replay characteristic, or control decision changes in this revision.

## Corrections

- Root sheet-symbol instances now use the root schematic UUID as their KiCad parent path.
- Child symbols now use the complete root/sheet instance path.
- The root `sheet_instances` table contains only the root page, matching KiCad 9 hierarchy ownership.
- The generated project file includes the KiCad schematic project sections required by native ERC.
- Root sheet geometry and external wire endpoints are placed on the 2.54 mm schematic grid.
- Root sheet symbols include their standard simulation, BOM, board and DNP attributes.

## Automated evidence

`scripts/report_kicad_erc.py` runs native KiCad hierarchical ERC and reports violation counts by category. It writes the complete report to:

```text
out/kicad/ProjectShellac-erc.rpt
```

## Validation

- Python tests: 111 passed.
- Engineering Model: passed.
- CAD-ready functional blocks: 8/8.
- Native KiCad 9 netlist export: passed.
- Hierarchy: 9 sheets and 239 components.
- Native hierarchical ERC: completed without the previous process crash.

The isolated validation profile reported 1,456 findings. These are now a measurable renderer backlog rather than a failure of the ERC toolchain. Most are off-grid endpoints, unresolved library-table references, and the resulting disconnected-pin/wire reports. Gate 2 remains open while those findings are corrected.

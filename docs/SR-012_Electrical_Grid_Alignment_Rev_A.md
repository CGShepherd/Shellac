# Project Shellac — SR-012 Electrical Grid Alignment Rev A

## Objective

Remove coordinate-grid noise from native KiCad ERC so the remaining report identifies genuine renderer connectivity and library issues. No validated analogue decision changes in this revision.

## Implementation

The writer now snaps component origins, wire endpoints, local labels and hierarchical labels to KiCad's 1.27 mm connection grid. Tests verify deterministic, idempotent snapping across the generated project.

The ERC runner also retries once after a failed first invocation, handling an observed transient KiCad 9 startup failure without hiding a persistent error.

## Validation

113 tests passed. All eight blocks remain CAD-ready and native KiCad netlist/ERC execution succeeds. Off-grid endpoint findings fell from 688 to zero; total isolated-profile ERC findings fell from 1,456 to 766.

Gate 2 remains open for pin/wire connectivity and library-table closure.

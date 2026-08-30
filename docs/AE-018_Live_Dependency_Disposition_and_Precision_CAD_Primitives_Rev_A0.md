# AE-018 — Live Dependency Disposition for DR-038 / DR-039

**Revision:** A0  
**Base commit:** `e26ce0959e98a49be90468629ea55d2e3f616768`

AE-017 found 80 files and 505 token references. Most are not live migration
targets. This disposition separates the active change surface from retained
history and regenerated outputs.

## DR-038 live migration surface

### Must migrate atomically

- `generator/model/balanced_input.py`
- `generator/blocks/balanced_input.py`
- `generator/core/components.py`
- `generator/core/pins.py`
- `generator/writers/kicad9.py`
- `generator/layout/placement_clusters.py`
- `tests/test_balanced_input.py`
- `tests/test_balanced_input_gain.py`
- affected writer/pin/layout tests
- BOM/procurement entries created for the new precision network / service links

### Must be rerun / numerically updated

- `generator/model/signal_chain_analysis.py`
- `generator/model/sch101_precision_analysis.py`
- `generator/model/sch101_precision_candidate.py`
- `generator/model/signal_chain_noise_dc.py`
- AE-012 / AE-013 / AE-014 / AE-015 successor closure documents
- associated regression tests

### Retain as historical evidence

- AE-010 and earlier records describing the 3.48x implementation
- SR-006 DIP-switch closure
- AE-016A / AE-016B repair records
- proposed/superseded decision records

These documents are not rewritten merely because the active implementation moves.

### Regenerate, do not hand-edit

Everything under `out/` that contains the old SCH101 values or symbols.

## DR-039 live migration surface

### Must migrate atomically

- `generator/blocks/replay_eq.py`
- post-EQ test-point/reference allocation
- selected film-capacitor footprint and placement contract
- SCH103 human-readable/pin-connectivity tests
- SCH107 interface tests where POST_EQ enters the filter/bypass block
- BOM/procurement entries for C/R pair

### Must be rerun / numerically updated

- replay-curve response including the 0.48 Hz pole
- AE-012 headroom
- AE-015 DC/noise
- switching transient analysis
- startup/power-down analysis
- commissioning expectations

### Retain as historical evidence

- AE-004 and earlier SCH103 electrical closure
- AE-015 as the evidence that motivated DR-039
- AE-016 staging/repair history

### Regenerate, do not hand-edit

Generated KiCad, layout, PCB and commissioning artifacts under `out/`.

## New AE-018 physical primitive gate

Before changing active SCH101, the repository now freezes the LT5400-7 physical
connectivity contract:

- R1 = pins 1–8 = 5 kΩ
- R2 = pins 2–7 = 1.25 kΩ
- R3 = pins 3–6 = 1.25 kΩ
- R4 = pins 4–5 = 5 kΩ
- exposed pad = pin 9, electrically floating
- MS8E exposed-pad footprint must be verified rather than guessed

The next phase may add the actual project-local KiCad symbol/footprint binding
without changing the live SCH101 signal path. Only after that primitive passes
writer/pin tests should the atomic functional migration occur.

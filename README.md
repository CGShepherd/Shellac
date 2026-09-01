# Project Shellac

Project Shellac is an evidence-driven replay preamplifier design and generator project.

## Current controlled state

Development authority is maintained on the **`develop`** branch until a
production release is promoted to `main`.

- Implemented signal-chain baseline: **DR-037 / DR-038 / DR-039 / DR-040**
- Validated implementation commit: **`dce5c0e`**
- Production signal-chain analytical closure: **AE-023**
- Current documentation/design-pack reconciliation: **AE-024 / AE-025**
- Audio enclosure: **METCASE UNICASE 2 M5502119, black RAL 9005 — FROZEN**
- PSU enclosure: **METCASE UNICASE 2 M5502119, black RAL 9005 — FROZEN**
- PSU mains entry: **SCHURTER KMF1.1121.11 — FROZEN architecture**
- Final production PCB/mechanical release and prototype measured acceptance remain open.

## What is authoritative?

For the current design, read in this order:

1. `config/decisions/current_decision_index.yaml`
2. implemented source under `generator/`
3. `docs/knowledge/DESIGN_PACK_INDEX.md`
4. controlled BOM/procurement configuration
5. latest passing regression suite
6. current assurance/commissioning records

Historical AE, SR, G3 and migration documents remain engineering evidence but
do not override the authoritative current index.

## Build and validation

Run:

```text
python -m pytest
```

Normal build entry point:

```text
build_shellac.bat
```

## Production close-out

Before production release Shellac still requires prototype measured acceptance,
final PCB/mechanical closure, manufacturing release files, complete maintenance
documentation, a clean-clone reproducibility audit, repository hygiene, and a
tagged production baseline.

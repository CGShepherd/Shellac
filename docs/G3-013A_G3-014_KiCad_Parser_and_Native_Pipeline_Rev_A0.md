# G3-013A / G3-014 — KiCad PCB Parser Closure and Native Pipeline Baseline

## G3-013A parser correction

The Gate 3A review board failed at line 16 because the `Dwgs.User` and
`Cmts.User` layer declarations omitted KiCad's required numeric layer IDs.
They are now emitted as layers 40 and 41.

The board-skeleton validator now scans every declaration inside the `layers`
block and rejects any entry whose first token is not numeric.

## G3-014 architecture

The generated populated board remains a review prototype. Future PCB work uses
a KiCad-native ownership model:

- KiCad owns the `.kicad_pcb` document, native footprints, pads, nets, zones,
  routing and edit history.
- The Project Shellac engineering model owns footprint identity, proposed
  coordinates, clusters, placement authority, critical-net rules and keep-outs.
- `out/layout/kicad_native_pipeline.json` is the controlled placement-intent
  exchange artefact.

No manufacturing holes are frozen and critical analogue placements remain
subject to Gate 3A review.

## Commands

```cmd
python -m pytest
python scripts\build_populated_review_board.py
python scripts\report_kicad_native_pipeline.py
```

Open:

```text
out\pcb\ProjectShellac_Gate3A_Review.kicad_pcb
```

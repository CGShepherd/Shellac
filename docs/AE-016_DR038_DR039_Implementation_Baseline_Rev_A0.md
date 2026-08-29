# AE-016 — DR-038 / DR-039 Implementation Baseline

**Base commit:** `21a7bbe208147802e57de5be75157c7d5c326a86`

This update converts DR-038 and DR-039 into the controlled electrical baseline.

DR-038 preserves the 14/18/22 dB gain choices while moving SCH101 to a 4.000x
precision differential converter and 1 kΩ-scale gain ladder.

DR-039 inserts a 1 µF film / 330 kΩ common post-EQ DC block before the SCH107
filter/bypass split. Its nominal corner is ~0.48 Hz and its calculated loss at
20 Hz is below 0.01 dB.

The package intentionally does not invent a fake LT5400 CAD symbol. The
electrical model is now controlled; a single correct MSOP-8 LT5400 component
must be added in the next CAD-physicalisation gate.

## Apply

Run:

`APPLY_UPDATE.bat`

Then:

`python -m pytest`

and the normal Shellac build/ERC workflow.

## Remaining gate

- LT5400-7 symbol/footprint integration;
- physical precision service-link implementation;
- frequency-dependent CMRR with RF mismatch;
- switching/startup transient closure.

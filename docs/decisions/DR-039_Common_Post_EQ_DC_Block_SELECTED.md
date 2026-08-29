# DR-039 — Common post-EQ DC block

**Status:** SELECTED — CAD/DEPENDENCY MIGRATION PENDING

The selected electrical architecture remains:

- 1.0 µF non-polar film series capacitor per channel;
- 330 kΩ downstream bias resistor to 0VA;
- position immediately after SCH103 and before the SCH107 filter/bypass split;
- nominal corner approximately 0.48 Hz.

DR-039 is not yet substituted into the active SCH103 generator. It shall be
migrated atomically with the selected physical capacitor, schematic references,
placement implications, SCH103 tests/snapshots, replay-curve regression, and
switching/start-up transient tests.

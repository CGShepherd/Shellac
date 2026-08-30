# DR-039 — Common post-EQ DC block

**Status:** IMPLEMENTED  
**Implementation closure:** SR-039, 30 August 2026

The active SCH103 generator implements:
- 1.0 uF non-polar PET film series capacitor per channel;
- 330 kOhm downstream bias resistor to 0VA;
- position immediately after SCH103 recovery and before SCH107 FILTER/BYPASS;
- nominal calculated corner approximately 0.48 Hz;
- raw-EQ and post-block test points.

Active references are C360/R360 for the left channel and C410/R410 for the right channel.

Validation evidence:
- replay-curve and signal-chain regressions pass;
- 374 / 374 total Python tests passed;
- native KiCad ERC: 0 errors, 0 warnings.

This record supersedes the earlier migration-pending staging text.

# DR-038 — SCH101 precision architecture

**Status:** IMPLEMENTED  
**Implementation closure:** SR-039, 30 August 2026

The active SCH101 implementation is the selected 4.000x LT5400-7 /
low-impedance precision architecture.

Implemented controls:
- LT5400-7 A-grade matched network per channel;
- verified MS8E exposed-pad physical footprint;
- exposed pad represented and electrically no-connect;
- low-impedance precision gain legs;
- service-link population for LOW / DEFAULT / HIGH gain settings;
- ordinary DIP contacts removed from the precision feedback ratio;
- matched RF input geometry and tighter input passive tolerances.

Validation evidence:
- 374 / 374 Python regression tests passed;
- generated KiCad build completed;
- native KiCad ERC: 0 errors, 0 warnings.

This record supersedes the earlier migration-pending staging text.

# SR-040 update manifest

Base: develop commit `75732f3caf582ec580709496c9eb4669ac2eddfa`.

Adds:
- authoritative M5502119 audio mechanical datum freeze;
- deterministic 220 x 140 mm PCB outline and four mounting holes;
- full schematic-population BOM/footprint census;
- routing-readiness gate;
- critical-cluster placement CSV/JSON reports.

Run `APPLY_SR040.bat`.

SR-040 does not auto-accept manual-authority analogue cluster placement.
That remains the final human review before routing release.

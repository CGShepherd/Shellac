# DR-040 — Precision CAD primitive staging rule

**Status:** SELECTED  
**Date:** 29 August 2026

Before DR-038 changes the active SCH101 implementation, LT5400-7 shall exist as
a verified physical CAD primitive with:

- correct MS8E package;
- correct 1–8 / 2–7 / 3–6 / 4–5 resistor connectivity;
- exposed pad physically represented and electrically floating;
- verified pin-1 orientation;
- no guessed footprint binding.

Precision gain selection shall use hard service links/solder bridges, not an
ordinary DIP contact in the feedback ratio.

This staging decision exists to prevent another partial model/CAD migration.

# DR-040 — Precision CAD primitive staging rule

**Status:** IMPLEMENTED / SATISFIED  
**Date selected:** 29 August 2026  
**Closure:** SR-039, 30 August 2026

The staging rule required LT5400-7 to exist as a verified physical CAD primitive
before DR-038 could enter the active SCH101 implementation.

Closure evidence:
- correct MS8E package and standard KiCad footprint;
- correct resistor-terminal pin numbering;
- exposed pad physically represented and electrically no-connect;
- unique semantic schematic pin locations;
- no guessed footprint binding;
- service-link gain selection instead of ordinary DIP feedback contacts;
- primitive-level and whole-SCH101 regressions;
- native KiCad ERC 0 errors / 0 warnings.

The staging condition is now satisfied and remains a maintenance constraint.

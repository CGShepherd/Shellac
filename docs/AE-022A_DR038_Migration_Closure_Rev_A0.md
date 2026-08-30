# AE-022A — DR-038 Migration Closure

Closes the ten root causes from the first full DR-038 migration test run.

Key dispositions:
- LT5400 EP9 is intentionally floating and now explicitly marked no-connect.
- ERC tests now verify LT5400 pin-level converter wiring rather than removed
  discrete R130–R133/R230–R233 resistors.
- AE-013 is frozen as historical pre-DR038 assurance evidence.
- DEFAULT gain moved from 7.8996 to 7.9960 V/V (+0.105 dB). AE-012 preserves
  the old downstream margin criterion after compensating only for that deliberate
  gain increase.
- commissioning and connectivity regressions are migrated to the implemented
  topology.
- a stale-contract audit is generated for final review.

After a green suite, run the normal Shellac build/ERC. Next phase is full
generated-schematic review/freeze, then PCB layout.

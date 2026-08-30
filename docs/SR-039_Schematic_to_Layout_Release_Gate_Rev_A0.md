# SR-039 — Schematic-to-Layout Release Gate — Rev A0

## Executive disposition

Project Shellac's electrical/schematic design is **released for layout work**.

Validated baseline:
- 374 / 374 Python regression tests;
- successful generated KiCad project build;
- native KiCad ERC: **0 errors, 0 warnings**.

DR-037, DR-038, DR-039 and DR-040 are treated as implemented. The signal-chain
architecture is frozen for layout unless a new controlled defect is demonstrated.

## Released now

- SCH101 precision balanced front end with 4.000x LT5400-7 architecture.
- SCH103 complete replay EQ and DR-039 common post-EQ DC isolation.
- SCH107 rumble filter.
- SCH104 final gain.
- SCH105 channel-mode matrix.
- SCH108 balanced output and mute.
- SCH109 controls/interfaces.
- Four-layer analogue PCB architecture and critical-net policy.

## Not yet released

### Final routing
The active board-outline model still uses provisional mechanical datums.
Critical-cluster placement may proceed inside the conservative provisional
220 x 140 mm keep-in, but mounting holes, enclosure intrusion keep-outs and final
harness corridors must not be invented.

### Manufacturing
The controlled BOM remains a partial high-level baseline rather than a full
schematic-population procurement BOM. Manufacturing release therefore requires
exact identities, quantities, footprints and procurement state for the complete board.

## Layout-critical constraints

SCH101:
- preserve cartridge-pair symmetry through RF filtering;
- keep each LT5400 adjacent to its OPA1656 converter;
- PLUS_SUM / MINUS_SUM and PRE_EQ feedback/output nodes are manual, zero-via critical nets;
- no power/control copper through the cartridge or LT5400 summing region.

SCH103:
- C360/C410 1 uF DR-039 film capacitors and R360/R410 330 k bias resistors
  stay at the recovery-output / POST_EQ hand-off;
- timing/selector branches remain local to each channel;
- preserve physical separation between left and right EQ islands.

SCH107:
- frequency-setting passives remain tight to the OPA1656 stage.

SCH108:
- THAT1646 OUT/SNS loops remain direct, local and zero-via where practicable.

Power / ground:
- Inner-1 remains continuous 0VA.
- CHASSIS is not a signal-current return.
- ±18 V load returns must not traverse cartridge/EQ reference regions.

## Next phase

SR-040 is the **mechanical-datum + full-BOM + critical-placement closure**.
It should end with:
1. frozen board outline and mounting holes;
2. full keep-out map;
3. complete BOM/footprint/procurement reconciliation;
4. accepted placement of all critical analogue clusters;
5. routing release.

Once SR-040 closes, routing should start immediately.

# G3-015 — Gate 3A Macro-Placement Acceptance and CLU-106 Refinement

## Decision

The 220 mm x 140 mm board architecture and right-to-left functional flow were visually reviewed in KiCad and accepted as the Gate 3A macro-placement baseline.

This acceptance does not freeze detailed component coordinates, routing, zones, mounting holes, or enclosure datums.

## Observation closure

G3A-OBS-001 identified overlapping review geometry around the SCH106 power-entry cluster. Root cause was the generic capacitor constructor assigning an 0805 footprint to all capacitors, including C901 and C904 (470 uF rail reservoirs), combined with uniform-grid packing inside CLU-106.

Corrective action:

- capacitor construction now permits an explicit footprint while preserving the 0805 default;
- C901 and C904 use `Capacitor_THT:CP_Radial_D10.0mm_P5.00mm`;
- C902 and C905 use `Capacitor_SMD:C_1206_3216Metric`;
- CLU-106 has a controlled local placement map within its accepted macro-region;
- courtyard-envelope regression testing prevents renewed CLU-106 overlap.

## Gate status

- Macro architecture: provisionally accepted.
- CLU-106 local review geometry: corrected.
- Routing: not started.
- Manufacturing holes: not frozen.
- Exact native KiCad footprint/courtyard verification: still required during detailed population.

# SR-021D — ERC Branch-Topology Closure

**Parent baseline:** SR-021C  
**Scope:** targeted SCH101 and SCH105 connectivity correction  
**Electrical design changes:** none

## Native ERC evidence

The provenance-verified SR-021C build produced 16 errors and 14 warnings. All findings mapped to branch conductors in SCH101 and SCH105.

## Root cause

The affected branches used endpoint-on-segment T geometry. The branch endpoint and the through conductor shared the same coordinate, but the conductor was not split and no explicit junction was emitted. KiCad therefore treated the branch as open.

Automatic junction inference remains deliberately conservative; ordinary geometric crossings must never become connected silently.

## Correction

SCH101 routes each differential-converter branch directly between its source and destination pins, avoiding overlapping output, input and feedback conductors.

SCH105 routes each 2.2 MΩ bias resistor to the buffer input with a separate vertical approach, avoiding overlap with the switch signal conductor.

## Acceptance

- complete Python regression suite;
- engineering-model validation;
- internal electrical-integrity audit;
- deterministic hierarchical build and provenance verification;
- native KiCad hierarchical ERC on the user's Windows installation.

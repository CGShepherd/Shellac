# Project Shellac — SR-013 Pin Coordinate Contract Closure Rev A

## Objective

Align Foundry's semantic named-pin coordinates with KiCad's embedded-symbol coordinate system. No validated analogue decision changes in this revision.

## Correction

KiCad library-symbol Y coordinates use the opposite sign to generated sheet coordinates. The named-pin transform now applies that inversion before instance rotation. Rotation tests were corrected to the KiCad convention, and the panel LED contract was aligned with its actual embedded pin positions.

## Validation

113 tests passed. Native hierarchical ERC completed with 600 findings, reduced from 766. Pin-connectivity findings are now zero on SCH103, SCH104, SCH105, SCH107, SCH108 and SCH109.

The remaining 136 disconnected pins are confined to SCH101 and SCH106, the two sheets that predate the semantic named-pin API and still contain manual coordinate wiring. They are the next critical-path conversion targets.

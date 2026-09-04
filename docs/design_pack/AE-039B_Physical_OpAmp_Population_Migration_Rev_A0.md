# AE-039B — Physical Op-Amp Population Migration

**Revision:** A0  
**Parent:** AE-039A  
**Status:** PHYSICAL POPULATION MIGRATED — REAL PIN SYMBOL MIGRATION STILL OPEN

AE-039B migrates BOM/footprint/placement authority from logical amplifier
functions to the physical package allocation frozen by AE-039A.

Eight logical B-unit pseudo-packages no longer own independent footprints:

`U102 U202 U302 U352 U402 U502 U720 U770`

Physical board population therefore changes from 254 to **246**.

The op-amp physical census becomes:
- 6 × OPA1656;
- 2 × OPA1655;
- 2 × OPA1612.

Placement clusters now reference only physical packages. The absorbed logical
amplifier functions remain present in the generated schematic model but do not
receive separate PCB coordinates.

## Boundary

AE-039B does not yet convert the generated KiCad pseudo-symbols into real
multi-unit A/B op-amp symbols with physical SOIC-8 pin numbers.

Therefore routing remains held. AE-039C will close the final schematic/pin
semantics.

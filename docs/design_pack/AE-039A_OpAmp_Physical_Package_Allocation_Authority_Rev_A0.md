# AE-039A — Op-Amp Physical Package Allocation Authority

**Revision:** A0  
**Parent:** AE-038  
**Status:** ALLOCATION FROZEN — CAD MIGRATION PENDING

AE-039A freezes the logical-amplifier to physical-package allocation before
modifying KiCad generation, BOM population or placement authority.

## Frozen allocation

### SCH101
- U101A / U101B: OPA1656 — left positive/negative gain legs.
- U103: OPA1655 single — left LT5400 differential converter.
- U201A / U201B: OPA1656 — right positive/negative gain legs.
- U203: OPA1655 single — right LT5400 differential converter.

Historical logical U102 and U202 are absorbed as unit B of U101/U201.

### SCH103
- U301A / U301B: OPA1612 — left active LF EQ / recovery.
- U351A / U351B: OPA1612 — right active LF EQ / recovery.

Historical logical U302/U352 become B units.

### SCH104
- U401A / U401B: OPA1656 — left/right isolation buffers.

Historical U402 becomes U401B.

### SCH105
- U501A / U501B: OPA1656 — left/right mode buffers.

Historical U502 becomes U501B.

### SCH107
- U700A / U700B: OPA1656 — left HP sections A/B.
- U750A / U750B: OPA1656 — right HP sections A/B.

Historical U720/U770 become B units.

## Physical census

- 6 × OPA1656 dual SOIC-8
- 2 × OPA1655 single SOIC-8
- 2 × OPA1612 dual SOIC-8

Total: **10 physical packages, 18 used amplifier channels, zero unused halves.**

## Future population effect

Once AE-039B migrates the physical CAD, eight historical pseudo-package
references disappear from board/BOM population:

`U102 U202 U302 U352 U402 U502 U720 U770`

The current 254-item board population is therefore expected to reduce by eight
to **246 physical PCB items**, assuming no unrelated simultaneous ECO.

That numeric forecast is a migration check, not a new permanent hard-coded
population invariant.

## Pin authority

For OPA1656/OPA1612 SOIC-8 dual packages:

- unit A: OUT 1, -IN 2, +IN 3;
- V- 4;
- unit B: +IN 5, -IN 6, OUT 7;
- V+ 8.

For OPA1655 SOIC-8 single:
- -IN 2;
- +IN 3;
- V- 4;
- OUT 6;
- V+ 7;
- NC 1, 5, 8.

## Implementation boundary

AE-039A intentionally changes no existing schematic-builder references and no
PCB population. AE-039B must migrate the writer and downstream physical models
atomically so a half-migrated generator cannot be mistaken for production CAD.

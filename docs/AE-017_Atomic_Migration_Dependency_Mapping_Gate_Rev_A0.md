# AE-017 — Atomic Migration Dependency-Mapping Gate

**Revision:** A0  
**Status:** MIGRATION PREPARATION  
**Date:** 29 August 2026  
**Base commit:** `6d34fa0b6c808b541576b79f6f1ba6b8313c6fad`

## Purpose

AE-016 demonstrated that DR-038 and DR-039 cannot safely be inserted by changing
one central model or one schematic block in isolation. The regression suite is
doing its job: it encodes both the electrical baseline and the rendered CAD
contracts.

AE-017 therefore creates a read-only dependency mapper before the next atomic
migration.

## Known hard contracts already verified

SCH101 currently has at least two independent classes of frozen contract:

1. numerical — the active test suite explicitly requires a 3.48x differential
   converter and the established 14/18/22 dB gain settings;
2. rendered CAD — tests explicitly require `SW1011`, `R112`, `R113`, `R114`
   and the current 4420 / 8280 / 21680 resistor segmentation.

SCH103 has a separately frozen replay-EQ transfer-function topology. DR-039 must
therefore be added without accidentally changing the historical/RIAA curve
contracts.

## Workflow

After extracting this package at repository root:

`python tools/ae017_dependency_map.py`

This creates:

`docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md`

Then run:

`python -m pytest`

The scanner is read-only except for the generated markdown report.

## Required next decision gate

Do not implement DR-038/DR-039 until the generated map has been reviewed and
every matched file has one of four dispositions:

- migrate;
- regression update because the design requirement genuinely changed;
- retain unchanged;
- historical/documentation only.

This prevents a second partial-baseline migration.

## Migration order after the map is closed

1. physical component and footprint contracts;
2. SCH101/SCH103 CAD builders;
3. electrical models;
4. BOM/procurement;
5. affected direct tests;
6. rendered schematic/geometry tests;
7. full replay curve;
8. headroom;
9. noise/CMRR/DC;
10. switching/power transient closure.

Only then should the active design be declared migrated.

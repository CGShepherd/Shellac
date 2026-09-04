# AE-038 — Dual Op-Amp Package / Unit Audit

**Revision:** A0  
**Closes analysis of:** AE036-F03  
**Status:** IMPLEMENTATION REQUIRED

## Executive result

The current generator represents each amplifier function as an independent
SOIC-8-footprinted pseudo-symbol. That is electrically convenient but physically
wrong for dual devices.

Current functional amplifier count:

| Sheet | Device family | Functional channels | Current pseudo-footprints | Correct physical package plan |
|---|---:|---:|---:|---:|
| SCH101 | OPA165x | 6 | 6 | 4 |
| SCH103 | OPA1612 | 4 | 4 | 2 |
| SCH104 | OPA1656 | 2 | 2 | 1 |
| SCH105 | OPA1656 | 2 | 2 | 1 |
| SCH107 | OPA1656 | 4 | 4 | 2 |
| **Total** |  | **18** | **18** | **10** |

The present CAD therefore overstates the op-amp package population by **8 SOIC-8
packages**.

## Recommended physical allocation

### SCH101

Per channel:

- one OPA1656 dual package:
  - unit A = positive-leg gain amplifier;
  - unit B = negative-leg gain amplifier;
- one OPA1655 single package:
  - differential converter adjacent to the channel's LT5400 network.

Thus SCH101 uses:
- 2 × OPA1656 dual;
- 2 × OPA1655 single.

This is preferred to using one OPA1656 for both left and right differential
converters. Cross-channel pairing would reduce package count by one but would
force one or both LT5400/converter loops to become physically non-local, violating
the routing/locality authority established by SR-041.

Using the OPA1655 for the converter is electrically conservative: OPA1655 and
OPA1656 are the single- and dual-channel members of the same OPA165x family with
the same published core performance, and both are available in TI's 8-pin SOIC D
package.

### SCH103

One OPA1612 dual package per channel:
- unit A = active LF EQ;
- unit B = recovery amplifier.

Total: 2 × OPA1612.

### SCH104

One OPA1656 dual:
- unit A = left isolation buffer;
- unit B = right isolation buffer.

Total: 1 × OPA1656.

### SCH105

One OPA1656 dual:
- unit A = left mode buffer;
- unit B = right mode buffer.

Total: 1 × OPA1656.

### SCH107

One OPA1656 dual per channel:
- unit A = first Sallen-Key section;
- unit B = second Sallen-Key section.

Total: 2 × OPA1656.

## Final package census

- OPA1656 dual SOIC-8: **6 packages / 12 used amplifier channels**
- OPA1655 single SOIC-8: **2 packages / 2 used amplifier channels**
- OPA1612 dual SOIC-8: **2 packages / 4 used amplifier channels**

Total:
- **10 physical op-amp IC packages**
- **18 active amplifier channels**
- **0 unused amplifier halves**

## Why OPA1655 is preferable to an unused OPA1656 half in SCH101

An alternative is one OPA1656 package per differential converter with its second
half unused. That would retain 10 packages but create two unused amplifier
channels requiring explicit stable termination.

OPA1655 avoids:
- unused-half stability rules;
- unnecessary active silicon/current ambiguity;
- misleading package/channel accounting.

It also preserves the exact local physical topology around each LT5400.

## Current generator defects to fix

1. `Component` has no concept of physical-package identity distinct from
   functional symbol identity.
2. `symbol_instance()` always emits `(unit 1)`.
3. pseudo-op-amp symbols use conceptual five-pin contracts rather than actual
   OPA1656/OPA1612 A/B pin numbers.
4. each pseudo-symbol carries its own SOIC-8 footprint.
5. footprint/BOM/placement models therefore count functional channels rather than
   physical packages.
6. supply pins are duplicated per pseudo-symbol rather than represented once per
   real package.

## Required implementation

The implementation increment should add an explicit package/unit abstraction:

- physical package reference, e.g. `U101`;
- functional unit, e.g. `A`, `B`, or `single`;
- device MPN/family;
- real pin mapping;
- footprint emitted once per physical package;
- BOM count emitted once per physical package;
- placement proposal emitted once per physical package;
- shared V+/V- represented at package level;
- schematic instances retain separate visible amplifier units.

Recommended real SOIC-8 dual pin map for OPA1656/OPA1612:
- A: OUT=1, -IN=2, +IN=3;
- V-=4;
- B: +IN=5, -IN=6, OUT=7;
- V+=8.

Recommended OPA1655 SOIC-8 single map:
- -IN=2;
- +IN=3;
- V-=4;
- OUT=6;
- V+=7;
- pins 1,5,8 NC.

## Routing status

Further production routing remains held until this package/unit implementation is
complete and the regenerated physical population passes ERC, placement and
footprint audits.

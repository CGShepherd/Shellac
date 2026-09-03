# AE-032 — Four-Layer Native Routing Preparation

**Revision:** A0  
**Status:** ROUTING CONTRACT — native PCB modification follows separately

## Purpose

AE-032 converts the SR-041 / SR-043 routing intent into a concise production
routing contract before the native KiCad board is modified.

This is intentionally separated from actual routing. The purpose is to freeze
the rules first, then route against them.

## Layer stack intent

| Layer | Role |
|---|---|
| F.Cu | Components and short/local signal routing |
| In1.Cu | Substantially continuous 0VA analogue reference plane |
| In2.Cu | Power-rail distribution / rail spine |
| B.Cu | Secondary signal routing and local returns where necessary |

In1.Cu is the primary electromagnetic return reference and must not be treated as
a convenient routing layer.

## Critical manually routed groups

The following remain manual-routing-only:

1. cartridge input differential pair;
2. SCH101 RF/common-mode network;
3. LT5400 precision ratio connections;
4. SCH101 gain feedback/service-link paths;
5. SCH103 EQ timing networks;
6. SCH105 channel summing/mode paths;
7. SCH108 THAT1646 balanced output pair.

## Routing rules

- no precision/high-impedance route crosses an In1.Cu discontinuity;
- input pair geometry remains closely matched;
- LT5400 loops remain short/local with minimum unnecessary via use;
- EQ timing loops remain compact;
- local supply decoupling uses minimum loop area;
- THAT1646 output legs remain geometrically symmetric;
- current-heavy rail distribution is kept off the reference plane;
- In2.Cu rail routing must not compromise sensitive-node shielding/return paths;
- autorouting is prohibited on critical analogue groups;
- only SR-041-authorised local placement refinement is permitted.

## Explicit hold regions

The following remain unfinalised pending Lorlin PT sample/MPN closure:

- Bass rotary footprint/fanout;
- Treble rotary footprint/fanout;
- Channel rotary footprint and second-wafer keep-out;
- top-cover rotary drilling datum.

These holds should not prevent routing of the rest of the board.

## Routing sequence

Recommended order:

1. configure/verify 4-layer stack;
2. establish uninterrupted In1.Cu reference plane;
3. define In2.Cu rail-spine corridors;
4. route SCH101 cartridge input and precision network;
5. route EQ-local networks up to the rotary hold boundary;
6. route SCH105 mode-matrix local analogue paths;
7. route THAT1646 outputs;
8. complete remaining low-risk signal routes;
9. complete power distribution;
10. finalise rotary regions after AE-027/AE-028;
11. pour/repour planes and inspect return paths;
12. run DRC/ERC plus manual analogue-layout review.

## Release condition

AE-032 does not claim the PCB is fabrication-ready. Fabrication release requires
the actual native board to satisfy this contract, pass DRC/ERC and undergo
Gerber/drill/plane review.

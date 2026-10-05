# DR-038 — SCH101 precision architecture

**Status:** CURRENT ARCHITECTURE — QUALIFICATION OPEN
**Historical implementation closure:** SR-039, 30 August 2026
**Current reconciliation:** AE-075B + AE-076C

## Current implemented authority

- exact network `LT5400BIMS8E-7#PBF`, B grade, option -7;
- exposed pad 9 bonded to quiet `0VA`;
- low-impedance precision gain legs;
- live gain programming uses `TSW-104-07-G-D` + `MNT-104-BK-G`;
- approximate 14 / 18 / 22 dB gain, with no LOW/HIGH bridge as the complete approximately 18 dB default;
- main PCB retains 23.7 kOhm per leg to 0VA (~47.4 kOhm differential), fixed 47 pF/leg to CHASSIS and matched 100 Ohm RF isolation.

The original A-grade/floating-EP statements are superseded provenance.

## AE-076C selected-next cartridge-capacitance architecture

The previous live H120/H121/H122 ganged L/R load-shunt implementation is superseded as the selected architecture but remains present in the live generator until controlled migration.

- two identical tiny passive cards, one local to each channel;
- cartridge signal path does not pass through the card;
- each card is only a differential shunt;
- main socket `SLW-102-01-G-D`, card header `TSW-102-07-G-D`;
- duplicate each node on a diagonal contact pair so 180-degree insertion is electrically benign;
- no card = BASE and fail-safe;
- matched L/R +47 pF and +100 pF service pairs;
- service selection uses cartridge plus measured cable capacitance, not cartridge name alone;
- optional development-card resistor footprints may exist but are DNP by default;
- gain programming remains separate.

## Qualification still open before routing

1. RUN10 complete-stage tolerance/CMRR and 20 kHz parasitics;
2. retained MNT-104 gain-shunt pairing/orientation;
3. exact SLW/TSW footprint/MCAD stack;
4. controlled SCH101/native migration from H120/H121/H122 to H120/H220 personality sockets;
5. RUN10 personality-interface capacitance and L/R matching;
6. bench correlation.

No routing, layout freeze, BOM freeze or manufacturing release is authorised.

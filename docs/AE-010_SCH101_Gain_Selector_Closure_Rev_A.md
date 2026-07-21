# Project Shellac — AE-010 SCH101 Gain-Selector Closure

**Revision:** A  
**Status:** electrically closed  
**Date:** 14 July 2026

## 1. Issue resolved

The live SCH101 builder previously showed a fixed 4× gain on each balanced leg
followed by a fixed 3.48× differential converter. That implied 13.92× total
gain, or 22.87 dB, while all downstream overload calculations used 7.94×
(approximately 18 dB).

AE-010 removes that inconsistency and implements the previously agreed internal
gain selection.

## 2. Frozen architecture

The existing topology is retained:

1. floating cartridge input and RF filtering;
2. matched OPA1656 non-inverting gain on each balanced leg;
3. fixed 3.48× precision differential converter;
4. single-ended `PRE_EQ_L/R` output.

Only the OPA1656 feedback resistor is selected.

## 3. Gain settings

Each gain leg uses 10.0 kΩ from the inverting input to the local reference.

| Setting | Feedback resistor | Per-leg gain | Complete SCH101 gain | Realised |
|---|---:|---:|---:|---:|
| Low | 4.42 kΩ | 1.442× | 5.018× | 14.01 dB |
| Default | 12.7 kΩ | 2.270× | 7.900× | 17.95 dB |
| High | 26.1 kΩ | 3.610× | 12.563× | 21.98 dB |

The default setting is within 0.05 dB of the 18 dB gain used by SCH103 and
output-headroom calculations.

## 4. Internal selector

An eight-way DIP bank provides two selection bits for each of the four gain
legs:

- left positive;
- left negative;
- right positive;
- right negative.

The same two-bit pattern must be repeated on all four legs:

| Setting | Pattern per leg |
|---|---|
| Low | 00 |
| Default | 01 |
| High | 10 |
| Reserved | 11 |

The reserved state shall not be used. The operating instructions and PCB
silkscreen must show the repeated four-leg patterns clearly.

This approach preserves the agreed internal DIP philosophy. It is a bench-set
control, not a front-panel control.

## 5. Matching requirement

Gain equality between the positive and negative legs directly affects
common-mode rejection and differential accuracy. Use 0.1% resistors, with
matched networks preferred where affordable. After assembly, verify all four
leg gains before connecting the cartridge.

## 6. Acceptance tests

- all four legs set to the same pattern;
- Low, Default and High total gains within ±0.1 dB of target;
- left/right gain difference below 0.05 dB;
- positive/negative leg gain difference below 0.05 dB;
- no oscillation at any gain;
- input-referred noise and DC offset recorded at each setting.

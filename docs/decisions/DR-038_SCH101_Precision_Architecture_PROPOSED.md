# DR-038 — Proposed SCH101 precision architecture

**Status:** PROPOSED — awaiting owner acceptance  
**Date:** 29 August 2026  
**Evidence:** AE-013, AE-014

## Decision proposed

Adopt a 4.00x precision differential converter and lower-impedance selectable
gain legs while preserving the established 14/18/22 dB total SCH101 gains.

Preferred differential network: LT5400-7 A-grade, 1.25 kΩ / 5 kΩ.

Candidate gain ladder per leg:
- Rg 1.000 kΩ
- base RF 249 Ω
- DEFAULT addition 750 Ω
- HIGH addition 1.91 kΩ

Require 0.01%-class relative matching across corresponding gain-leg elements.

## Rationale

This simultaneously:
- removes the tolerance-limited CMRR weakness identified by AE-013;
- reduces SCH101 resistor noise by roughly 6 dB;
- uses a catalogue precision difference-amplifier ratio;
- preserves system gain/headroom assumptions to within 0.07 dB.

## Conditions before CLOSED status

- exact gain-resistor technology selected;
- selector contact resistance included in corner model;
- RF-input pair matching included in frequency-dependent CMRR model;
- AE-012 headroom regression passes;
- ≥70 dB 20 Hz–1 kHz and ≥60 dB at 20 kHz CMRR requirements accepted or revised.

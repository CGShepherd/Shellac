# DR-039 — Proposed common post-EQ DC block

**Status:** PROPOSED  
**Date:** 29 August 2026  
**Evidence:** AE-015

## Proposed decision

Add one first-order DC-blocking network per channel immediately after SCH103 and
before the SCH107 filter/bypass split.

Initial values:
- C = 1.0 µF film
- R = 330 kΩ to 0VA
- fc ≈ 0.48 Hz

## Rationale

The non-flat SCH103 active LF stage has approximately 38x DC noise gain.
Conservative independent offset maxima can therefore propagate to multi-volt
differential DC at the XLR when SCH107 is bypassed.

A common post-EQ AC block removes both SCH101 and SCH103 static offset in both
rumble-filter states while adding less than 0.01 dB loss at 20 Hz.

## Conditions before CLOSED

- film capacitor physical down-selection;
- replay-curve regression;
- startup/power-down transient test;
- mute and rumble-switch transient test;
- downstream DC verification.

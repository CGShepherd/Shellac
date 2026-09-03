# Project Shellac — Prototype Commissioning Acceptance Matrix

**Authority:** AE-029  
**Status:** FIRST-HARDWARE ACCEPTANCE PLAN

Use this as the commissioning sequence for the first representative audio PCB.

## Stage 0 — Visual / unpowered

- verify component orientation and values;
- verify LT5400 orientation and exposed-pad implementation;
- verify gain service links;
- verify DR-039 film capacitors;
- verify switch wiring/PCB terminals;
- verify continuity of 0VA and chassis strategy;
- resistance check from each rail to 0VA before applying power.

## Stage 1 — Power only / MUTE engaged

- current-limited bench supply first;
- verify ±17 V nominal regulated rails at audio PCB;
- inspect current draw;
- verify no device heating;
- measure output DC;
- scope power-up transient;
- retain MUTE for >=2 s.

## Stage 2 — DC / idle

- record DC at defined test points;
- verify balanced output differential DC <=25 mV provisional;
- repeat FILTER and BYPASS;
- repeat all channel modes.

## Stage 3 — Flat-path functional signal

Inject low-level balanced 1 kHz source.

Verify:
- LOW / DEFAULT / HIGH gains;
- L/R tracking;
- Stereo;
- Dual Left;
- Dual Right;
- Mono average;
- output balance.

## Stage 4 — Equalisation

With DEFAULT gain:
- verify FLAT;
- sweep each Bass position;
- sweep each Treble position;
- verify True RIAA;
- normalise curves at 1 kHz;
- apply AE-029 tolerances.

## Stage 5 — Rumble filter

Measure FILTER/BYPASS at:
5, 10, 15, 20, 30, 100, 1000 Hz.

## Stage 6 — CMRR

Common-mode injection at:
20, 100, 1k, 10k, 20k Hz
for LOW / DEFAULT / HIGH.

## Stage 7 — Noise

Inputs correctly terminated:
- DEFAULT / True RIAA;
- FILTER;
- BYPASS;
- unweighted 20 Hz–20 kHz RMS;
- save spectrum.

## Stage 8 — Overload

Sweep input level to onset of compression/clipping at:
20, 50, 100, 1k, 10k, 20k Hz
for representative worst-case EQ states and all gain settings.

## Stage 9 — Switching / transient

Scope:
- MUTE;
- Rumble;
- Bass;
- Treble;
- all Channel transitions;
- cold/warm power-up;
- power-down.

## Stage 10 — Return-to-service subset

After any repair:
- rail/DC check;
- DEFAULT 1 kHz level;
- RIAA spot/sweep;
- noise;
- channel modes;
- output DC;
- mute/transient sanity check.

# Project Shellac — AE-008 SCH108 Balanced Output and Mute

**Revision:** A  
**Status:** electrically closed  
**Date:** 14 July 2026

## 1. Integrated gain correction

THAT1646 provides a fixed 2× (+6.021 dB) gain from its single-ended input to
its differential output. To preserve the intended complete signal-chain gain,
SCH104 is revised from 2× to a unity OPA1656 isolation buffer.

The integrated result is unchanged:

| Condition | SCH104 output | XLR differential output |
|---|---:|---:|
| Nominal | 0.321 V RMS | 0.642 V RMS |
| Severe | 3.21 V RMS | 6.42 V RMS |

This avoids a default 46 dB signal chain and avoids an imprecise passive
attenuator at the 5 kΩ THAT1646 input.

## 2. Output driver

One THAT1646 SOIC-8 device is used per channel on ±18 V rails.

Relevant design characteristics:

- +6 dB differential gain;
- floating transformer-like balanced output;
- short-circuit-protected outputs;
- stable into long and capacitive cables;
- approximately 50 Ω output impedance per leg;
- high output capability;
- low noise and distortion.

A conservative 10 V RMS differential design ceiling is retained. The severe
6.42 V RMS case has more than 3.8 dB margin.

## 3. Mechanical mute

A stereo 2PDT break-before-make toggle switches both THAT1646 inputs between:

- MODE_L / MODE_R; and
- 0VA.

The line-driver outputs remain connected to the XLRs. Muting at the inputs
avoids shorting the active balanced outputs.

## 4. Common-mode offset

Fit two 10 µF high-quality non-polar capacitors in each THAT1646 sense path,
following the manufacturer's common-mode offset reduction circuit.

These capacitors are part of the common-mode feedback path, not series audio
coupling capacitors.

## 5. Connector and protection

Each output leg includes:

- one ferrite bead;
- one 100 pF C0G capacitor to CHASSIS at the connector;
- one 1N4004 clamp to +18 V;
- one 1N4004 clamp to -18 V.

The protection follows THAT's recommended RFI and phantom-discharge scheme.

XLR wiring:

- pin 1: CHASSIS;
- pin 2: hot/+;
- pin 3: cold/-.

The connectors are full-size panel-mounted male XLRs wired by internal
star-quad; they are not PCB-mounted.

## 6. Decoupling

Per THAT1646:

- 100 nF from +18 V to 0VA;
- 100 nF from -18 V to 0VA;
- 10 µF local bulk capacitance on each rail.

The 100 nF parts shall be placed close to the IC pins.

## 7. Verification

- differential gain 2.000× within device tolerance;
- nominal output approximately 0.642 V RMS for 0.321 V RMS input;
- clean differential output at 6.42 V RMS;
- mute attenuates both channels without unstable or floating inputs;
- output DC common-mode and differential offsets recorded;
- stable operation into the intended cable and Pre90 input;
- pin-1/chassis and RFI network continuity confirmed.

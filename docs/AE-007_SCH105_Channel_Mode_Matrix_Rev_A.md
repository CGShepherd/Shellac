# Project Shellac — AE-007 SCH105 Channel Mode Matrix

**Revision:** A  
**Status:** electrically closed  
**Date:** 14 July 2026

## 1. Required modes

| Position | Left output | Right output |
|---|---|---|
| Stereo | L | R |
| Dual Left | L | L |
| Dual Right | R | R |
| L+R Mono | (L+R)/2 | (L+R)/2 |

The L+R mode uses arithmetic averaging rather than addition without
attenuation. Equal correlated left and right signals therefore retain their
original level instead of increasing by 6 dB.

## 2. Trade decision

A passive resistor matrix alone was rejected because its output impedance
would change substantially between direct and summed modes.

Relay routing was rejected because it added coils, drivers, supply-current
transients and control complexity without a material performance advantage.

A simple 2P4T selector with a permanently connected averaging network was
rejected because the averaging resistors would form a continuous bridge
between left and right channels in stereo mode.

The approved solution is:

- one mechanically linked 4P4T break-before-make rotary switch;
- two poles for output-source selection;
- two poles that connect the left/right summing branches only in L+R mode;
- one dual OPA1656 unity buffer after the switch.

## 3. Component values

| Item | Value |
|---|---:|
| Left summing resistor | 4.70 kΩ, 0.1% |
| Right summing resistor | 4.70 kΩ, 0.1% |
| Buffer-input bias resistor | 2.20 MΩ per output, 1% |
| Output isolation | 100 Ω per channel |
| Buffer | OPA1656, dual SOIC-8 |
| Supply | ±18 V |

The mono averaging node has a nominal source impedance of 2.35 kΩ. Loading by
the two 2.20 MΩ buffer-input bias resistors causes less than 0.03 dB level
error for equal inputs.

## 4. Switching behaviour

The switch shall be break-before-make. During contact transition, each buffer
input is held near 0VA by its 2.20 MΩ resistor rather than floating.

The switch truth table is fixed as follows:

| Position | Pole A | Pole B | Pole C | Pole D |
|---|---|---|---|---|
| Stereo | L | R | Open | Open |
| Dual Left | L | L | Open | Open |
| Dual Right | R | R | Open | Open |
| L+R Mono | Mono node | Mono node | L to 4.7 kΩ | R to 4.7 kΩ |

## 5. Headroom and noise

The unity buffers do not increase signal level. A severe 6.42 V RMS input
therefore retains approximately 3.85 dB margin to the conservative 10 V RMS
internal design ceiling.

The parallel 4.7 kΩ summing resistors have a 2.35 kΩ Thevenin resistance and
contribute approximately 6.2 nV/√Hz thermal-noise density at 300 K. Because
SCH105 follows the complete preamplifier gain, this contribution is negligible
relative to programme level.

## 6. Layout and verification

- Keep the summing resistors and switch-return conductors short.
- Route left and right direct paths symmetrically.
- Place 100 nF decouplers at the OPA1656 supply pins.
- Provide 10 µF nearby bulk decoupling per rail.
- Verify all four truth-table states using independent left/right tones.
- Verify mono cancellation with equal antiphase signals.
- Verify no measurable crosstalk through the mono network in stereo mode.

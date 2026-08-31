# Project Shellac — Signal-Chain Commissioning and Maintenance Baseline

**Status:** PRE-PRODUCTION MAINTENANCE BASELINE  
**Evidence:** DR-037, DR-038, DR-039, AE-012 through AE-023

## Normal configuration

- SCH101 gain: DEFAULT / approximately 18 dB.
- HIGH gain is reserved for lower-output cartridges and has reduced low-frequency headroom.
- Rumble filter may be FILTER or BYPASS; DR-039 provides DC isolation in both states.
- Full RIAA replay uses TRUE RIAA 3180/318 us bass plus 2121 Hz treble.

## Power sequencing

The DR-039 1 µF / 330 kΩ network has a time constant of approximately 0.33 s.

For commissioning and conservative operation:

1. engage MUTE before applying or removing power;
2. apply power;
3. allow at least 2 s before releasing MUTE;
4. before power-down, engage MUTE first.

Two seconds corresponds to more than six DR-039 time constants and leaves less
than 0.3% of an initial post-EQ DC-block charging transient.

This is an operating/commissioning recommendation, not an automatic timing
function; Shellac retains its mechanical mute philosophy.

## Expected nominal level

At DEFAULT gain with a 5 mV RMS cartridge reference and complete RIAA, the
balanced XLR output around 1 kHz is approximately 0.65 V RMS differential.

## Headroom

The conservative Shellac design ceiling remains 10 V RMS differential.

- DEFAULT retains useful wanted-band headroom at the 5 mV reference.
- HIGH is valid but is a lower-output-cartridge sensitivity setting and should
  not be used merely to obtain a louder output.

## CMRR commissioning targets

With a symmetrical low-impedance test source:

- >=70 dB, 20 Hz to 1 kHz, at LOW/DEFAULT/HIGH;
- >=60 dB at 20 kHz.

The production tolerance model includes RF-series resistor, common-mode
capacitor, gain-leg and LT5400 ratio errors.

## DC offset

With DR-039 fitted, upstream SCH101/SCH103 static offset is blocked before the
rumble FILTER/BYPASS split.

A conservative analytical downstream differential DC limit is approximately
20 mV. A tighter measured production acceptance value should be frozen after
prototype data exists.

## Electronics noise

The current first-order complete-RIAA electronics model predicts an output
noise of order 0.1 mV RMS and electronics SNR in the mid-70 dB range against
the nominal output. 78-rpm record/surface noise will normally dominate.

## Service caution

Do not substitute an ordinary DIP switch into the SCH101 precision feedback
path. LOW/DEFAULT/HIGH are hard service-link configurations and all
corresponding gain legs must be configured identically.

# AE-058 — LTspice 26 Correlation Compatibility and Numerical Closure — Rev A2

## Status
Pre-SPICE design-assurance evidence. Not manufacturing baseline authority.

## Numerical closure corrections

### Matrix analytical correlation
The AE-055 matrix arithmetic represents an ideal unloaded equal-resistor average.
The initial LTspice fixture included a 1 GΩ shunt from the averaging node to
ground as a defensive convergence aid. The node is already fully DC-defined by
the two 4.7 kΩ source legs, so that shunt is unnecessary and changes the quantity
being correlated.

Its finite loading produced the observed approximately 2.35 ppm attenuation:
- ideal equal-input output: 1.0
- simulated with 1 GΩ shunt: approximately 0.99999765

The shunt is therefore removed. The strict matrix tolerance is retained.

### DR039 cutoff correlation
At 200 points/decade, LTspice crossing interpolation differed from the exact
analytical 1/(2*pi*R*C) result by approximately 7.3 microhertz. The independent
20 Hz attenuation metric already agreed within the existing tolerance.

Rather than widening the cutoff criterion, the AC sweep density is increased
from 200 to 2000 points/decade. This maintains the numerical acceptance contract
while reducing interpolation error at negligible computational cost for this
single-pole fixture.

## Assurance judgement
These changes modify only the correlation fixtures and numerical resolution.
They do not alter DR039 implementation authority, SCH101 architecture, matrix
hardware values, AE-049 system acceptance limits, or the intended integrated
SHELLAC_TOP model.

# Project Shellac — SR-004 SCH107 Pin-Aware Conversion

**Revision:** A  
**Status:** SCH107 CAD-ready  
**Date:** 14 July 2026

## Scope

This increment converts SCH107 from a component-placement representation into
an electrically connected KiCad sheet.

## Connectivity implemented

Per channel:

- POST_EQ input net;
- two explicit unity-gain Sallen-Key high-pass sections;
- both capacitor junctions;
- feedback resistor from first junction to section output;
- shunt resistor from second junction to 0VA;
- OPA1656 input, output, +18 V, -18 V and 0VA pins;
- inter-stage net;
- 100-ohm filtered-output isolation resistor;
- direct and filtered bypass branches;
- input, first-stage, second-stage and final-output test points;
- local 100 nF and 10 µF rail decoupling.

The stereo 2P2T bypass selector is represented by a deterministic six-pin
custom symbol with named direct, filtered and output pins for both channels.

## Readiness consequence

SCH107 now has pin-level wiring and all custom symbols emitted by the sheet are
embedded by the writer. It therefore passes the block-level CAD-readiness gate.

The project-level gate remains open until all remaining blocks and the root
hierarchy are complete.

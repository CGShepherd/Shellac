# Project Shellac — SR-005 SCH108 Pin-Aware Conversion

**Revision:** A  
**Status:** SCH108 CAD-ready  
**Date:** 14 July 2026

## Scope

SCH108 is converted from a functional component layout into an explicit
pin-connected output schematic.

## THAT1646 connectivity

The custom symbol follows the official SOIC-8 pinout:

1. OUT-
2. SNS-
3. GND
4. IN
5. VEE
6. VCC
7. SNS+
8. OUT+

The 10 uF non-polar capacitors connect OUT- to SNS- and OUT+ to SNS+.

## Mute and output network

The stereo 2P2T mute selects MODE_L/R or 0VA before the driver inputs.
Each driver output then passes through a ferrite bead to the connector-side
net. Each connector-side leg has a 100 pF C0G shunt to CHASSIS and diode
clamps to both supply rails. XLR pin 1 connects to CHASSIS, pin 2 to positive,
and pin 3 to negative.

## Readiness consequence

SCH108 now emits real signal, sense, supply, protection, chassis, connector and
test-point nets. All custom symbols used by the block are embedded by the
writer, so SCH108 passes block-level CAD readiness.

# G3-010A — Panel-Interface Schematic ECO

## Decision

Panel XLR connectors are mechanically owned by the enclosure, not the PCB.
The PCB receives those interfaces through detachable, crimped harnesses.

## Changes

### SCH101

- J101: left panel XLR, off-board.
- H101: left JST VH three-way PCB header.
- J201: right panel XLR, off-board.
- H201: right JST VH three-way PCB header.

The panel and board connector pins are connected one-to-one:

1. chassis/shield
2. signal hot
3. signal cold

### SCH106

- J901: panel five-pin regulated-DC XLR, off-board.
- H901: five-way Mini-Fit Jr PCB header.

Pin functions remain:

1. 0VA
2. +18VA input
3. -18VA input
4. chassis
5. reserved

## Consequences

- The footprint-contract freeze blockers are closed.
- Panel connectors cannot leak into PCB population.
- The cluster placement model now anchors to H101, H201 and H901.
- The external and internal connector families remain mechanically distinct.

This is a mechanical-ownership ECO. The analogue design is unchanged.

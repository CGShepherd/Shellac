# G3-005 — Component-Cluster Placement Baseline Rev A0

## Purpose

Translate the accepted schematic and region architecture into a constrained
placement problem before any PCB coordinate is committed.

## Authority model

Sensitive analogue clusters are manual-authority. A placement engine may
propose their position and orientation, but the result is not accepted without
engineering review. The panel-control harness cluster may be synthesised under
constraints after connector pinouts are frozen.

## Coverage

Every on-board schematic reference is assigned to exactly one cluster. This is
regression-tested against the live block builders, preventing orphaned or
multiply-owned components as the design evolves.

## Deferred decisions

- enclosure part number;
- carrier-plate dimensions and fasteners;
- PCB outline and mounting holes;
- exact connector footprints and harness pinouts;
- exact XY coordinates and rotations.

These remain deferred deliberately rather than guessed.

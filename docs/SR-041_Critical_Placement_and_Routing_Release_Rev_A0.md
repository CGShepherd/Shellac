# SR-041 — Critical Placement Acceptance and Routing Release — Rev A0

## Disposition

Project Shellac is **released for PCB routing**.

SR-041 does not freeze every component XY coordinate as immutable. Instead it
freezes the physical architecture that matters electrically:

- the 220 x 140 mm board outline;
- the four SR-040 mounting-hole datums;
- functional cluster location and signal-flow order;
- sensitive-node adjacency and separation;
- routing authority and via limits;
- the continuous 0VA reference-plane strategy.

Exact component positions may be refined locally during manual routing provided
the component remains inside its owning cluster envelope and the cluster's
adjacency, orientation, keep-out and probing rules remain satisfied.

This is intentional. Locking exact XY before routing would force avoidable
rework when shortening feedback loops or escaping real footprint pads.

## Manual-routing authority

The following remain manual:

1. cartridge input pairs and RF front end;
2. SCH101 LT5400 source/summing/feedback and PRE_EQ nodes;
3. SCH103 replay-EQ feedback, timing and selector branches;
4. SCH107 frequency-setting nodes;
5. mode-matrix summing nodes;
6. THAT1646 OUT/SNS loops;
7. 0VA/chassis bond region.

The rail spine, balanced outputs and ordinary analogue routes may use assisted
routing only with post-route review. Control routes may use constrained
automation outside sensitive regions.

## Placement acceptance

All manual-authority clusters are accepted as the routing baseline subject to
controlled local refinement. This includes SCH101, SCH103, SCH107, SCH108 and
the other clusters already marked manual by the placement contract.

A new deterministic check prevents any placed footprint envelope from entering
the frozen mounting-hole copper/component keep-out.

## Next step

Create/populate the KiCad PCB from the released placement and begin manual
routing in this order:

1. cartridge inputs and SCH101;
2. SCH103 replay-EQ islands;
3. SCH107 filter;
4. THAT1646 output sense loops;
5. remaining signal path;
6. rail spine and local power branches;
7. controls and non-critical completion.

After routing: native DRC, ERC regression, plane/return-path review, fabrication
outputs and PCBWay release pack.

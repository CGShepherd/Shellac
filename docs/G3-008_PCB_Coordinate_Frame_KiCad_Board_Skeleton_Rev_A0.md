# G3-008 — PCB Coordinate Frame and KiCad Board Skeleton

G3-008 creates the first KiCad PCB artefact for Project Shellac. It is a
**provisional design skeleton**, not a manufacturing board.

The generated board contains:

- the stable component-side coordinate convention;
- a 220 × 140 mm provisional rectangular outline;
- the four-layer stack-up declaration;
- functional placement-region guides on `Dwgs.User`;
- board-edge clearance guidance on `Cmts.User`;
- prominent `PROVISIONAL — NOT FOR MANUFACTURE` status text.

It deliberately contains no mounting holes while the enclosure/carrier decision
is unresolved. Frozen mounting-hole footprints are emitted only from an approved
`BoardOutlineContract`.

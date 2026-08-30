# SR-041A — mounting-hole clearance closure

SR-041 correctly detected two component/mounting-hole keep-out collisions:

- H101 / MH1
- TP8010 / MH4

Both occur on the left mounting-hole column. The correction moves the two
mounting-hole columns outward symmetrically:

- X inset: 8.0 mm -> 5.0 mm
- Y inset: unchanged at 8.0 mm

Resulting hole centres:

- MH1 = (5, 8) mm
- MH2 = (215, 8) mm
- MH3 = (215, 132) mm
- MH4 = (5, 132) mm

The 3.2 mm NPTH drill and 8 mm copper keep-out remain unchanged.

No PCB outline, carrier geometry, signal-chain topology, component placement,
electrical value, footprint or routing policy changes are introduced.

# SR-043 — Native Board Placement and Stack-up Gate — Rev A0

The SR-042 F8 hand-off produced a genuine KiCad 9 board with real pads and
schematic-derived nets and no routed copper.

SR-043 applies all 250 released component placements, the frozen 220 x 140 mm
Edge.Cuts outline, and four frozen 3.2 mm NPTH mounting holes.

The remaining KiCad-owned setup step is to configure four copper layers:
F.Cu / In1.Cu / In2.Cu / B.Cu. In1.Cu is the continuous 0VA plane and In2.Cu
is reserved for power distribution. Save the board and run VALIDATE_SR043.bat
before any routing.

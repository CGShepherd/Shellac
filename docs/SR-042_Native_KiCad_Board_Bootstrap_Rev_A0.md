# SR-042 — Native KiCad Board Bootstrap — Rev A0

## Purpose

SR-041 released the design for routing. SR-042 moves from engineering-model
placement into the **real KiCad PCB document**.

The old G3-013 populated review board must not be routed: its footprints are
only envelopes and contain no real pads or nets. SR-042 therefore creates a
placement-reference board with the four frozen mounting holes and 250 accepted
placement envelopes, while explicitly retaining KiCad as owner of the real
`.kicad_pcb`.

## One native-KiCad hand-off

After this package passes:

1. open `out/kicad/ProjectShellac.kicad_sch`;
2. use **Tools -> Update PCB from Schematic (F8)**;
3. create/save `out/kicad/ProjectShellac.kicad_pcb`;
4. do not route yet;
5. use `out/sr042/placement_manifest.csv` plus
   `out/kicad/ProjectShellac_PlacementReference.kicad_pcb` to position the real
   footprints;
6. add the four frozen NPTH holes;
7. run native KiCad DRC.

Once that real native board is pushed to `develop`, the next phase can modify
and review the actual PCB rather than a placeholder model, and the first copper
pass begins with SCH101.

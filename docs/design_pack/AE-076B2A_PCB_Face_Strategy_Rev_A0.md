# AE-076B2A — PCB Face Strategy — Rev A0

**Status:** SELECTED — NATIVE CONTROL/SUPPORT MIGRATION OPEN

The AE-076B2 read-only audit found 261 native footprints on F.Cu and zero on
B.Cu. The four controlled Panasonic ECEA1VN100U 11 mm sense capacitors
C80010/C80011/C90010/C90011 are all on F.Cu. Native support geometry remains
MH1-MH4 only.

AE-076B2A selects the installed board orientation:
- F.Cu faces downward into the enclosure;
- B.Cu faces the removable upper cover;
- existing electronics remain on F.Cu;
- all seven operator controls are mounted from B.Cu toward the upper cover.

This removes the four 11 mm sense capacitors from the NKK 12.3 mm top-cover
clearance stack without moving the existing electronics population.

Exact mirrored B.Cu control footprints, pin numbering, actuator/body
orientation, courtyards and 3D models must be verified before native migration.

Still open: C&K installed-plane compatibility, six-support XY/Z/hardware and
tolerance stack, exact control XY and panel apertures, vendor CAD ingestion,
KiCad STEP export, exact rear DC connector, full clearance/service review and
RUN10 switch-local parasitic/stability obligations.

No native KiCad geometry is changed. Routing remains explicitly unauthorised.

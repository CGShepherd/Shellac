# AE-076B2B — Mechanical Source Inputs, DC Interface and KiCad STEP — Rev A0

**Parent baseline:** `1e8702139db68ef42bd0c2dd414db99524948309` (AE-076B2A)
**Status:** PARTIAL MCAD INPUT SET CONTROLLED — METCASE STEP INGESTED / GEOMETRY RECONCILIATION OPEN

The initial B2B transaction failed closed because METCASE requires registration
and login for 3D model downloads. This record therefore distinguishes public
manufacturer evidence from authenticated manufacturer geometry.

Controlled now:
- official M5502119 PDF drawing, hash-controlled;
- official Neutrik NC3FD-L-B-1, NC3MD-L-B-1, NC5MD-LX-B and NC5FD-LX-B STEP;
- governed KiCad PCB STEP export with source-board/version/hash evidence;
- five-pole Neutrik regulated-DC interface.

The authenticated M5502119 STEP is ingested and hash-controlled. Dimensional reconciliation against the controlled manufacturer drawing remains open.

J901 remains 1=0VA, 2=+17VA_IN, 3=-17VA_IN, 4=CHASSIS, 5=NC_RESERVED.
Selected DC hardware is NC5FD-LX-B at the PSU source, NC5MD-LX-B at the audio
chassis, with NC5MXX-B/NC5FXX-B cable ends.

Pin-1-to-shell bonding is prohibited. Generic 5-pole/DMX cable substitution is
prohibited unless pinout/continuity is verified.

The generated PCB STEP omits H901, C30060 and C35060 because their referenced 3D models are unavailable in the installed KiCad model set. FreeCAD assembly, exact PCB-model closure, NKK/C&K geometry, common-plane fit, six-support geometry, control XY and native migration remain open. Routing remains false.

# AE-076B — Control Service-Module Architecture Supersession — Rev A0

**Project:** Shellac
**Status:** CURRENT ARCHITECTURE SELECTED — PHYSICAL MCAD/CAD MIGRATION OPEN
**Baseline:** `817297ed7cccfdbaaa4c0ee3360d5c8ac3fdc35d` (AE-076A)

## Selected current architecture

AE-076B supersedes the current AE-075D/E/F four-local-control-PCB,
detachable-control-harness and aluminium-carrier ownership path.

Shellac shall use:
- one 220 x 140 mm-class main audio PCB as the only audio/control PCB;
- all seven operator controls directly mounted to that PCB;
- upper cover + main PCB + controls as one removable service module;
- six PCB-to-upper-cover primary supports;
- no aluminium carrier in the selected architecture;
- no local EQ/C&K control PCBs and no control inter-board harnesses;
- short detachable front input-XLR, rear output-XLR and rear-DC panel looms retained.

Analogue locality is retained: Bass/Treble remain local to SCH103, Rumble to
SCH107, and Matrix/Mute to their downstream signal-chain regions.

## Z-stack boundary

The NKK `NR01105ANG13-2C/-2A` + AT3009 installation retains the controlled
**12.3 mm panel-to-PCB** relationship.

The controlled C&K evidence does not define a unique installed PCB plane.
AE-076B therefore does not infer a common Z from catalogue body/bushing depth.
AE-076B2 must prove C&K fit at the rigid PCB plane constrained by NKK evidence.

## Six-support boundary

Six PCB-to-upper-cover supports are selected as the primary PCB datum/support.
Their XY, Z, hardware and tolerance stack are not frozen. Threaded C&K bushings
remain secondary registration/support only after the PCB is naturally located.

## Physical CAD boundary

SR-040 / AE-071B `MH1`-`MH4` native geometry is retained unchanged as
**interim physical CAD**. AE-076B does not add `MH5/MH6`, move MH1-MH4, or
migrate control footprints.

## AE-076B2 MCAD gate

Before manual PCB placement can be accepted, create a governed dimensionally
accurate assembly containing the M5502119 chassis/panels, current KiCad PCB,
major controls/connectors, six-support candidate geometry and service/clearance
envelopes. Review top/front/rear views, longitudinal/transverse control-stack
sections and service-removal access.

Still open under B03:
- C&K/NKK common-plane compatibility;
- six-support XY/Z/hardware/tolerance stack;
- exact control footprints/pin maps/courtyards/3D envelopes;
- control XY and top-cover apertures;
- RUN10 parasitic/stability acceptance;
- native PCB control/support migration;
- manual placement reconciliation.

Routing, layout freeze, BOM freeze and manufacturing release remain explicitly
unauthorised.

# AE-076F0 — Metcase Rail-Carrier Mechanical Trade — Rev A0

**Date:** 2026-10-09  
**Parent promoted baseline:** `2a912eac1c63313443f99dc87f86e07232f1a40b`  
**Status:** INFORMATIONAL TRADE / DESIGN-DRIVING QUALIFICATION OPEN  
**Authority effect:** NONE. AE-076B six PCB-to-upper-cover supports remain current selected architecture. No routing, layout, BOM, manufacturing or drilling release.

## Problem and reference dimensions

One main 220 x 140 mm-class Shellac PCB; B.Cu faces removable cover and F.Cu component population faces downward. Seven controls mount directly to the PCB; NKK installed cover/panel-to-PCB datum nominally 12.3 mm. Metcase M5502119 source controls 260 x 250 x 90.2 mm exterior, 86.2 mm inside cover datum and approximately 229 mm internal front/rear depth; nominal guide width 241.01 mm and inside-face width 236.00 mm. These are descriptive evidence, NOT a dimensionally frozen groove throat or full assembly datum. Manufacturer UNICASE catalogue states nominal 1.6 mm PCB thickness and four guide positions. The archived controlled M5502119 PDF and exact authenticated STEP are the geometry sources. Manufacturer reference: https://www.metcase.co.uk/en/Unicase/M5502119.htm and https://www.metcase.co.uk/en/Unicase/M5502119/M5502119.pdf .

## Candidates (no selection)

A. **Current selected:** PCB tied to removable upper cover through six primary supports. Exact switch stack, XY/Z and installation still open.

B. **Rail sheet + local reinforcement:** a nominal 1.5 or 1.6 mm aluminium sheet/tongues enter one pair of extrusion guides; a separate **narrower 2 mm or thicker** structural plate/frame is bolted or structurally bonded to the inboard area, not inserted as a full 3.5/3.6 mm laminate into the groove. This distinguishes rail-interface thickness from bending stiffness. The reinforcement must clear the approximately 236 mm inside-face width, actual groove lip, rail extrusion, component population and fastener heads. Bolting requires demonstrated shear transfer/preload/slip resistance and retained joints; bonding requires appropriate alloy/finish preparation, joint inspection, durability and an independent service/failure assessment. The exact metal-to-metal and chassis electrical bond must be deliberate.

C. **Two rail levels:** separate approximately 1.5/1.6 mm skeletal frames guided at two compatible heights, connected by hex spacers/bolts, with the main PCB separately supported. Potential for greater bending and torsional stiffness, but discrete spacer joints may not provide box-section composite action; check racking, enclosure assembly tolerance, overconstraint, load paths and axial sliding retention.

D. **PCB itself enters guides:** NOT a viable direct assumption for an approximately 220 mm-wide board across nominal 241 mm guide width. Any PCB edge extensions or adaptors would require a different qualified mechanical scheme, not an informal fit claim.

E. **Single structurally reinforced sheet/rib frame:** retain as a lower-complexity comparator before endorsing two-rail cage hardware.

## Mandatory discriminators before choice

1. Exact four groove face/throat widths, heights, parallelism and engagement lengths from authenticated STEP, with drawing correlation and at least one physical extrusion gauge/fit; nominal 1.6 mm guidance is NOT groove-fit acceptance for 1.5 mm sheet.
2. Upper-cover panel/control Z-stack: NKK 12.3 mm installed relationship; all C&K bushing/knob stack, PCB thickness and F.Cu component/card height; exact control shaft height and cover drop-on/aperture path.
3. Use bounded realistic switch lateral/torque loads and supported-PCB deflection limits based on controls, panel hole clearances and solder-joint strain; do not infer stiffness from plate strength or claim that two perforated plates behave as an ideal rigid box without shear-coupling evidence.
4. Confirm the full populated 256-footprint board STEP, installed service-card envelopes, gain shunts, H901 and both capacitors; no copper, switch-body, connector or card interference. Ensure bottom-off probing/service and full slide-in/slide-out operation.
5. Check rail-edge capture, vibration/rattle, longitudinal stops, captive hardware, disassembly without removing soldered switches, thermal expansion and tolerance accumulation across two rail levels.
6. Quiet 0VA/chassis: no inadvertent parallel R909 bridge, intentional CHASSIS connection and verification despite aluminium surface finish/oxide/anodising.
7. Cost/fabrication comparison: thickness availability, kerf/corner radii, fastener access, thread engagement, fatigue, repeatability and assembly sequence. Avoid threaded fasteners solely in 1.5 mm sheet without pull-out/thread engagement evidence.

## Decision method

Build two parametric assembly candidates first: current upper-cover six-support selection and rail-sheet plus inboard reinforcement. Compare dual-rail skeletal cage if simpler support fails stiffness/access/service gates. Hold native MH1-MH4, control positions and release gates until selected candidate passes dimensionally accurate MCAD and fit/load/access verification. A mechanical preference is not manufacturing evidence.

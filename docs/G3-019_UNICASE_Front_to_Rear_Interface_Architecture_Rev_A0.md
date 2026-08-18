# G3-019 — UNICASE Front-to-Rear Interface Architecture — Rev A0

## Objective

Freeze the enclosure-family, panel ownership, signal-flow direction, PCB-mounted control philosophy, and drilling-template contract before exact enclosure sizes and control coordinates are committed.

This change does **not** freeze either enclosure order code and does not release any hole coordinates for manufacture.

## Enclosure family decision

Project Shellac now uses the **METCASE UNICASE** family in **black RAL 9005** as the selected enclosure architecture for both the main audio chassis and the external PSU.

METCASE describes UNICASE as an aluminium total-access instrument enclosure with removable top/base panels, a removable internal chassis, PCB guide rails, and anodised front/rear panels. The current audio-size candidate is black UNICASE 2 `M5502119`, for which METCASE publishes 260 x 250 x 90 mm external dimensions and a 241 x 229 mm base-PCB capability. Exact usable control stack-up, panel intrusion, mounting geometry and final order-code fit remain drawing-gated.

Manufacturer references:

- https://www.metcase.co.uk/en/Metal-Enclosures/Unicase.htm
- https://www.metcase.co.uk/en/Unicase/M5502119.htm

## Main audio chassis architecture

The physical signal direction is now **front to rear**.

- Front panel: left/right cartridge input XLRs.
- Front board edge: balanced-input/RF region immediately behind the input connectors.
- Middle board bands: replay EQ, rumble filtering, final gain/mode processing.
- Rear board edge: mute/balanced-output regions.
- Rear panel: left/right output XLRs.
- Rear panel near centreline: regulated DC inlet and local chassis-bond region.
- Upper cover: operator switch/potentiometer shafts or bushings and indicators/light pipes.

The old right-to-left board-flow convention is superseded.

## Control mounting

All operator switches and potentiometers are PCB mounted. No flying switch/potentiometer harness is permitted.

Where a suitable component is available, a threaded bushing should pass through the upper cover and be retained by its washer/nut. The bushing provides location and secondary mechanical support **only after** the PCB position has been established by its own mounting datums. The nut must never be used to pull an offset PCB into alignment.

Plain-shaft PCB controls remain an allowed fallback if required by electrical/component quality constraints.

PCB-mounted LEDs with light pipes are preferred. A flying indicator lead is permitted only if a suitable PCB/light-pipe solution cannot be achieved and that exception is explicitly reviewed.

## PSU architecture

PSU physical flow is **rear to front**.

- Rear panel: IEC/filter/switch and mains entry.
- Rear internal zone: protective earth and mains wiring.
- Transition: toroidal transformer.
- Forward internal zone: rectification/regulation.
- Front panel: regulated low-voltage DC output.

The top/base clamshell panels should remain unmachined if the selected UNICASE size permits the complete transformer, regulator, wiring, segregation and thermal layout.

## Preliminary placement reorientation

The coarse placement synthesis now treats board Y as the front-to-rear direction. Inputs occupy the front band. Left/right replay networks occupy the next band. Rumble/final-gain/control logic occupy the middle band. Balanced outputs and regulated-DC entry occupy the rear band, with DC entry reserved near the centreline.

The previous CLU-106 left-edge macro coordinates are intentionally discarded because they encode the superseded enclosure orientation. CLU-106 returns to deterministic manual-review placement until exact rear-panel/DC-entry geometry is frozen.

## Drilling-template contract

Case drilling templates are generated mechanical outputs, not hand-dimensioned workshop sketches.

Released templates must:

- use a manufacturer-defined enclosure/panel datum rather than chained hole-to-hole dimensions;
- be supplied as 1:1 PDF and DXF;
- include switch/pot bushing centres and finished hole diameters;
- include anti-rotation features where required by selected hardware;
- include indicator/light-pipe apertures;
- include front/rear XLR/DC and PSU IEC/DC connector cut-outs;
- include datum/centre lines and check dimensions;
- include a 100 x 100 mm calibration box;
- state `PRINT AT 100% / ACTUAL SIZE — DO NOT FIT TO PAGE`;
- verify PCB-to-cover stack-up and bushing thread engagement before drilling.

No manufacturing drilling template may be released until exact UNICASE order codes, PCB/control coordinates, control part numbers, panel thickness and manufacturer drawings are frozen.

## Status after G3-019

Frozen:

- METCASE UNICASE family;
- black RAL 9005 finish;
- main-chassis front-to-rear signal direction;
- front input / rear output + DC panel ownership;
- PCB-mounted operator controls through the upper cover;
- PSU rear-mains/front-DC direction;
- datum-based drilling-template requirements.

Still open:

- exact audio UNICASE order code;
- exact PSU UNICASE order code;
- exact switch/potentiometer families and bushing stack-up;
- final indicator/light-pipe implementation;
- released hole coordinates and templates;
- final carrier/chassis mounting decision after exact UNICASE drawings are overlaid.

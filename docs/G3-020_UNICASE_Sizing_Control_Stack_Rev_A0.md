# G3-020 — UNICASE exact sizing and control-stack mechanical closure — Rev A0

## Objective

Close the audio enclosure order code at drawing level and turn the smaller matching PSU UNICASE into an explicit component-fit gate rather than silently relaxing the historical PSU envelope.

## Decisions

- Audio enclosure: METCASE UNICASE 2, black RAL 9005, **M5502119 — FROZEN**.
- Manufacturer drawing evidence used by the model: 260 x 250 x 90.2 mm external, 241 x 229 mm base-PCB envelope, 256 x 236 mm inside-face envelope, 86.2 mm usable cover height, 2 mm front/rear panels.
- The 220 x 140 mm PCB fits directly; the existing 230 x 150 mm carrier concept also fits the stated base envelope when correctly oriented.
- PSU candidate: METCASE UNICASE 1, black RAL 9005, **M5501119 — CONDITIONAL**.
- M5501119 is not frozen and the historical 180 mm depth / 80 mm height PSU screening gate is not silently weakened.
- Toroid International TI-69043-ME is represented conservatively as 78 x 78 x 36 mm, derived from the 73 mm diameter / 31 mm height datasheet dimensions plus the stated 5 mm allowance.
- Exact IEC/filter/switch, regulator-board mounting, mains/SELV segregation and passive thermal fit must close before M5501119 can supersede the old screening envelope.

## Control stack

The upper-cover stack is now a formal contract. PCB/standoffs establish position first. Panel holes provide assembly clearance. Threaded pot/switch nuts may locate and support only after natural alignment and must never pull the PCB or cover into position.

Manufacturing drilling coordinates remain gated by exact control part numbers, bushing dimensions, verified cover thickness/Z datum, PCB control coordinates and washer/nut/knob stack.

## Scope discipline

This increment does not select pots, switches, IEC hardware or release drilling templates. Those are the next physical-part closure tasks required by the explicit gates above.

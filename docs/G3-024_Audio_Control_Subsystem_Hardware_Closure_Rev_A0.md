# G3-024 — Audio Control Subsystem Hardware Closure

**Revision:** A0  
**Status:** candidate for controlled merge  
**Base:** SR-036 / `2728729f96166abf521d332aec886016555fd057`

## Objective
Close physical hardware selection for the five external operating switches and two rail indicators without inventing the still-unrecovered internal 3180 us RIAA switch topology or prematurely releasing PCB/drilling geometry.

## External controls
- SW901 Bass — Grayhill `71BDF30-01-2-AJN`, adjustable stop at 5.
- SW902 Treble — same exact MPN, adjustable stop at 5.
- SW903 Channel Mode — Grayhill `71BDF30-02-2-AJN`, two decks/four poles total, adjustable stop at 4.
- SW904 Rumble — C&K `7201SYCBE`, DPDT ON-ON, PC pins, threaded bushing, gold contacts.
- SW905 Mute — same exact C&K `7201SYCBE`.

All five are intended as PCB-mounted controls with bushings through the top cover. PCB standoffs define the board datum; the bushings are intentional secondary structural connections and must not pull a misaligned PCB into position.

## Rail indicators
LED901 and LED902 are fitted only to the audio chassis, on the top-cover longitudinal centre spine, as a symmetric pair. Selected LED is Vishay `TLLG4401`, 3 mm diffused green low-current type. Selected holder is Arcolectric/Bulgin `A104700BLACK`, black-finished brass 3 mm bezel.

Retain 8.2 kΩ current limiting. With a 2.4 V design forward voltage, nominal current is about 1.90 mA from an 18 V rail. This deliberately targets subdued indication. LEDs use short flying leads; no light pipes are used.

## Representation boundary
The existing SCH109 builder remains a generic electrical/interface representation and is not yet placement authority. G3-024 updates the engineering model/BOM with selected hardware. Verified custom footprints, 3D envelopes and final PCB/top-cover coordinates remain for the next physical-board package.

## Internal RIAA ON/BYPASS
Recovered intent is retained: the later 3180 us / 50 Hz RIAA function is separately switchable internally and BYPASS is straight-through. It is not implemented by adding a third pole to the Bass rotary. The controlled SCH103 evidence does not yet identify the exact nodes or pole count, so G3-024 intentionally does not nominate an SPDT/DPDT topology or MPN.

## Acceptance
- selected external hardware exists in the controlled BOM/model;
- model no longer describes only generic top-panel controls;
- tests assert switch commonality, structural ownership and low-current LED implementation;
- RIAA topology and footprint/drilling authority remain explicitly open;
- full regression passes.

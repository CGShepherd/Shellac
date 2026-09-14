# Project Shellac — AE-041 DP4 Matrix and Top-Cover Control Authority

**Revision:** A0
**Status:** ARCHITECTURE FROZEN — ABSOLUTE MECHANICAL COORDINATES OPEN
**Date:** 9 September 2026
**Scope:** Post-AE-040C control/matrix authority consolidation

## 1. Purpose

This record consolidates the current Project Shellac control and matrix architecture
before any new PCB placement or top-cover drilling is released.

It deliberately distinguishes:
- frozen architecture;
- selected/procurable control hardware;
- provisional ergonomic geometry;
- verification items that remain open.

No previous 4P4/Lorlin channel-matrix architecture is to be reinstated unless later
evidence demonstrates a material defect in the selected DP4 architecture.

## 2. Frozen signal-flow and top-cover authority

Main audio signal flow remains:

`FRONT -> Input -> Bass -> Treble -> Rumble -> Matrix -> Mute -> Output -> REAR`

The removable TOP COVER mirrors this front-to-rear flow.

The front and rear vertical panels retain the previously defined XLR and power
interfaces. This record does not redefine Shellac as a conventional front-panel
control layout.

### 2.1 Channel-local controls

Bass and Treble remain dual-mono and remain physically local to their respective
left/right channel circuitry.

The channel controls are intentionally independent so that left and right channels
may be configured with different replay characteristics for direct comparison.

Selected platform:
- NKK NR01 family;
- four physical rotary controls total;
- Bass L / Bass R first;
- Treble L / Treble R second;
- Bass knobs red;
- Treble knobs black.

### 2.2 Shared downstream controls

After the independent channel paths, shared controls may converge toward the
longitudinal centreline:

1. Rumble
2. Matrix
3. Mute

This convergence is an electrical/functional consequence of the downstream shared
architecture. It is not a central-control-strip design rule.

## 3. Matrix architecture

### 3.1 Selected topology

The selected matrix architecture is DP4.

Permanent averaging resistors:
- 2 x 4.7 kOhm;
- 0.1 % tolerance;
- connected at the SCH104 OPA1656 outputs;
- located before the existing 100 Ohm isolation resistors.

The permanent averaging network provides the `(L+R)/2` source required for mono
operation without requiring a four-pole four-position rotary switch.

### 3.2 Selected switch

Leading production switch:
- Manufacturer: C&K
- MPN: A20403RNCG
- Function: DP4T
- Positions: 4
- Switching: break-before-make / non-shorting
- Contacts: gold
- Mounting: through-hole PCB
- Procurement intent: quantity one

Matrix order, CCW -> CW:

1. DUAL L
2. STEREO
3. L+R
4. DUAL R

Preferred knob:
- TE / Alcoswitch KN900B1/4
- black knurled aluminium
- 24.1 mm nominal diameter
- indicator line

### 3.3 Review disposition

The DP4 permanent-summing architecture has passed preliminary analytical review for:
- loading;
- Johnson-noise contribution;
- nominal gain error;
- resistor-tolerance sensitivity;
- DC interaction.

The following remain verification items:
- channel crosstalk with real impedances/layout parasitics;
- switch transient behaviour;
- bench confirmation of mode levels and mono averaging;
- SPICE confirmation where useful.

These open checks are qualification items, not reasons to revert to 4P4.

## 4. Rumble and Mute hardware

The existing control authority is retained:

- SW904 Rumble: C&K 7201SYCBE
- SW905 Mute: C&K 7201SYCBE

Required characteristics:
- DPDT ON-ON;
- gold-contact low-level suitability;
- panel threaded bushing;
- PC through-hole terminals;
- epoxy-sealed terminal construction.

This is recovered authority, not a new component selection.

## 5. Rumble and Mute operator convention

Both toggles use transverse LEFT <-> RIGHT actuation when the unit is viewed from
the FRONT.

Longitudinal placement communicates signal-chain order.
Transverse lever movement communicates function state.

### 5.1 Rumble

Heading: `RUMBLE`

Left: `BYPASS`
Right: `IN`

Avoid `OFF/ON`, because "rumble on" is semantically ambiguous.

### 5.2 Mute

Heading: `MUTE`

Left: `RUN`
Right: `MUTE`

Avoid `OFF/ON`, because it creates unnecessary ambiguity about whether the label
describes the audio path or the mute function.

### 5.3 Common state convention

For both toggles:
- LEFT = normal/non-asserted state;
- RIGHT = asserted special function.

## 6. Relative top-cover geometry

Absolute drilling coordinates remain OPEN.

The following are ergonomic/layout targets, not manufacturing-release dimensions:

- Treble -> Rumble centre pitch: >= 25 mm
- Rumble -> Matrix centre pitch: >= 32 mm
- Matrix -> Mute centre pitch: >= 35 mm
- Matrix top-side ergonomic access envelope: target approximately 40 mm diameter

The Matrix-to-Mute spacing is deliberately the largest because Mute is likely to be
operated rapidly and accidental rotation of the Matrix selector is undesirable.

The final pitches shall be checked against:
- exact switch-body envelopes;
- PCB footprints;
- top-cover fixing features;
- main-board component keep-outs;
- knob/lever finger clearance;
- wiring and service access.

## 7. REG-08 authority

REG-08 shall be treated as a TOP-COVER MECHANICAL-REGISTRATION AUTHORITY.

REG-08 is not a physical central control region.

It shall register:
- control shaft/bushing penetrations;
- switch orientation;
- control labels/state labels;
- hardware keep-outs;
- top-cover-to-main-PCB datum relationship;
- allowable mechanical tolerances;
- manufacturing release status.

It shall preserve channel-local placement where electrically appropriate and shall
permit shared controls to converge only where the downstream architecture genuinely
becomes shared.

## 8. Main mechanical baseline retained

- Frozen enclosure family/order: existing METCASE M5502119 authority retained.
- Main PCB remains approximately 220 x 140 mm.
- Signal flow remains FRONT -> REAR.
- Controls remain on the removable TOP COVER.
- Front/rear panels retain previously defined XLR and power interfaces.

## 9. Superseded control concepts

The following are not live authority:
- Lorlin 4P4 channel-matrix architecture;
- centralised Bass/Treble control strip;
- conventional front-panel operator-control layout;
- linked-stereo Bass/Treble operation;
- any top-cover layout that reverses the front-to-rear signal sequence.

Historical design records remain traceability evidence and shall not be deleted.

## 10. Release boundary

This record freezes architecture but does NOT release:
- final PCB coordinates;
- final top-cover drilling;
- artwork coordinates;
- Matrix legend angles;
- shaft-height stack-up;
- final footprint orientation;
- crosstalk qualification;
- switching-transient qualification.

Those items require the post-patch generated placement model and/or SPICE/bench
evidence.

## 11. Design acceptance assertions

A conforming future implementation shall satisfy all of the following:

1. Four independent NKK NR01 Bass/Treble controls are represented.
2. Bass precedes Treble in the top-cover longitudinal sequence.
3. Rumble precedes Matrix.
4. Matrix precedes Mute.
5. Rumble and Mute use C&K 7201SYCBE authority.
6. Rumble labels are BYPASS / IN.
7. Mute labels are RUN / MUTE.
8. Both toggles use left-normal/right-asserted convention.
9. Matrix hardware authority is C&K A20403RNCG.
10. Matrix mode order is DUAL L / STEREO / L+R / DUAL R, CCW -> CW.
11. Matrix electrical requirement is DP4, not 4P4.
12. Two permanent 4.7 kOhm 0.1 % averaging resistors are represented at the SCH104
    OPA1656 outputs before the 100 Ohm isolation resistors.
13. REG-08 is registration authority, not a central control strip.
14. Absolute drilling coordinates remain unreleased until mechanical review closes.

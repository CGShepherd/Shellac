# Project Shellac G3-016 — Real-Footprint Audit and Capacitor ECO Blockers

**Revision:** A0  
**Gate:** 3A detailed population preparation  
**Status:** Blocked pending controlled capacitor decomposition and technology decisions

## Purpose

Convert the visually accepted macro-placement into a physically credible component population without allowing placeholder geometry to conceal unresolved schematic-to-part mappings.

## Audit result

The footprint contract contains 225 PCB-owned references. Mechanical identities for the input harness connectors, DC harness connector, DIP gain selector, 39 probe test points, SOIC-8 devices, standard 0805 passives, protection diodes, and the corrected CLU-106 reservoir capacitors are credible for continued review.

The audit identifies two classes that cannot yet be frozen:

1. Fourteen SCH103 replay-EQ references encode two or three parallel capacitor values under one reference and one 0805 footprint. These are electrical aggregate values, not physical components. Each aggregate must be decomposed into separately referenced capacitors while retaining the exact synthesised total and mirrored-channel symmetry.
2. Four 10 uF non-polar signal capacitors in SCH108 are assigned generic 0805 footprints without an approved dielectric, voltage rating, derating basis or physical technology.

A further sixteen 10 uF 0805 capacitors require voltage and DC-bias derating review before footprint freeze.

## Decision

No silent footprint substitution is authorised. The next controlled activity is a capacitor-technology and physical-decomposition ECO. Routing remains prohibited.

## Invariants

- One reference denotes one physical fitted component.
- Compound EQ values are preserved as explicit parallel parts.
- Left and right channels use identical decompositions and footprints.
- Capacitor dielectric and voltage rating are selected from electrical duty, not package convenience.
- The affordable-performance principle remains applicable: tighter or larger parts are used only where calculation and tolerance synthesis justify them.

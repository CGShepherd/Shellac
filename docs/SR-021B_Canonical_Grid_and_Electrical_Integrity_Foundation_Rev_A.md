# SR-021B — Canonical Grid and Electrical-Integrity Foundation

**Revision:** A  
**Parent:** accepted SR-021 baseline  
**Status:** locally validated; native KiCad ERC required for acceptance

## Trigger

Native KiCad ERC on SR-021 reported 27 errors and 26 warnings. The rejected
SR-021A exact-coordinate experiment increased this to 32 errors and 892
warnings. Both outcomes demonstrated that connectivity could not be repaired
safely during serialization.

## Architectural correction

All electrical geometry is now normalised when the in-memory `Sheet` is
constructed:

1. component origins are aligned to the canonical 1.27 mm grid;
2. semantic pin positions derive from those aligned origins;
3. wire endpoints, labels and no-connect markers are aligned when added;
4. zero-length wires are rejected;
5. the KiCad writer formats an already-valid electrical model.

This makes the grid an invariant of the design representation rather than a
post-processing side effect.

## Internal assurance gates

`generator/electrical_audit.py` adds repository-wide checks for:

- off-grid components, pins, wires, labels and no-connects;
- required symbol pins without a conductor or explicit no-connect;
- incompatible labels joined by conductor geometry;
- zero-length wires.

Every one of the eight functional sheets passes all four checks.

## Targeted topology repairs

### SCH106

The five-pin PSU inlet no longer fans four domains through overlapping vertical
conductors. Each connector pin uses an independent labelled interface stub and
the visible rails begin separately.

### SCH107

Left and right direct-bypass lanes are separated. Output test points use
different x-coordinates, preventing overlapping stereo output conductors.

### SCH109

Rail indicator branches are now drawn as physical rail-resistor-LED-0VA series
circuits. The obsolete `*_LED_DRIVE` net labels are removed, and positive-rail
LED orientation prevents wires passing through the opposite LED pin.

### Symbol electrical types

The OPA1656 buffer `0VA` reference and THAT1646 `GND` reference are passive
pins rather than undriven power-input pins. Their ±18 V supply pins remain
power inputs.

### Root hierarchy

Root-sheet local labels are placed directly on hierarchical sheet pins. This
removes the 22 dangling root wire stubs reported by native ERC while retaining
deterministic label-based cross-sheet connectivity.

## Local validation

- Python suite: 151 tests passed.
- Engineering Model: 8 blocks / 27 signals / passed.
- Model-driven hierarchical build: passed.
- Two consecutive generated `out/kicad` trees: byte-identical.
- Internal electrical-integrity audit: all eight blocks passed.

## Acceptance

Native KiCad 9 hierarchical ERC must be rerun on Windows. SR-021B becomes the
accepted baseline only after the new report has been reviewed. No analogue
component values or functional design decisions are changed by this increment.

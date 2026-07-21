# Project Shellac — SR-015 ERC and Deterministic Build Closure Rev A

## Status

Implemented and validated against the accepted SR-014 repository.

## Purpose

Close the remaining generated-project library, hierarchy attachment, electrical-rules and repeatability findings without changing any validated analogue value, gain target, replay curve, supply voltage or external control decision.

## Changes

- Generate project-local `Device`, `Connector_Generic` and `ProjectShellac` symbol libraries plus local symbol and footprint library tables.
- Correct the remaining connector, DIP-switch and ferrite-bead footprint identifiers.
- Attach every hierarchical interface to a real electrical endpoint or an explicit non-physical hierarchy anchor.
- Remove legacy local interface aliases in favour of Engineering Model signal names.
- Correct vertical two-pin connection routing and outward power-pin stubs that previously created unintended rail-name collisions.
- Mark the unused PSU connector pin with a KiCad no-connect marker.
- Add non-physical power-output declarations after the two PSU rail links so ERC can identify the regulated +18 V and -18 V rails as driven.
- Replace random child-sheet UUID generation and run-date title fields with deterministic values.
- Make the readiness audit consume native KiCad ERC evidence and pass only when the report is clean.

## Evidence

- Python regression suite: 122 passed.
- Engineering Model: 8 blocks, 27 signals, validation passed.
- Model-driven build: 8 implemented blocks, 0 pending.
- Root hierarchy: 8 sheets, 66 pins, 19 cross-sheet signals.
- CAD-ready functional sheets: 8/8.
- Native KiCad hierarchical ERC: 0 violations.
- Two consecutive clean builds: byte-identical generated project files.
- Gate 2 schematic readiness: PASS.

The accepted SR-014 baseline reported 286 native KiCad findings. SR-015 closes all of them through renderer, library and connectivity corrections. No analogue engineering decision was reopened.

## Programme consequence

Gate 2 is now passed by automated evidence. The next critical-path activity is a visual schematic capture review in KiCad, followed by any presentation-only corrections and then schematic freeze/ERC sign-off before PCB floor-planning and layout.

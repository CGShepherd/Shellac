# Project Shellac - SR-016 Schematic Capture Review Preparation Rev A

## Status

Implemented and validated against the accepted SR-015 repository.

## Purpose

Move the generated project from electrically valid capture to a reviewable A3 schematic pack. This increment changes presentation and renderer behaviour only. It does not alter validated analogue values, gains, replay curves, control truth tables, supply voltages or signal-chain architecture.

## Review findings addressed

- Sheet notes were centred on their insertion point and clipped at the left border.
- Long net labels extended back over symbols and component references.
- SCH105 contained long diagonal signal connections.
- Decoupling components and panel indicators on several sheets entered the A3 title-block area.
- SCH101 gain-network components and its DIP selector were unnecessarily crowded.
- Non-physical hierarchy anchors cluttered functional sheets.
- Root connectivity labels duplicated the already-visible hierarchical pin names and crowded the gaps between sheet symbols.

## Changes

- Left-justify and consistently size sheet notes.
- Orient local label justification away from the connected wire stub.
- Reduce annotation and label typography to a consistent review scale.
- Add deliberate Manhattan routing for the SCH105 mode matrix.
- Spread the SCH101 gain and differential-converter presentation and move its DIP selector into clear space.
- Reposition SCH103 channels and all affected decoupling/indicator groups inside the usable A3 drawing area.
- Hide non-physical hierarchy-anchor annotations while preserving their electrical function.
- Hide redundant root local-label text while retaining deterministic root connectivity.
- Add regression checks for title-block clearance and orthogonal SCH105 signal routing.

## Evidence

- Python regression suite: 124 passed.
- Engineering Model: 8 blocks, 27 signals, validation passed.
- Model-driven build: 8 implemented blocks, 0 pending.
- Native KiCad hierarchical ERC: 0 violations.
- CAD-ready sheets: 8/8.
- Gate 2 schematic readiness: PASS.
- Consecutive clean builds remain byte-identical.
- Nine-page A3 PDF rendered and visually inspected for clipping, title-block intrusion, page completeness and routing presentation.

## Next review

Open the generated KiCad project and review the root plus all eight child sheets at normal working zoom. Record findings against the generator source. In particular, inspect dense internal net naming on SCH101 and SCH103, switch presentation, signal-flow readability and service/test-point identification before schematic freeze.

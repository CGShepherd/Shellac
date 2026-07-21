# G3-007 — Board-Outline and Mounting-Hole Synthesis Interface

## Purpose

Prevent plausible-looking manufacturing coordinates from being generated before
the audio enclosure and carrier plate are supported by authoritative drawings.

## States

- **PROVISIONAL:** board architecture and coordinate convention only; no holes.
- **DECISION_READY:** reserved for complete evidence awaiting formal approval.
- **FROZEN:** board outline and four datum-referenced mounting holes derived from
  an approved carrier-plate freeze.

## Frozen Rev A mounting contract

- four non-plated 3.2 mm finished holes;
- 8.0 mm copper keep-out diameter;
- rectangular pattern measured from the lower-left PCB origin;
- default 8.0 mm inset from each board edge;
- component-side coordinate view;
- board remains vertically removable from the audio enclosure.

Exact values remain provisional until an enclosure and carrier plate are frozen.

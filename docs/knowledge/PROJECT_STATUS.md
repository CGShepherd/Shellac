# Project Shellac — Controlled Project Status

**Knowledge baseline:** SR-035  
**Engineering base:** SR-034 / G3-023  
**Base commit:** `97d333cb66cff90b5685dc6e0a73d3b28d3cf601`

## Frozen / closed
- SCH101 gain architecture and internal eight-way DIP selection are electrically closed.
- SCH103 replay timing-capacitor physical decomposition/selection policy is controlled.
- Audio and PSU enclosures: METCASE UNICASE 2 M5502119, black RAL 9005.
- PSU mains-entry architecture: SCHURTER KMF1.1121.11.
- Front-to-rear audio interface and rear-to-front PSU flow.
- PCB/standoffs establish alignment; panel control hardware does not force PCB position.

## Current manufacturing limitation
Gate 3A PCB output remains a review artefact and does not itself provide manufacturing authority for final pads/nets/routing, mounting holes or drilling coordinates.

## Next engineering package
**G3-024 — Audio Control & Physical-Board Closure.** Start from the prior Lorlin/commonality strategy rather than a blank-sheet switch search. Verify each function against hard electrical/mechanical requirements; freeze exact parts only with sufficient evidence; reconcile PCB/panel ownership; close indicator strategy and establish real mounting-hole authority.

## Following package
Release datum-based manufacturing drilling information only after exact controls, PCB/control coordinates and stack-up are frozen.

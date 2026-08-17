# G3-018 Detailed Placement Readiness — Rev A0

## Objective

Establish a deterministic, physically credible placement candidate and make all placement conditions that still require human review explicit before routing begins.

## Result

The 243-component candidate has no conservative footprint-body overlaps and no KO-001 board-edge violations. The audit remains `HUMAN_REVIEW_REQUIRED` rather than route-ready because conservative courtyard proximity, manual-authority analogue/power clusters, and unfrozen mechanical datums still require review.

## Deterministic findings

- PCB placement proposals: 243
- Automatically accepted proposals: 4
- Manual-authority clusters: 15
- Geometric blockers: 0
- Review findings: 32
  - conservative courtyard-proximity findings: 16
  - manual-cluster review gates: 15
  - unresolved mechanical-datum gate: 1
- Unresolved mechanical inputs: 5

## Design decisions

The existing preliminary grid synthesizer compressed row pitch in one dense mixed-package cluster, CLU-101-B, producing four conservative body overlaps. A deterministic shelf-packing fallback is now used only when the normal grid would overlap bodies. Existing placement remains unchanged for clusters that already fit.

Courtyard proximity is reported as review rather than blocker because the current envelope database is an engineering approximation, not parsed KiCad courtyard polygon geometry. Body overlap and board-edge clearance remain hard blockers.

Mounting-hole and enclosure intrusion checks are not fabricated while mechanical datums remain provisional. Their absence is surfaced explicitly as a review finding.

## Deferred scope

This increment does not route the PCB, select manufacturer parts, redesign the enclosure, freeze mounting holes, or automatically accept critical analogue placement. Those actions remain controlled downstream gates.

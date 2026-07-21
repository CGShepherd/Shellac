# Project Shellac — SR-009 Root Hierarchical Schematic Rev A

## Purpose

Generate one deterministic KiCad root schematic from the validated Engineering
Model and connect all eight pin-aware functional sheets without changing any
approved analogue circuit or component value.

## Implemented

- Eight hierarchical sheet instances, one per functional block.
- Hierarchical pins derived from each block interface.
- Matching hierarchical labels in every child schematic.
- Root-level labelled wire stubs providing cross-sheet net connectivity.
- Deterministic UUIDv5 identities for the root, sheet instances, sheet pins,
  hierarchy labels, root wires and root net labels.
- Child symbol-instance paths aligned with their root sheet instance UUIDs.
- Root and child page-instance records.
- Readiness audit updated to remove the resolved root-hierarchy blocker.

## Deliberate boundary

SR-009 does not reopen electrical engineering decisions.  Final KiCad symbol
resolution and ERC validation remain the next Gate 2 evidence activities.

## Acceptance evidence

- Existing SR-008 tests remain green.
- New hierarchy tests verify all block files, interfaces, labels and paths.
- Two independent builds produce byte-identical root schematics.
- KiCad 9 CLI can parse the generated hierarchy and export a netlist.

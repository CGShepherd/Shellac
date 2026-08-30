# Project Shellac — Controlled Design Pack Index

**Authority:** `main` plus the baseline commit/tag identified in `config/decisions/current_decision_index.yaml`.

This index defines how the repository should be read. Historical documents remain valuable evidence, but the current design is determined by the authoritative decision index and implemented generator baseline.

## 1. Current design baseline

Use these first when determining what is actually implemented:

- generator/model and generator/blocks source on `main`
- `config/decisions/current_decision_index.yaml`
- controlled BOM/procurement configuration
- most recent passing regression suite
- release/baseline tag

A **selected but pending** decision is not the same as implemented hardware.

## 2. Decision register

Authoritative status:
- `config/decisions/current_decision_index.yaml`

Narrative rationale/evidence:
- `docs/decisions/`
- DR-037 record under `docs/`

The index wins if historical prose contains ambiguous status language.

## 3. Design assurance record

Current evidence chain for the signal path:

- AE-001 through AE-010: block-level synthesis/closure history
- AE-011 A1: restored end-to-end architecture
- AE-012: all-state gain/headroom
- AE-013: SCH101 noise/CMRR weakness
- AE-014: precision architecture down-selection
- AE-015: full-chain noise/DC finding
- AE-016 / A / B: failed migration and controlled repair history
- AE-017: atomic migration dependency map
- AE-018: live dependency disposition and LT5400 physical contract
- AE-019: documentation audit
- AE-020: authoritative register/design-pack structure

## 4. Production and commissioning pack

Existing:
- BOM/procurement configuration
- commissioning generator/output
- generated KiCad and PCB artifacts

Still required before release:
- final implemented DR-038/DR-039 BOM
- manufacturing release checklist
- final commissioning limits from the implemented baseline
- signed-off schematic/ERC/PCB checks

## 5. Maintenance guide structure

The maintenance guide shall eventually contain:

1. equipment identification and revision;
2. safety and power architecture;
3. block diagram and signal flow;
4. configuration/service-link settings;
5. expected DC voltages;
6. expected AC signal levels at test points;
7. replay EQ verification procedure;
8. noise and CMRR acceptance;
9. mute/rumble/control checks;
10. fault-isolation flow;
11. approved substitutions and obsolete parts;
12. reassembly/return-to-service test.

See `docs/maintenance/MAINTENANCE_GUIDE_SKELETON.md`.

## 6. Historical archive rule

Documents describing superseded alternatives are never deleted merely because the design changed. They remain provenance.

They must not, however, be used to determine current hardware without checking the current decision index.

Notable examples:
- optional independent 3180 us RIAA work;
- original 2x SCH104 concept;
- AE-016 premature DR-038/DR-039 implementation attempt;
- pre-precision SCH101 resistor architecture once DR-038 is eventually implemented.

## 7. Change-control rule

Every future design change must update, in the same merge:

- implemented source/CAD where applicable;
- affected tests;
- decision index status;
- supporting assurance record;
- BOM/procurement if parts change;
- commissioning/maintenance data if service behaviour changes.

This prevents the design pack and implementation from drifting apart again.

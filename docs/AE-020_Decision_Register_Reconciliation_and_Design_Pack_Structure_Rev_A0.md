# AE-020 — Decision Register Reconciliation and Design-Pack Structure

**Revision:** A0  
**Status:** CONTROL STRUCTURE PROPOSED FOR ADOPTION  
**Baseline:** `main` at `1ebb04d`

## Finding

AE-019 correctly exposed ambiguity, but much of that ambiguity comes from narrative documents mentioning selected and rejected alternatives in the same file. Status cannot therefore be inferred reliably from keyword occurrence.

The repository needs a machine-readable authoritative current-status index separate from historical narrative evidence.

## Resolution

AE-020 introduces:

- `config/decisions/current_decision_index.yaml` — authoritative current decision status;
- `docs/knowledge/DESIGN_PACK_INDEX.md` — how to read the controlled pack;
- `docs/maintenance/MAINTENANCE_GUIDE_SKELETON.md` — future service-document structure.

No historical decision or AE document is rewritten.

## Key reconciled statuses

- DR-037: **CURRENT_IMPLEMENTED**
- DR-038: **CURRENT_SELECTED_PENDING_IMPLEMENTATION**
- DR-039: **CURRENT_SELECTED_PENDING_IMPLEMENTATION**
- DR-040: **CURRENT_SELECTED_PENDING_IMPLEMENTATION**
- AE-016 implementation attempt: **SUPERSEDED by the repair/staging evidence**

This explicitly separates design intent from implemented hardware.

## Next documentation phase

After DR-038/039 atomic migration closes, the decision index must be changed in the same merge from selected/pending to implemented, and the maintenance guide populated with the new service links, DC-block behaviour, CMRR/noise limits and commissioning checks.

# AE-024 — Project-Wide Design Record and Decision Reconciliation Audit

**Revision:** A0  
**Status:** READ-ONLY RECONCILIATION GATE  
**Base repository commit inspected:** `dce5c0ec36e12f979338d8c46106c44a79c7a023`

## Purpose

Shellac now contains enough engineering history that documentation consistency is
itself a configuration-control problem.

AE-024 introduces a read-only audit before the production design pack is frozen.

It does not rewrite historical AE, SR, G3 or decision records. Instead it
identifies where current authority and historical evidence have drifted apart.

## Known issues motivating the audit

1. `config/decisions/decision_status.yaml` and
   `config/decisions/current_decision_index.yaml` presently use different status
   vocabularies.

2. The root `README.md` still identifies SR-034 / G3-023 as the current release
   baseline despite substantial later controlled work.

3. DR-038 recently demonstrated that an authoritative status can be correct while
   stale staging prose remains in the same record.

These are exactly the defects the production design pack must eliminate.

## Audit scope

The generated report inventories:

- decision/review IDs;
- status claims;
- authoritative index status;
- incompatible status vocabularies;
- potential contradictory claims;
- baseline declarations;
- document classification for the production pack.

## Run

From repository root:

`python tools/ae024_design_record_audit.py`

This writes:

`docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md`

Then run:

`python -m pytest`

## Important staging note

AE-023 is not present in GitHub at the inspected commit. AE-024 is deliberately
read-only so it can be applied safely to the local AE-023 working tree without
changing any of its circuit or decision-index modifications.

After AE-023 is committed, rerun AE-024 so its generated report reflects the new
authoritative baseline before we start reconciliation edits.

## Production pack target

The eventual pack is organised as:

- release authority;
- requirements/architecture;
- decision register;
- production CAD/fabrication;
- BOM/procurement;
- design assurance;
- commissioning/acceptance;
- maintenance;
- build/reproducibility;
- clearly isolated historical evidence.

This structure should also provide the template later extracted into Foundry.

# FDR-001 — Project Shellac Foundry Baseline

**Status:** CONTROLLED CANDIDATE
**Introduced by:** G3-025
**Purpose:** preserve the method of engineering as well as the design.

## Authority hierarchy

When evidence or instructions conflict, resolve in this order:

1. safety, regulatory and physical-law constraints;
2. frozen controlled artefacts and manufacturer evidence;
3. explicit controlled decisions in the decision register;
4. controlled Shellac design tenets and engineering rules;
5. derived engineering analysis with reproducible tests;
6. procurement convenience, aesthetics and cost preferences.

A lower level never silently overrides a higher level.

## Evidence hierarchy

- E1: manufacturer drawing, datasheet or official technical page.
- E2: controlled repository model/test/release evidence.
- E3: authorised distributor technical data for the exact MPN.
- E4: reputable secondary technical source.
- E5: recovered historical intent or conversation-derived design intent.
- E6: engineering inference or assumption.

E5/E6 may motivate analysis but cannot by themselves release irreversible
manufacturing geometry.

## Decision states

- `OPEN`: requirement/problem known; no preferred closure.
- `CANDIDATE`: engineering solution proposed but not yet accepted.
- `SELECTED`: preferred solution accepted; validation/release evidence may remain.
- `FROZEN`: reopening requires a superseding controlled decision.
- `MANUFACTURING_RELEASED`: exact geometry/process authorised for fabrication.

## Autonomous decision rule

When direct user input is unavailable, a package may close a decision only when:
- it is consistent with higher-authority controlled requirements;
- evidence is sufficient for the state claimed;
- it is reversible without scrapping manufactured hardware;
- no safety boundary is relaxed;
- no frozen architecture is silently reopened;
- acceptance criteria are deterministic.

Otherwise preserve the issue as an explicit gate.

## Contradiction handling

1. record both statements and provenance;
2. identify authority level;
3. determine whether conflict is real or representational;
4. derive/test the minimum resolving change;
5. issue a superseding decision;
6. update stale artefacts in the same package where practical.

Never erase historical rationale merely because a later decision wins.

## Package rule

Every package records:
- exact base commit;
- changed artefacts;
- acceptance tests;
- remaining gates;
- suggested commit/tag;
- what is explicitly not released.

## Manufacturing gate

No drilling, panel machining or PCB fabrication release is permitted from nominal
catalogue geometry alone. Manufacturing release requires:
- exact selected MPN;
- verified footprint/pad geometry;
- verified panel thickness and Z datum;
- washer/nut/anti-rotation stack where applicable;
- PCB/control coordinates;
- tolerance/clearance check;
- datum-based drawing/template;
- controlled review evidence.

## Project-memory rule

Git is authoritative project memory. Conversation can recover intent, but mature
decisions, rationale, status and evidence belong in Git.

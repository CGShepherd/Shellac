# AE-076D — Executable Authority and Qualification-Delta Reconciliation — Rev A0

**Parent baseline:** `46bfd380193fc6008cdcb2f7ae8acece597f8f80`
**Status:** CURRENT EXECUTABLE AUTHORITY RECONCILED / QUALIFICATION EXECUTION OPEN / ROUTING HOLD RETAINED

AE-076D removes temporal coupling between historical release snapshots and current executable authority without changing analogue topology, migrating selected-next hardware, executing RUN08-RUN14 or releasing routing.

## Closed historical executable defects

Later controlled evidence now closes stale AE071-F02/F04/F05/F06/F07 semantics via AE-074, AE-075A, AE-075B, AE-075-B07 and AE-075G respectively. AE036-F07 is closed by the current/historical authority structure and AE-076C; AE036-F08 is closed by AE-071B board-only/locked mounting-hole ownership. Newer direct-control B.Cu migration, complete-stage RUN10 and gain/personality physical verification remain OPEN routing blockers.

## Historical release quarantine

The SR-039, SR-041 and SR-042 YAML/design records remain unchanged provenance. Their Python adapters are now historical-snapshot readers: historical status remains visible, but `current_authority=false`; they can never grant current routing permission, and SR-042 cannot regenerate historical bootstrap artefacts from mutable current design state.

## Current control/readiness authority

AE-027/AE-028-era rotary language is removed from current pre-routing guidance. Exact NKK/C&K B.Cu footprints, pin/pad mapping, keep-outs, top-cover apertures and the six-support service-module stack remain governed by current AE071-B03.

## Current qualification delta

`config/decisions/ae076d_qualification_delta.yaml` preserves AE-048/049/050 as historical methodology/execution authorities while mapping the remaining campaign to +17.0 V / 0VA / -17.0 V, Grado Prestige 78C, AE-074 branch-local DR-039, AE-076C BASE/+47/+100 differential personality states and AE-075G 25-ohm-per-leg / 50-ohm-differential output semantics. No numerical criterion is relaxed and no RUN08-RUN14 execution is claimed. The Grado 20–50 kHz finding remains an open model-validity/measurement issue.

## Release disposition

The live hold advances to AE-076D. Final routing, layout freeze, BOM freeze and manufacturing release remain FALSE. Final independent design assurance remains OPEN and required after design-driving plus mechanical/native closure.

## One-off build recoverability and state continuity

Final AE-076D review records that Shellac is expected to be a one-off build rather than the first article of an iterative production programme. Residual pre-fabrication uncertainty therefore cannot be deferred on the assumption of a later PCB respin. The current engineering standard is `docs/knowledge/ONE_OFF_BUILD_RECOVERABILITY_STANDARD.md`.

Every remaining design-affecting uncertainty shall be classified before fabrication as `CLOSE_BEFORE_FAB`, `ESCAPE_ROUTE_REQUIRED`, or `BENCH_ONLY_ACCEPTABLE`. Escape mechanisms must be specific, low-impact and realistically reworkable on the assembled unit.

`PROJECT_SHELLAC_WORKING_STATE.md` is introduced as the mandatory non-authoritative cross-chat execution index. It shall be refreshed after every material pass and before the next major phase so conversation-memory loss cannot silently restore superseded design states.

## Next transaction

Proceed to the already-selected personality/native migration and governed H901/C30060/C35060 model binding; routing remains held.

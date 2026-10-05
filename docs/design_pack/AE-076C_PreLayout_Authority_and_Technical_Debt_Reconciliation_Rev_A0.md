# AE-076C — Pre-Layout Authority and Technical-Debt Reconciliation — Rev A0

**Parent baseline:** `3183c07a61248aad648fdecc9cc883a5cfba14c6`
**Status:** CURRENT AUTHORITY RECONCILED / ROUTING HOLD RETAINED

## Cartridge personality architecture

Selected-next: two identical per-channel passive cartridge-loading cards; one local card per channel; differential shunt only; no-card BASE; matched +47/+100 pF L/R service pairs; select by cartridge plus measured cable capacitance; main socket Samtec `SLW-102-01-G-D`; card header `TSW-102-07-G-D`; diagonal duplicate-node assignment makes 180-degree insertion electrically benign. Main-board resistive/RF loading remains. H110/H111/H112 gain programming remains separate.

This is selected-next pending implementation. Live SCH101 still contains H120/H121/H122 until the next controlled migration.

## Executable authority

`precision_cad_contract.py` now matches the already-live `LT5400BIMS8E-7#PBF` and EP9-to-quiet-0VA implementation. `production_readiness.py` is replaced as a current fail-closed oracle: electrical design-driving work, native/model closure, stack/plane rules and routing remain blocked.

## Matrix

C&K `A30403RNCB` is the single selected production Matrix part. TE/Alcoswitch `MRJE3404` is considered-alternative provenance only, not a live fallback. Exact C&K footprint/3D/pin-to-pad/B.Cu migration remains a B03 gate.

## B2C evidence

M5502119 external body reconciliation passes; exact H901 and capacitor-model solutions are proven. Governed native binding remains open, so R-037 is narrowed but not falsely closed.

## Release gates

Routing, layout freeze, BOM freeze and manufacturing release remain FALSE.

## Deferred executable/current-authority debt — AE-076D

AE-076C deliberately does not silently rewrite older executable release machinery. The following current-oracle debt is carried explicitly into AE-076D:

1. `generator/model/production_integrity_audit.py` retains pre-AE-074 DR-039 OPEN semantics;
2. the same oracle retains pre-AE-075A SCH108 sense-cap OPEN semantics;
3. the same oracle retains pre-AE-075B XLR pin-1 OPEN semantics;
4. the same oracle retains pre-AE-075-B07 input-harness OPEN semantics;
5. the same oracle retains pre-AE-075G THAT1646/output-impedance semantics;
6. `generator/model/prerouting_readiness.py` still names AE-027/AE-028 as the current rotary-control gate;
7. `tools/ae031_prerouting_control_audit.py` still emits AE-027/AE-028-era guidance;
8. historical `generator/layout/sr041_routing_release.py` can still return `ROUTING_RELEASED` and therefore requires executable quarantine/fail-closed treatment;
9. `generator/layout/schematic_release_gate.py` mixes an SR-039-era snapshot with later live validators and superseded common-post-EQ assumptions;
10. `config/release/ae071_prerouting_hold.yaml` still carries `final_design_assurance.authority: AE-075_PENDING`;
11. a current qualification delta must explicitly map historical AE-048/049/050 methodology to the +17.0 V rail authority, Grado Prestige 78C source identity and personality-card BASE/+47/+100 electrical states.

These are current-configuration/release-oracle debts, not evidence that the selected analogue architecture is invalid. None grants routing authority.

## Next transaction

AE-076D shall reconcile/quarantine the stale executable/release oracles and current qualification delta above while preserving immutable historical provenance and the existing routing hold.

## Following transaction

After AE-076D, control the exact personality-interface CAD/footprint, migrate SCH101/native H120/H121/H122 to per-channel H120/H220, bind exact H901/capacitor models and regenerate a zero-missing-model PCB STEP. Design-driving RUN08-RUN14 then remains mandatory before routing release can be reconsidered.

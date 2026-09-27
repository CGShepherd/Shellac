# AE-074 — DR039 Branch-Local Product Migration — Rev A0

**Project:** Shellac
**Baseline:** `82bb77c683e779c8a6bd82ccbd11799beb9893de` (AE-073 governed baseline)
**Status:** PRODUCT GENERATOR / GENERATED SCHEMATIC / NATIVE PCB MIGRATION RECONCILED — QUALIFICATION GATES OPEN

## Purpose

Migrate the AE-067 / RUN04 selected DR-039 branch-local DC-block architecture into the live product generator without changing the selected values, without renumbering the existing physical parts, and without releasing routing.

## Implemented electrical migration

- SCH103 no longer contains the common pre-split 1 uF / 330 kOhm network.
- `POST_EQ_L` and `POST_EQ_R` are direct recovery-amplifier handoffs into SCH107.
- SCH107 DIRECT/BYPASS contains one 1 uF series PET-film capacitor and one 330 kOhm / 1% downstream return to 0VA per channel.
- SCH107 FILTER retains the existing intrinsic DC blocking of its high-pass capacitors and receives no additional DR-039 series block.
- `SW1071` remains the stereo break-before-make selector and both filter channels remain continuously driven.

## Identity and physical-contract preservation

The migration deliberately preserves the existing component identities:

- left DIRECT/BYPASS: `C30060`, `R30060`;
- right DIRECT/BYPASS: `C35060`, `R35060`.

No project rule requires these stable identities to be renumbered merely because their schematic ownership moves to SCH107. Preserving them minimises native-PCB, placement, procurement and service churn.

The existing capacitor contract is retained: 1 uF PET film, 63 V, WIMA-MKS2 class, `Capacitor_THT:C_Rect_L7.2mm_W5.0mm_P5.00mm`. The 330 kOhm return remains 1%.

Placement ownership moves from `CLU-103-HF-L/R` to `CLU-107-L/R`. Existing native-board XY positions are not automatically re-packed by AE-074.

## Test-point disposition

`TP3004/TP3504` and `TP3005/TP3505` are retained to avoid unrelated physical churn. After removal of the common block they lie on the continuous SCH103 recovery-output / POST_EQ handoff and are renamed semantically as recovery-output and POST_EQ access points.

## Configuration disposition

- DR-039 becomes `CURRENT_ARCHITECTURE_QUALIFICATION_OPEN`.
- AE-067 remains immutable topology-selection evidence and continues to state that AE-067 itself did not imply product migration.
- The integrated selected-next contract records AE-074 as product-migration authority while preserving AE-067 as selection authority.
- `AE071-B02` is resolved by AE-074 after controlled native-PCB F8 reference relink, net audit and metadata reconciliation.
- Future final-design assurance moves from the reserved `AE-074_PENDING` placeholder to `AE-075_PENDING`.
- Final routing, layout freeze, BOM freeze and manufacturing release remain prohibited.

## Native PCB reconciliation evidence

KiCad's native `.kicad_pcb` remains the board owner. AE-074 completed the controlled F8 update using reference-designator relinking rather than global reannotation.

The reconciled native board preserves the accepted identities and positions:

- `C30060` at `99.605, 73.256`;
- `R30060` at `92.405, 80.279`;
- `C35060` at `206.605, 73.256`;
- `R35060` at `199.405, 80.279`.

The branch-local net result is symmetric:

- capacitor pad 2 remains `ROOT__POST_EQ_L/R`;
- capacitor pad 1 and paired 330 kOhm resistor pad 1 share the new DIRECT/BYPASS branch-local net;
- resistor pad 2 remains `0VA`.

`MH1`-`MH4` remain locked board-only objects and remain excluded from BOM/POS output. The board remains intentionally unrouted.

The F8 updater reported zero errors. Its six warnings were bounded to physical pads 1, 5 and 8 of `U103/U203`; those pads are NC on the OPA1655 SOIC-8 physical package and are therefore expected. The four migrated footprint `Function` fields were subsequently reconciled to the branch-local semantics by an exact metadata-only patch; position, ownership and net invariants were rechecked afterwards.

During schematic migration, using a negative `-90` degree symbol rotation for the left DR-039 return resistor caused a KiCad 9.0.7 hierarchical ERC regression (approximately 148 messages, including 56 errors). Re-expressing the geometrically equivalent rotation canonically as `270` degrees restored native hierarchical ERC to **0 errors / 0 warnings**. Regression tests now require SCH107 rotations to be one of `0/90/180/270` and reject collinear overlapping wires.

The post-F8 validator completed with exit code 0 after the full regression suite, current-decision audit, native-board audit and governed schematic validation. AE071-B02 is therefore closed by AE-074.

## Qualification boundary

AE-074 is an implementation event, not additional RUN04 evidence. The following remain open:

- RUN09 full-system noise;
- RUN10 sensitivity/tolerance and value engineering;
- RUN12 muted/live selector switching through the balanced output;
- prototype/bench correlation.

No manufacturing baseline is claimed.

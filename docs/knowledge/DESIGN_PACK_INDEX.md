# Project Shellac — Controlled Design Pack Index

**Working authority:** `develop` plus `config/decisions/current_decision_index.yaml`.

**Production authority:** a tagged `main` release after production/reproducibility gates close.

## 1. Current design baseline

Use first:
- implemented `generator/` source on `develop`;
- `config/decisions/current_decision_index.yaml`;
- `config/decisions/document_authority.yaml`;
- controlled BOM/procurement configuration;
- latest passing regression suite.

Current signal-chain status:
- DR-037: implemented;
- DR-038: implemented;
- DR-039: implemented;
- DR-040: implemented;
- AE-023: analytical production signal-chain closure complete;
- prototype measured acceptance: open.

## 2. Decision register

Current status:
- `config/decisions/current_decision_index.yaml`

Status semantics:
- `config/decisions/decision_status.yaml`

Authority classification:
- `config/decisions/document_authority.yaml`

Historical prose is retained as provenance and is not rewritten merely because a later state exists.

## 3. Assurance chain

AE-001 through AE-010: block-level history.
AE-011/012: end-to-end architecture and headroom.
AE-013/014: SCH101 precision redesign.
AE-015: full-chain noise/DC finding.
AE-016/A/B: failed migration and repair history.
AE-017/018: atomic migration and LT5400 physical contract.
AE-019/020: documentation-control structure.
AE-023: implemented production signal-chain analytical closure.
AE-024/025: production design-record reconciliation.

## 4. Production/commissioning

Still required:
- measured CMRR/noise/DC/overload/transient acceptance;
- final PCB/mechanical release;
- manufacturing release checklist;
- fabrication outputs frozen to a release commit;
- complete commissioning sheet;
- clean-clone reproducibility evidence.

## 5. Maintenance

Current signal-chain baseline:
`docs/maintenance/Signal_Chain_Commissioning_and_Maintenance_Baseline_Rev_A0.md`

## 6. Historical evidence rule

Superseded/staging records remain provenance and do not determine current hardware.

## 7. Change-control rule

Future implemented changes must update source/CAD, tests, current decision index,
assurance evidence, BOM/procurement and maintenance information together where applicable.

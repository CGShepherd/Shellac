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
- DR-037: current — complete canonical RIAA retained in SCH103; duplicate independent 3180 us stage removed;
- DR-038: architectural intent current — LT5400 precision SCH101 architecture retained; gain-selection implementation is under pre-SPICE reconciliation;
- DR-039: requirement current — AE-052 selects branch-local DC blocking as the preferred SPICE candidate: 1 uF / 330 kOhm only in the direct bypass branch, with the existing SCH107 high-pass branch providing intrinsic DC blocking; implementation remains pending full-system LTspice qualification;
- DR-040: current subject to the live implementation and subsequent assurance records;
- AE-041 Rev A1: current control authority — 3P4T switched-summing matrix and current top-cover control architecture;
- AE-042 through AE-064: current pre-SPICE assurance/evidence chain;
- prototype measured acceptance: open.

This is not yet a manufacturing baseline. The next intended configuration milestone is the **Shellac Pre-SPICE Architecture Baseline** after repository reconciliation, clean regression and configuration-control closure.

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
AE-023: implemented production signal-chain analytical closure at that historical state.
AE-024/025: production design-record reconciliation at that historical state.
AE-040B: historical/superseded control-authority state; retained as provenance.
AE-041 Rev A0: superseded intermediate DP4/A20403RNCG matrix authority; retained as historical provenance only.
AE-041 Rev A1: current 3P4T matrix and top-cover control authority.
AE-042: SCH101 pre-SPICE interim design authority.
AE-043: SCH103 pre-SPICE analysis.
AE-044: DR-039 / SCH107 coupled pre-SPICE review establishing that the common pre-split 1 uF / 330 kOhm block is materially loaded by SCH107 and requires architectural requalification.
AE-045: SCH104 pre-SPICE analysis.
AE-046: SCH105 pre-SPICE analysis.
AE-047: system headroom, power and ground pre-SPICE reconciliation.
AE-048: full-system SPICE qualification matrix.
AE-049: SPICE numerical acceptance criteria.
AE-050: SPICE execution package.
AE-051: pre-SPICE non-simulation issue reconciliation.
AE-052: DR-039 / SCH107 pre-SPICE architectural downselect; branch-local direct-path DC block is the preferred SPICE candidate while the existing SCH107 filtered branch provides intrinsic DC blocking. This is a preferred candidate, not implemented authority, until integrated qualification closes.
AE-053: LTspice/Python simulation-toolchain architecture; LTspice is the authoritative integrated analogue solver, Python is the controlled orchestration/extraction/acceptance/reporting layer, and the existing analytical Python remains an independent cross-check. Reference LTspice models shall not be silently rewritten.

AE-054 through AE-058 establish implemented LTspice/Python execution and analytical-correlation infrastructure. AE-059 reconciles configuration-control semantics without implementing AE-042 or AE-052.

AE-060 establishes the fail-closed integrated-model contract and model-source preflight. It does not claim that SHELLAC_TOP is yet implemented or qualified.

AE-061 establishes controlled model-source provenance, corrects the primary Grado cartridge identity to Prestige 78C, and keeps model ingestion fail-closed until artefacts are captured and verified.

AE-062 qualifies the locally acquired OPA1656, OPA161x/OPA1612, LT5400-7 and THAT1646 model sources against controlled hashes, exact subcircuit interfaces and LTspice smoke execution. Vendor payloads remain external to the repository pending redistribution review; 1N4004 provenance remains open.

AE-063 reconciles the live SCH108 clamp identity from generic axial 1N4004 to Vishay S1G, matching the existing SMA footprint, and qualifies the manufacturer S1G SPICE model as a controlled external reference. System phantom-fault qualification remains open.

AE-064 qualifies controlled behavioural electrical source equivalents for Grado Prestige 78C and Audio-Technica AT-VM95SP, adds a non-gating Grado Gold/8MZ compatibility model, and closes the integrated model-source gate. Cartridge body/return bench verification remains open and SHELLAC_TOP itself is not yet implemented.

AE-042 through AE-064 are assurance/evidence records. They do not by themselves constitute manufacturing release authority.

AE-048, AE-049 and AE-050 remain respectively the qualification, numerical-acceptance and execution authorities for the simulation campaign. AE-053 defines the toolchain architecture used to execute those authorities and does not replace them.

## 4. Production/commissioning

Still required:
- implementation of the integrated SHELLAC_TOP candidate-analysis model and genuine RUN00;
- integrated full-system configuration qualification following AE-059 reconciliation;
- Shellac Pre-SPICE Architecture Baseline configuration milestone;
- full-system LTspice qualification and sensitivity/value-engineering work;
- measured CMRR/noise/DC/overload/transient acceptance;
- cartridge terminal/isolation bench confirmation where required;
- grounding-population and phantom-energy closure;
- final PCB/mechanical release;
- manufacturing release checklist;
- fabrication outputs frozen to a release commit;
- complete commissioning sheet;
- clean-clone reproducibility evidence.

The intended simulation implementation sequence begins with toolchain implementation, RUN00 model sanity and analytical correlation before Monte Carlo or value engineering.

## 5. Maintenance

Current signal-chain baseline:
`docs/maintenance/Signal_Chain_Commissioning_and_Maintenance_Baseline_Rev_A0.md`

Maintenance documentation must be reconciled to the final electrically qualified implementation before manufacturing release.

## 6. Historical evidence rule

Superseded/staging records remain provenance and do not determine current hardware.

In particular, historical linked-stereo Lorlin/Grayhill control concepts and the historical 4P4 matrix must not override AE-041 Rev A1 or the current generator/BOM architecture.

## 7. Change-control rule

Future implemented changes must update source/CAD, tests, current decision index,
assurance evidence, BOM/procurement and maintenance information together where applicable.

No implemented functionality may exist without an explicit requirement or controlled design decision, and no controlled design decision may be treated as implemented without corresponding implementation evidence.

Reference LTspice models and vendor macro-models are controlled evidence inputs. They must not be silently rewritten; any wrapper, substitution, patch or behavioural replacement must be explicit, traceable and justified.

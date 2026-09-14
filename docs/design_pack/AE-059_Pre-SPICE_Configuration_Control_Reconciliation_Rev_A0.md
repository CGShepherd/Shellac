# Project Shellac — AE-059 Pre-SPICE Configuration-Control Reconciliation

**Revision:** A0  
**Status:** CONFIGURATION RECONCILIATION — NO ANALOGUE TOPOLOGY MIGRATION  
**Date:** 14 September 2026  
**Scope:** Reconcile current authority, live implementation semantics, executable governance and one selected grounding-population mismatch before the integrated SPICE campaign.

## 1. Purpose

AE-059 reconciles the controlled repository after the pre-SPICE assurance and simulation-toolchain increments. It does not qualify, implement or promote the selected-next SCH101 or DR-039/SCH107 architectures.

The governing distinction is:

- **live implementation** — the circuitry presently generated and regression-tested;
- **selected-next architecture** — a controlled design selection that still requires qualification and deliberate migration;
- **manufacturing baseline** — not yet established.

No selected-next analogue topology shall be migrated merely to make documents, tests or source appear superficially aligned.

## 2. Baseline guarded by this record

The recovery baseline for AE-059 is local `develop` at:

`8c88a88ecd39c9438a6215c8d32b5b3933cca0d5`

The historical production baseline remains the tagged `main` release recorded by `config/decisions/current_decision_index.yaml`.

AE-059 shall be applied only from the guarded recovery baseline and only with a clean tracked working tree.

## 3. Decisions retained without implementation change

### 3.1 DR-037

DR-037 remains `CURRENT_IMPLEMENTED`.

Complete canonical RIAA remains in SCH103. The independent downstream 3180 us stage remains removed.

### 3.2 DR-038 / SCH101

DR-038 remains `CURRENT_SELECTED_PENDING_IMPLEMENTATION`.

The live generator still contains the earlier service-link gain-programming network together with the implemented LT5400 4x differential converter. This live implementation remains valid regression subject matter but is not the selected-next gain-selection authority.

AE-042 remains the selected-next authority for the fail-safe removable-shunt topology, approximately 14/18/22 dB with the no-shunt state at approximately 18 dB.

AE-059 shall change status wording only. It shall not migrate the SCH101 gain network.

### 3.3 DR-039 / SCH107

DR-039 remains `CURRENT_REQUIREMENT_IMPLEMENTATION_REQUALIFICATION`.

The live implementation retains the common post-EQ 1 uF / 330 kOhm DC block before the SCH107 FILTER/BYPASS split.

AE-052 remains the selected-next preferred SPICE candidate: branch-local 1 uF / 330 kOhm blocking in the direct bypass branch while the SCH107 filtered branch provides intrinsic DC blocking.

AE-059 shall not migrate DR-039/SCH107 circuitry.

## 4. Mute architecture clarification

AE-041 Rev A1 remains the current matrix/top-cover control authority, but its statements that the output-mute design or mute topology remain unresolved are superseded by this record.

The selected and live mute architecture is:

- SW905: C&K 7201SYCBE;
- mechanical DPDT, break-before-make;
- one pole per channel;
- RUN connects the selected channel-mode signal to the corresponding THAT1646 input;
- MUTE connects the corresponding THAT1646 input to 0VA;
- the mute is immediately before the balanced output drivers;
- no relay;
- no timer;
- no comparator;
- no automatic power-sequencing or delay circuitry.

The normal operator sequence for a matrix change remains:

`MUTE -> change MATRIX -> RUN`

Only switching-transient magnitude and subjective/bench click performance remain qualification items. The topology itself is not open.

This clarification deliberately preserves the project principle of avoiding extraneous functionality.

## 5. Ground-bond population correction

The selected direct-bond build uses:

- R909 = 0 Ohm, fitted;
- C909 = DNP;
- D901 = DNP;
- D902 = DNP.

The C909 reference and footprint remain in the design as an alternative configuration option, but C909 shall be DNP in the selected direct-bond population.

This is a configuration/population correction, not an experimental topology change.

## 6. Simulation-toolchain authority

AE-053 defines the LTspice/Python architecture.

AE-054 through AE-058 establish implementation, early analytical correlation, LTspice correlation execution, Windows/LTspice compatibility and numerical-correlation closure.

Accordingly the earlier risk statement that no implemented LTspice toolchain exists is superseded.

What remains open is the integrated full-system `SHELLAC_TOP` qualification campaign defined by AE-048, AE-049 and AE-050.

AE-058 contains multiple revision-labelled records, including two A2-labelled documents serving different functions. AE-059 treats these as traceable companion evidence rather than silently renaming historical records:

1. compatibility/RUN00 correction lineage; and
2. numerical-correlation closure.

Future document-control increments should avoid reusing the same AE/revision pair for distinct records.

## 7. Executable governance reconciliation

The following configuration-control defects shall be corrected:

1. `decision_status.yaml` shall admit all statuses currently used by controlled authority.
2. `tools/audit_current_decision_index.py` shall validate the index rather than incorrectly requiring DR-038/DR-039 to be `CURRENT_IMPLEMENTED`.
3. authority-path tests shall verify that live/current evidence paths resolve.
4. deliberately deleted historical implementation utilities shall be represented as historical-deleted artefacts, not dangling live paths.
5. the project root README shall become project navigation rather than obsolete patch-transport instructions.
6. tests shall explicitly protect the selected mechanical mute and selected C909 DNP population.
7. analytical Python shall be described as a live-state regression/cross-check model, not final integrated qualification authority.

## 8. Explicit non-actions

AE-059 shall not:

- implement AE-042;
- implement AE-052;
- change nominal Shellac rails from +/-18 V;
- introduce relay, timer, comparator or automatic mute circuitry;
- alter the selected matrix topology;
- change RIAA networks;
- rewrite vendor/reference LTspice models;
- treat analytical Python as a substitute for integrated LTspice qualification;
- promote `develop` to `main`;
- push any Git branch automatically.

Shellac and Phoenix remain independent designs; Phoenix rail choices shall not be imported into Shellac.

## 9. Acceptance gates

Before an AE-059 commit is permitted:

1. branch is exactly `develop`;
2. starting HEAD is exactly `8c88a88ecd39c9438a6215c8d32b5b3933cca0d5`;
3. no unresolved merge state exists;
4. tracked working tree is clean before application;
5. the changed/staged path set equals the AE-059 allowlist;
6. current status vocabulary is internally valid;
7. all current/pre-SPICE authority paths resolve;
8. deliberately deleted historical artefacts are explicitly classified as deleted;
9. C909 is DNP while R909 remains 0 Ohm;
10. SW905 remains a mechanical DPDT signal/0VA selector immediately before THAT1646;
11. no relay/timer/comparator mute architecture is introduced;
12. full `pytest` passes;
13. `git diff --check` passes.

Real LTspice RUN00, deterministic verification and analytical correlation remain strongly recommended evidence gates before promotion of the pre-SPICE baseline, but AE-059 must not claim that those gates qualify the still-unimplemented AE-042 or AE-052 migrations.

## 10. Resulting state

After AE-059, the repository should describe one coherent state:

- current live circuitry remains regression-testable;
- selected-next circuitry remains explicitly pending qualification/migration;
- current control and mute intent is unambiguous;
- direct ground-bond population is represented correctly;
- implemented simulation infrastructure is acknowledged;
- configuration-control tools enforce the same semantics as the controlled records.

This establishes a trustworthy configuration-control starting point for the integrated SPICE campaign. It does not establish a manufacturing baseline.

# AE-053 — Shellac LTspice / Python Simulation Toolchain Architecture
**Project:** Shellac
**Status:** INTERIM / PRE-SPICE TOOLCHAIN AUTHORITY
**Date:** 2026-09-12

## 1. Purpose

Define the controlled simulation-toolchain architecture used to execute the Shellac SPICE campaign established by AE-048, AE-049 and AE-050.

AE-053 does not replace:
- AE-048 — qualification scope and required evidence;
- AE-049 — numerical acceptance criteria;
- AE-050 — run structure, canonical parameters/nodes, execution sequence and result package.

It defines how those authorities are implemented reproducibly.

## 2. Solver authority

LTspice is the authoritative integrated analogue solver for Shellac.

Claims involving integrated analogue node behaviour, device macro-model interaction, nonlinear/transient behaviour, convergence-dependent operating points, rail/fault interaction, noise or other solver-dependent effects shall be based on the controlled LTspice model and run output.

Python shall not be used as a substitute circuit solver for such claims.

## 3. Python authority

Python is the controlled orchestration, extraction, acceptance and reporting layer.

Python responsibilities include:
- generating explicit run configurations from controlled parameters;
- invoking LTspice in batch mode;
- capturing simulator/version and run metadata;
- extracting measurements from LTspice outputs;
- normalising results into structured tables;
- applying AE-049 acceptance thresholds;
- producing pass/fail summaries;
- producing controlled plots and comparison tables;
- correlating LTspice results against analytical expectations;
- recording anomalies without silently modifying reference models.

Python may generate wrapper netlists, parameter include files or run-control artefacts where this improves repeatability, provided the generated artefacts are traceable to controlled source and do not silently alter reference device models.

## 4. Independent analytical cross-check

Existing analytical Python remains an independent cross-check.

Its purposes are:
- expected-value calculations;
- first-order transfer-function checks;
- tolerance sensitivity estimates;
- regression comparison;
- detection of configuration or extraction errors;
- sanity checks before expensive simulation.

Analytical Python is deliberately independent of the authoritative LTspice integrated result path. Agreement increases confidence; disagreement creates an anomaly requiring resolution.

Analytical Python shall not be tuned merely to reproduce LTspice output without an explicit physical or modelling justification.

## 5. Reference-model control

Reference LTspice models, including vendor macro-models, shall not be silently rewritten.

For every external or reference model retain where practical:
- original filename;
- source/vendor;
- version or retrieval date;
- file hash;
- licence/usage note where relevant;
- known limitations.

Permitted integration methods, in order of preference:
1. use the reference model unchanged;
2. add a controlled wrapper/adaptor around the unchanged model;
3. apply an explicit, separately recorded compatibility patch;
4. use a documented behavioural substitute only where the reference model is unavailable or unsuitable.

Any patch or substitute must identify:
- what changed;
- why it was required;
- which claims it can and cannot support;
- correlation evidence where available.

The original reference file remains retained unchanged.

## 6. Controlled directory architecture

Implementation should follow AE-050's controlled simulation structure, with toolchain separation sufficient to distinguish source, generated artefacts and results.

Recommended structure:

`simulation/`
- `models/`
  - authoritative top-level and project subcircuits;
- `models/reference/`
  - unchanged vendor/reference models;
- `models/wrappers/`
  - controlled adaptors around reference models;
- `config/`
  - controlled run parameter sets and acceptance mappings;
- `runs/`
  - RUN00 onward run families;
- `scripts/`
  - Python orchestration/extraction/reporting;
- `generated/`
  - reproducible generated netlists/includes; not hand-edited authority;
- `results/`
  - structured extracted results and master CSV;
- `plots/`
  - controlled generated figures;
- `logs/`
  - LTspice stdout/stderr/run logs and anomaly evidence;
- `manifests/`
  - model hashes, tool versions and run provenance.

Exact repository paths may be refined during implementation, but authority separation shall be preserved.

## 7. Reproducibility contract

Every accepted simulation result shall be reproducible from:
- repository commit;
- controlled LTspice model set;
- reference-model manifest/hashes;
- Python environment/dependency record;
- LTspice version;
- run configuration;
- numerical/convergence settings;
- extracted raw result;
- acceptance criterion version.

A result without sufficient provenance is informative only and shall not close a qualification item.

## 8. RUN00 implementation priority

Toolchain implementation begins with AE-050 RUN00 — Model sanity.

Initial objective:
- prove the LTspice invocation path;
- prove parameter injection;
- prove reference-model resolution;
- prove canonical node availability;
- prove DC operating-point extraction;
- prove structured result generation;
- prove deterministic rerun;
- prove Python acceptance/report generation.

RUN00 shall stop the campaign on:
- convergence failure;
- unresolved model include;
- floating or impossible valid-state node;
- unexpected saturation;
- inconsistent parameter/configuration state;
- non-reproducible output.

No Monte Carlo or value-engineering work begins until RUN00 and analytical correlation are credible.

## 9. Analytical correlation gate

Before broad integrated qualification, correlate simple deterministic cases against independent analytical Python.

Minimum early correlation should include where applicable:
- simple RC corner checks;
- selected SCH101 nominal gain;
- direct-path DR-039 1 uF / 330 kOhm corner;
- known SCH107 nominal response;
- representative SCH103 transfer checkpoints;
- matrix arithmetic where resistive behaviour is analytically tractable.

Differences must be categorised as:
- expected model-fidelity difference;
- extraction/normalisation error;
- configuration error;
- model defect;
- analytical-model limitation;
- unresolved anomaly.

Unresolved material differences block progression.

## 10. Acceptance execution

Python shall apply AE-049 criteria from controlled data, not hard-coded undocumented thresholds distributed across scripts.

Where practical, acceptance limits should be represented in one controlled mapping or configuration layer and identified in each result record.

Automated pass/fail does not override engineering judgement for:
- macro-model limitations;
- convergence artefacts;
- numerical instability;
- physically implausible results;
- safety/absolute-maximum interpretation.

Such cases become explicit anomalies.

## 11. Deterministic-first rule

Execution shall preserve AE-048/AE-050 ordering:
1. configuration/model reconciliation;
2. RUN00 sanity;
3. deterministic block and integrated runs;
4. headroom/noise;
5. sensitivity;
6. selected Monte Carlo only after sensitivity identifies high-leverage cases;
7. switching/fault campaigns;
8. consolidated review.

Monte Carlo is not a substitute for deterministic model correctness.

Value engineering shall not begin from an unqualified or poorly correlated nominal model.

## 12. Change-control rule

Simulation findings may propose design changes, but the toolchain shall not silently mutate authoritative design or reference-model source.

Any design change resulting from simulation requires:
- anomaly/issue record;
- explicit candidate change;
- rerun against affected qualification cases;
- decision record where architecture changes;
- controlled implementation only after approval.

Generated files are evidence or build artefacts unless explicitly designated as authority.

## 13. Review perspectives

### QUAD
Review for functional minimalism, signal-path integrity, serviceability and avoidance of unnecessary circuitry. Reject toolchain complexity that does not improve confidence or traceability.

### HP / Agilent / Keysight
Review for metrology discipline: defined stimulus, controlled configuration, traceable extraction, repeatability, numerical validity and explicit uncertainty/model limits. Plot inspection alone is insufficient.

### Airbus civil TDA
Review for configuration control, requirements-to-evidence traceability, independence of verification, anomaly disposition, reproducibility and prohibition of uncontrolled source modification.

## 14. Initial implementation deliverables

Before progressing beyond RUN00, produce:
- LTspice version/toolchain record;
- Python environment/dependency record;
- reference-model manifest with hashes;
- top-level model skeleton;
- controlled parameter/config representation;
- batch invocation script;
- result extractor;
- AE-049 acceptance evaluator;
- structured RUN00 result record;
- analytical-correlation report;
- anomaly log;
- rerun/reproducibility instructions.

## 15. Gate relationship

The intended next configuration milestone is the **Shellac Pre-SPICE Architecture Baseline**.

AE-053 supports that milestone by defining the simulation architecture, but the milestone itself depends on completion of the current authority reconciliation and configuration-control closure.

After that baseline, implementation begins with the LTspice/Python toolchain, RUN00 and analytical correlation before Monte Carlo or value engineering.

## Confidence

- LTspice as authoritative integrated analogue solver: 99%
- Python as controlled orchestration/extraction/acceptance/reporting layer: 99%
- independent analytical Python retained as cross-check: 99%
- unchanged reference-model retention with explicit wrappers/patches: 100%
- RUN00 plus analytical correlation before Monte Carlo/value engineering: 100%
- AE-048/049/050 remain governing qualification/acceptance/execution authorities: 100%

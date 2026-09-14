# AE-054 — Shellac RUN00 Toolchain Implementation
**Project:** Shellac
**Status:** IMPLEMENTATION STAGING / PRE-SPICE INFRASTRUCTURE
**Date:** 2026-09-13

## 1. Purpose

Implement the first controlled repository artefacts required by AE-053 without
changing the authoritative Shellac analogue architecture.

This stage implements toolchain infrastructure only.

## 2. Implemented

- isolated `simulation/` hierarchy;
- LTspice executable discovery with `LTSPICE_EXE` override;
- controlled LTspice command-line arguments;
- YAML run/configuration and acceptance mappings;
- deterministic template rendering with unresolved-parameter rejection;
- SHA-256 model/input manifest generation;
- RUN00 include-resolution sanity model;
- LTspice batch invocation;
- native/captured log retention;
- scalar `.meas` extraction;
- AE-049-linked data-driven acceptance;
- structured CSV/JSON result evidence;
- deterministic rerun comparison;
- Python regression tests that do not require LTspice.

## 3. Explicit non-scope

This stage does not:
- implement the AE-042 fail-safe SCH101 14/18/22 dB gain network;
- implement the AE-052 DR039/SCH107 branch-local candidate;
- introduce vendor macro-models;
- claim integrated analogue qualification;
- alter the manufacturing baseline;
- start sensitivity, Monte Carlo, value engineering, switching or phantom-fault work.

## 4. RUN00 character

The initial RUN00 circuit is intentionally a minimal project-owned sanity circuit.
It proves the controlled invocation/config/include/extraction/acceptance path.

It is not the authoritative integrated `SHELLAC_TOP` model and supports no product
performance claim.

## 5. Progression gate

Before expanding RUN00 to the integrated Shellac model:
1. repository regression remains green;
2. `doctor` records the installed LTspice executable identity;
3. `manifest` completes;
4. `prepare RUN00` is deterministic;
5. real LTspice `run RUN00` succeeds;
6. `verify RUN00` proves repeatability;
7. any command-line/version incompatibility is corrected in controlled configuration;
8. initial reference macro-models are added unchanged with provenance.

Only then should integrated SCH101/SCH103/DR039-SCH107/SCH104/SCH105/SCH108 modelling begin.

## 6. Design-assurance review

### QUAD
The implementation is deliberately minimal and does not introduce circuit functionality.
Generated artefacts are separated from controlled source.

### HP / Agilent / Keysight
Stimulus/configuration, measurement extraction, acceptance limits and provenance are
machine-readable. Plot inspection is not used for RUN00 acceptance.

### Airbus civil TDA
Authority references are explicit, reference models are immutable by policy, generated
artefacts are distinguished from source, and failure to resolve configuration or
measurements stops the run.

## Confidence

- architecture conforms to AE-053 intent: 99%
- stage is isolated from analogue-design authority: 100%
- suitable as first RUN00 infrastructure increment: 98%
- installed-LTspice CLI compatibility pending execution on target machine: 85%

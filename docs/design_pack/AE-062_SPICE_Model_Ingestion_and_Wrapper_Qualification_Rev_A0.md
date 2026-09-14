# AE-062 — SPICE Model Ingestion and Wrapper Qualification — Rev A0

**Project:** Shellac
**Status:** PRE-SPICE MODEL INGESTION AND WRAPPER SMOKE QUALIFIED / NO PRODUCT-CIRCUIT MIGRATION

## 1. Purpose

AE-062 controls the locally acquired SPICE sources required for the first integrated Shellac model and introduces controlled Shellac-side wrappers. It does not migrate the product generator, complete `SHELLAC_TOP`, or promote integrated RUN00.

## 2. Qualified vendor sources

Four upstream sources passed direct LTspice parse/operating-point smoke testing:

- OPA1656 — TI macro model: `.SUBCKT OPA1656 IN+ IN- VCC VEE OUT`.
- OPA1612 — TI `OPA161x` macro model: `.SUBCKT OPA161x IN+ IN- VCC VEE OUT`.
- LT5400-7 — installed ADI LTspice model: `.SUBCKT LT5400-7 1 2 3 4 5 6 7 8 9`.
- THAT1646 — THAT Rev 05 model: `.SUBCKT THAT1646 OUT- SNS- GND IN Vee Vcc SNS+ OUT+`.

Exact archive/library/model hashes are controlled in `simulation/config/model_qualification.yaml`.

## 3. Wrapper policy and execution qualification

Vendor originals are not rewritten. Shellac wrapper files provide stable project interfaces. No vendor macro-model payload is added to the repository because redistribution permission has not yet been established.

Direct vendor-model smoke testing did not by itself qualify the Shellac wrappers. Wrapper-level LTspice execution was therefore treated as a distinct gate. `simulation/scripts/ae062_wrapper_smoke.py` exercised each `SHELLAC_*` wrapper against the already-qualified local source artefact; all four wrapper smoke cases passed before the controlled source states were promoted to `QUALIFIED_LOCAL_SOURCE` / `QUALIFIED_LOCAL_LIBRARY_SOURCE`.

## 4. Qualification semantics

Current AE-062 evidence establishes exact source provenance, controlled hashes, exact upstream subcircuit interfaces, verified wrapper pin mapping, successful direct vendor-model LTspice smoke execution, and successful LTspice execution through all four controlled Shellac wrappers.

This smoke qualification does not establish validity for every nonlinear, noise, overload, recovery, stability or fault mechanism in AE-049.

## 5. 1N4004 remains open

No explicit `1N4004` file or textual model entry was found in the installed LTspice library tree. Generic diode substitution shall not be used to close phantom-fault qualification.

## 6. Cartridge models

AE-062 does not close the cartridge-model items. AT-VM95SP has an official parameter source; Grado Prestige 78C remains secondary-corroborated with bench topology confirmation open.

## 7. Configuration-control boundary

AE-062 does not modify AE-050, does not migrate AE-042/AE-052 into the product generator, does not add automatic mute functionality, and does not alter the Shellac nominal rails from ±18 V.

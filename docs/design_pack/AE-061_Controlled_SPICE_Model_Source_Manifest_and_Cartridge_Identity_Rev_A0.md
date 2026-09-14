# AE-061 — Controlled SPICE Model-Source Manifest and Cartridge Identity Reconciliation
**Project:** Shellac  
**Status:** PRE-SPICE MODEL-SOURCE CONTROL / NO PRODUCT-CIRCUIT MIGRATION  
**Date:** 2026-09-14

## Purpose
Close the source-identification layer between AE-060 and the first genuine integrated `SHELLAC_TOP` model without overstating simulation readiness.

This record:
- corrects the primary Grado cartridge identity to the actual **Grado Prestige 78C** used by the project;
- resolves the generic SCH101 input-op-amp model role to **OPA1656**;
- identifies controlled upstream sources for OPA1656, OPA1612, LT5400-7 and THAT1646;
- records the intended 1N4004 model-control approach;
- records electrical source parameters for Grado 78C and Audio-Technica AT-VM95SP;
- deliberately leaves integrated RUN00 blocked until actual model artefacts/library entries are captured, hashed, wrapped and exercised.

## Configuration correction and supersession
AE-050 Rev A0 records Grado 78E as the primary Grado cartridge. That issued record is retained unchanged as provenance.

The project hardware baseline is Grado Prestige 78C. For all active simulation execution from AE-061 onward, **AE-061 supersedes AE-050 Rev A0 only with respect to the primary Grado cartridge identity**: use Grado Prestige 78C. All other AE-050 execution requirements remain in force unless separately superseded.

This is a configuration correction, not a change of cartridge hardware, and does not retrospectively rewrite AE-050.

Available historical/secondary specifications indicate 78C and 78E share the same nominal 47 kOhm load, 45 mH inductance and 475 Ohm source resistance, but that similarity is not used to justify retaining the wrong identity.

## Controlled source decisions

### OPA1656
Roles:
- SCH101 gain stages;
- SCH101 differential converter;
- SCH104 unity buffer;
- SCH105 output buffers.

Upstream source:
- Texas Instruments OPA1656 product support;
- `OPA1656 PSpice Model (Rev. C)`;
- package identifier `SBOMAW6C.ZIP`.

Status: `SOURCE_IDENTIFIED_PENDING_INGESTION`.

### OPA1612
Role:
- SCH103 active LF stage.

Upstream source:
- Texas Instruments OPA161x product support;
- `OPA161x PSpice Model (Rev. G)`;
- package identifier `SBOM396G.ZIP`.

Status: `SOURCE_IDENTIFIED_PENDING_INGESTION`.

### LT5400-7
Role:
- SCH101 precision matched-resistor differential converter network.

Upstream source:
- Analog Devices LT5400 product/LTspice library support;
- exact LT5400-7 instance/library representation to be captured from the controlled LTspice installation.

Status: `SOURCE_IDENTIFIED_PENDING_LIBRARY_CAPTURE`.

### THAT1646
Role:
- SCH108 balanced output driver.

Upstream source:
- THAT Corporation Device Models package;
- current public package identified as `File Revision 05`;
- exact THAT1646 subcircuit membership/name must be verified after package capture.

Status: `SOURCE_IDENTIFIED_PENDING_INGESTION`.

### 1N4004
Role:
- SCH108 phantom/fault rail clamps.

Decision:
- use a controlled LTspice/native or explicitly documented equivalent diode model;
- capture exact model text/provenance/hash used for qualification;
- do not imply that generic diode behaviour is sufficient for every fault-energy claim.

Status: `RESOLUTION_PATH_DEFINED_PENDING_CAPTURE`.

## Cartridge models

### Grado Prestige 78C — primary project cartridge
Model class: controlled behavioural source model.

Initial electrical values for SPICE source/loading work:
- source resistance: 475 Ohm;
- source inductance: 45 mH;
- recommended load: 47 kOhm;
- nominal output: 5 mV at 1 kHz, 5 cm/s where the cited secondary specifications use that convention.

Evidence quality:
- identity is project/hardware authority;
- electrical parameters are corroborated by multiple secondary Grado dealer/archive sources;
- manufacturer-primary electrical documentation has not yet been captured;
- body/return/isolation topology remains a bench-verification item.

Status: `PARAMETERS_IDENTIFIED_BENCH_TOPOLOGY_OPEN`.

### Audio-Technica AT-VM95SP — compatibility/secondary 78 rpm cartridge
Model class: controlled behavioural source model.

Official Audio-Technica values:
- source resistance: 485 Ohm DC;
- source inductance: 550 mH at 1 kHz;
- recommended load: 47 kOhm;
- recommended load capacitance: 100–200 pF;
- nominal output: 2.7 mV at 1 kHz, 5 cm/s.

Status: `PARAMETERS_IDENTIFIED_OFFICIAL_SOURCE`.

## Model-file control rule
Vendor model contents are not copied into the repository by AE-061.

Before a model may become `RESOLVED`, the project must record:
1. source URL/vendor;
2. vendor revision or package identifier;
3. captured local filename/library location;
4. SHA-256 of the captured artefact or exact controlled library extract;
5. subcircuit/model name and pin order;
6. wrapper mapping;
7. licensing/redistribution disposition;
8. minimum sanity regression.

Any compatibility edit must occur in a project-owned wrapper or explicitly documented patched derivative; vendor/reference originals must not be silently rewritten.

## Fail-closed rule
`simulation/scripts/integrated_preflight.py` must continue to return blocked status while any required source is not `RESOLVED`.

Source identification is not model qualification.

## Explicit non-actions
AE-061 does **not**:
- implement AE-042 in the product generator;
- implement AE-052 in the product generator;
- change the ±18 V Shellac rail authority;
- change EQ values, matrix behaviour or mute topology;
- add automatic sequencing;
- claim `SHELLAC_TOP` exists;
- claim any vendor model has already been captured or validated;
- promote `develop` to `main`.

# AE-063 — SCH108 SMA Clamp and SPICE Model Reconciliation — Rev A0

**Project:** Shellac
**Status:** ACTIVE CONFIGURATION RECONCILIATION / PRE-SPICE REFERENCE MODEL QUALIFIED / SYSTEM FAULT QUALIFICATION OPEN

## 1. Purpose

AE-063 resolves an active configuration inconsistency in SCH108: the live generator identified the phantom/fault rail clamps as `1N4004` while assigning them an SMA surface-mount footprint. A conventional 1N4004 is an axial DO-41 rectifier, so the electrical identity and physical implementation were not coherent.

AE-063 reconciles the live design to a 1 A / 400 V standard rectifier that is physically compatible with the existing SMA geometry: Vishay General Semiconductor S1G.

## 2. Active hardware reconciliation

The live SCH108 clamp identity changes from generic `1N4004` to `S1G`.

The already-selected PCB footprint remains:

`Diode_SMD:D_SMA`

The controlled BOM records:
- manufacturer family: Vishay General Semiconductor;
- device family: S1G;
- package: SMA / DO-214AC;
- nominal class: 1 A / 400 V standard rectifier;
- quantity: 8;
- exact procurement/tape-reel order suffix: open until BOM freeze.

This is a component-identity correction to make the live electrical and physical representations coherent. It does not change the clamp topology or the nominal ±18 V Shellac rails.

## 3. Controlled SPICE reference

The Vishay S1G manufacturer model was acquired from:

`https://www.vishay.com/docs/89655/s1g.txt`

Controlled SHA-256:

`ffd79ea06d6ab712987b44e577c8787dbe54d25a90de58e3f6901a1b89642ed4`

The model declares:

`.MODEL s1g D ...`

A local LTspice operating-point smoke test completed successfully with return code 0.

The vendor payload is not committed to the repository pending redistribution review. The active manifest therefore records a controlled external reference plus exact hash and direct-use semantics.

## 4. Qualification boundary

AE-063 establishes:
- coherent SCH108 clamp electrical/physical identity;
- controlled manufacturer model provenance;
- exact model hash;
- successful LTspice model execution;
- direct-use model interface control.

AE-063 does **not** establish:
- phantom-fault survival;
- rail-injection acceptability;
- clamp pulse-energy capability in the complete Shellac network;
- reverse-recovery significance under every AE-049/AE-050 fault case;
- final equivalence of every procurement suffix/lot;
- integrated `SHELLAC_TOP` qualification.

Those remain system-level simulation and bench obligations.

## 5. Historical provenance

AE-048, AE-050, AE-061 and AE-062 references to `1N4004` remain unchanged historical evidence. AE-063 supersedes the generic `1N4004` identity only for active configuration and future integrated simulation execution.

The exploratory Diodes Incorporated 1N4004 model acquisition is investigation evidence only and is not the selected Shellac reference model.

## 6. Explicit non-actions

AE-063 does not:
- alter the THAT1646 topology;
- alter mute behaviour;
- add automatic sequencing;
- change the ±18 V Shellac rail authority;
- implement AE-042 or AE-052;
- claim fault-energy closure;
- promote `develop` to `main`.

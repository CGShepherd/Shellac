# Project Shellac — AE-060 Integrated SPICE Model Contract and Preflight

**Revision:** A0
**Status:** PRE-SPICE MODEL-CONTRACT / NO PRODUCT-CIRCUIT MIGRATION
**Date:** 14 September 2026
**Baseline:** `develop` at `40a95200e2fb81b7772c1e583310fd059380e855`

## Purpose

AE-060 is the controlled bridge from the proven LTspice/Python toolchain to the first real integrated `SHELLAC_TOP` model. It does not claim that an integrated model already exists.

The integrated qualification model is a **candidate-analysis model** where AE-048/050 require selected-next architecture:
- SCH101 uses the AE-042 fail-safe removable-shunt 14/18/22 dB candidate.
- DR-039/SCH107 exposes controlled LF candidate variants including the AE-052 preferred branch-local direct-path DC block.
- The product generator remains unchanged until a later controlled migration decision.
- Passing simulation does not by itself make a candidate implemented hardware.

The required top level is `SHELLAC_TOP`, with the AE-050 hierarchy, canonical nodes and global parameter vocabulary.

Before integrated RUN00 is accepted, every required active-device or source model must be a controlled vendor/reference model with source/version/hash or a documented behavioural substitute with explicit limitations.

The existing divider RUN00 remains valid toolchain evidence but is **not** integrated-system RUN00.

AE-060 shall not change generator circuitry, migrate AE-042 or AE-052, change nominal Shellac rails from +/-18 V, add relay/timer/comparator/automatic mute circuitry, alter EQ/matrix topology, or claim SIMULATED status.

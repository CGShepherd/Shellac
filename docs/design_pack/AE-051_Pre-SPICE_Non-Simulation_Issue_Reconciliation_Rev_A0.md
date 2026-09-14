# AE-051 — Pre-SPICE Non-Simulation Issue Reconciliation
**Project:** Shellac
**Status:** INTERIM / PRE-SPICE CONFIGURATION RECONCILIATION
**Date:** 2026-09-11

## Purpose
Close or correctly classify outstanding issues that do not require SPICE evidence before the simulation campaign begins.

---

## 1. Control-authority conflict

### Finding
AE-040B is superseded by later controlled authority.

AE-040B still states:
- linked-stereo 2P5 Bass/Treble;
- Lorlin PT preferred;
- 4P4 Channel Mode concept.

AE-041 A1 and the live generator/BOM now state:
- four independent Bass/Treble controls, one per channel;
- NKK NR01 family for EQ controls;
- 3P4T C&K A30403RNCB matrix, TE MRJE3404 fallback;
- front-to-rear top-cover sequence retained.

### Disposition
**CLOSED AT ARCHITECTURE LEVEL.**

Current authority:
- AE-041 A1 + live generator/model/control_architecture.py + controlled BOM.

AE-040B shall remain historical provenance and shall not be used for procurement or manufacturing release.

### EQ rotary exact MPN
The NR01 electrical requirement is:
- SP5T;
- 5 fixed positions;
- BBM / non-shorting;
- gold contacts;
- straight PCB terminals;
- quantity one procurement.

NKK NR01105ANG13 satisfies those electrical requirements and is available as a no-knob base variant.

However:
- the final panel/PCB stack;
- usable actuator projection;
- external knob retention;
- final chosen knurled-knob compatibility;
- final drilling/registration

remain mechanical release items.

Therefore the exact production EQ rotary MPN remains:
**FAMILY SELECTED / EXACT MPN OPEN.**

Do not prematurely freeze NR01105ANG13 until the top-cover stack is mechanically checked.

---

## 2. AT-VM95SP balanced-input compatibility

### Published evidence
Audio-Technica documentation identifies four output terminals:
- white: left +
- blue: left -
- red: right +
- green: right -

Published electrical data:
- output 2.7 mV at 1 kHz, 5 cm/s;
- DC resistance 485 Ohm;
- inductance 550 mH;
- recommended load 47 kOhm;
- recommended capacitance 100–200 pF.

This is strongly consistent with use as a floating two-channel source into Shellac's differential left/right inputs.

### Remaining evidence gap
The manufacturer documentation located does not explicitly guarantee:
- infinite DC resistance between L- and R-;
- no internal connection from either return to cartridge body/shield.

### Disposition
**PRIMARY QUALIFICATION CARTRIDGE — ELECTRICALLY COMPATIBLE SUBJECT TO BENCH CONTINUITY CHECK.**

Before prototype qualification:
1. measure L+ to L-;
2. measure R+ to R-;
3. measure L- to R-;
4. measure every terminal to cartridge body;
5. record values.

Acceptance for Shellac balanced use:
- each coil measures plausibly close to published DC resistance;
- no unintended low-resistance L-/R- common;
- no low-resistance terminal-to-body bond.

If returns are internally common, Shellac may still operate electrically but it is no longer a fully floating differential-source qualification case and shall be modelled/documented accordingly.

---

## 3. Grado 78E compatibility

### Published evidence
Current third-party product data consistently identifies the legacy Grado 78E as approximately:
- 5 mV output;
- 475 Ohm resistance;
- 45 mH inductance;
- 47 kOhm load;
- 78-rpm cartridge.

Current Grado public product pages no longer expose a detailed 78E product record, so manufacturer-level evidence for terminal topology was not located.

The cartridge is frequently described as "mono", but that label alone does not establish whether:
- the body contains two independent coils;
- the returns are internally common;
- channels are strapped internally;
- only the stylus/generator response is mono.

### Disposition
**PRIMARY 78-RPM INTENT RETAINED / BALANCED TERMINAL TOPOLOGY REQUIRES BENCH CONFIRMATION.**

Required continuity check:
1. identify all four cartridge terminals;
2. L+ to L-;
3. R+ to R-;
4. L- to R-;
5. L+ to R+;
6. each terminal to body.

Do not assume the older Grado 78C/78E proxy is a fully floating stereo electrical model until measured.

---

## 4. 0VA-to-CHASSIS network

Live SCH106 fits:
- R909 = 0 Ohm direct 0VA-to-CHASSIS bond;
- C909 = 100 nF in parallel;
- D901/D902 opposed clamps DNP.

### Finding
With R909 = 0 Ohm fitted, C909 is electrically bypassed by the direct bond.

### Disposition
- R909: **RETAIN PROVISIONALLY**
- C909: **DNP IN DIRECT-BOND BUILD**
- D901/D902: **DNP**
- direct-bond versus alternative lift configuration: final bench/hum/EMC evidence item.

The C909 footprint may remain only as an explicit alternative-configuration provision. It should not be populated in the selected direct-bond configuration.

---

## 5. Controlled-register staleness

### Risk Register
The current Risk Register is materially stale:
- R-002 incorrectly says Grayhill Bass/Treble is selected;
- R-003 incorrectly says Grayhill 4P4 Channel Mode is selected;
- R-015 still treats duplicate RIAA as open-blocking although DR-037 superseded it.

### Current decision index
The decision index is also behind the live design:
- DR-038 describes the earlier service-link gain implementation rather than the selected fail-safe shunt topology;
- DR-039 is labelled CURRENT_IMPLEMENTED despite AE-044 showing the requirement remains valid but the present implementation requires requalification;
- AE-041 A1 matrix/control authority is not represented.

### Design Pack Index
The index stops its assurance-chain summary around AE-025 and describes DR-039 as implemented without the later requalification finding.

### Disposition
**CONFIGURATION-CONTROL PATCH REQUIRED BEFORE BASELINE OR MANUFACTURING RELEASE.**

This is documentation/configuration debt, not evidence that the live circuit should revert.

Recommended patch target:
1. Risk Register;
2. current_decision_index.yaml;
3. DESIGN_PACK_INDEX.md;
4. document authority if needed;
5. BOM notes where configuration state changes.

Do not patch these controlled files until an explicit reconciled change set is prepared and approved.

---

## 6. Pre-SPICE closure table

| Item | Disposition |
|---|---|
| Linked-stereo Lorlin vs dual-mono NKK conflict | CLOSED — AE-041 A1/live model wins |
| Matrix 4P4 vs 3P4T conflict | CLOSED — 3P4T A30403RNCB preferred |
| Exact EQ rotary MPN | OPEN — mechanical stack/knob confirmation |
| AT-VM95SP four-terminal topology | DOCUMENTED |
| AT-VM95SP internal return/body isolation | BENCH CHECK |
| Grado 78E published R/L/V values | SUFFICIENT FOR PRELIMINARY MODEL |
| Grado 78E terminal topology/isolation | BENCH CHECK |
| R909 direct bond | RETAIN PROVISIONALLY |
| C909 with R909 fitted | DNP |
| Ground-lift clamps | DNP |
| Risk/decision/design-pack registers | STALE — CONTROLLED PATCH REQUIRED |

---

## Confidence
- AE-041 A1 supersedes AE-040B for current control architecture: 100%
- NKK NR01 family electrically suitable for EQ control: 99%
- exact EQ MPN should remain open pending mechanical stack: 98%
- AT-VM95SP has four separately identified L+/L-/R+/R- terminals: 100%
- AT-VM95SP internal isolation requires bench confirmation: 98%
- Grado 78E electrical source values adequate for preliminary modelling: 95%
- Grado 78E terminal topology requires measurement: 99%
- C909 redundant when R909=0 Ohm is fitted: 100%
- controlled registers are stale relative to live architecture: 100%

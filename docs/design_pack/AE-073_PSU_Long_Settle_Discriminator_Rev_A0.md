# AE-073 — PSU RUN01 Long-Settle Discriminator and Simulation Disposition

**Revision:** A0  
**Date:** 2026-09-24  
**Repository baseline:** `8c0a77cd19464e3081cedb4e40552c95ebae9fd4` (`develop`)  
**Scope:** AIYIMA LM317/LM337 + LF353 servo PSU P1-V model  
**Status:** SIMULATION DISCRIMINATOR CLOSED; POWERED HARDWARE QUALIFICATION OPEN

## 1. Purpose

AE-073 resolves the apparent contradiction produced by the exploratory 400 ms RUN01 PSU simulations.

At 400 ms, the model appeared to show a maximum regulated output of only about ±15.6 V even with the 5 kΩ programming resistance at its maximum. That result conflicted with the reconstructed circuit topology, analytical LM317/LM337 set-point behaviour, and existing physical experience with the same PSU/transformer family.

The specific discriminator was therefore:

> Is the 400 ms result a real DC adjustment ceiling, or is it a startup-settling artefact caused by the LF353 servo remaining saturated while the AC-coupled sense/feedback network charges?

AE-073 extends the same controlled composed model to 8 s and observes the regulated outputs, raw rails, regulator ADJ nodes, LF353 outputs, and servo error nodes at progressively later windows.

## 2. Authority and model provenance

The simulation is based on the controlled P1-V reconstruction at repository baseline:

`8c0a77cd19464e3081cedb4e40552c95ebae9fd4`

Relevant controlled material at that baseline includes:

- `simulation/psu/config/p1v.yaml`
- `simulation/psu/config/model_sources.yaml`
- `simulation/psu/models/wrappers/`
- `simulation/psu/RUN00_QUALIFICATION.md`

The composed decks embed the SHA-verified vendor macromodel payloads used by the controlled PSU model flow.

Toolchain observed in the retained logs:

- LTspice 26.0.2 for Windows
- Python 3.13 environment used by the Shellac repository

This record does **not** upgrade the P1-V model to powered-hardware authority. The physical PSU remains pending bench validation.

## 3. Pre-discriminator evidence: 400 ms RUN01

The exploratory 400 ms load/trim sweep produced the following representative results at a 170 Ω load per rail:

| Programming resistance | +VOUT average | -VOUT average |
| ---: | ---: | ---: |
| 2160 Ω | +7.5697 V | -7.4929 V |
| 2260 Ω | +7.8537 V | -7.7767 V |
| 5000 Ω | +15.6040 V | -15.5256 V |

The corresponding 400 ms servo-topology observations showed the LF353 outputs still strongly displaced from zero:

| Programming resistance | OP (U1B output) | ON (U1A output) |
| ---: | ---: | ---: |
| 2160 Ω | -5.9695 V | +6.0468 V |
| 2260 Ω | -6.2533 V | +6.3308 V |
| 5000 Ω | -14.0022 V | +14.0817 V |

At the representative 2260 Ω point, each LF353 output is approximately 1.52 V from its corresponding supply rail. The same saturation signature persists across the exploratory sweep. The 400 ms results are therefore not valid evidence of the settled DC adjustment ceiling.

The compact pre-discriminator summaries are retained as:

- `run01_400ms_load_trim_summary.csv`
- `run01_400ms_servo_topology_summary.csv`

## 4. Long-settle discriminator

Three cases were executed to 8 s:

1. **as_found_nominal_rprog**  
   RSET+ = 2260 Ω, RSET- = 2160 Ω, programming resistors = 220 Ω / 220 Ω.

2. **as_found_measured_rprog**  
   RSET+ = 2260 Ω, RSET- = 2160 Ω, measured programming resistors = 219 Ω / 216 Ω.

3. **target17_estimate**  
   RSET+ = 2735 Ω, RSET- = 2691 Ω, measured programming resistors = 219 Ω / 216 Ω.  
   These RSET values are analytical investigation values only; they are not frozen production values.

Observation windows were centred on approximately 0.4 s, 1 s, 2 s, 4 s and 8 s.

### 4.1 Settled 7.9–8.0 s results

| Case | +VOUT | -VOUT | OP | ON | +RAW | -RAW |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| as_found_nominal_rprog | +14.0800 V | -13.5120 V | -0.01435 V | +0.01371 V | +19.2938 V | -19.3209 V |
| as_found_measured_rprog | +14.1385 V | -13.7388 V | -0.01443 V | +0.01394 V | +19.2905 V | -19.3089 V |
| target17_estimate | **+16.8434 V** | **-16.8045 V** | **-0.01814 V** | **+0.01799 V** | +19.1606 V | -19.1617 V |

All three simulations returned `rc=0`.

At the late window the prior saturation signature is absent. The LF353 outputs have converged to approximately zero, rather than remaining about 1.52 V from the rails.

### 4.2 Target-17 V convergence

The target-17 V investigation case progressed as follows:

| Window | +VOUT | -VOUT | OP | ON |
| --- | ---: | ---: | ---: | ---: |
| ~0.4 s | +9.2761 V | -9.1028 V | -7.5794 V | +7.7533 V |
| ~1.0 s | +9.6376 V | -9.6315 V | -6.8727 V | +6.8422 V |
| ~2.0 s | +13.7687 V | -13.7459 V | -2.9394 V | +2.9264 V |
| ~4.0 s | +16.2949 V | -16.2596 V | -0.5391 V | +0.5360 V |
| ~8.0 s | **+16.8434 V** | **-16.8045 V** | **-0.01814 V** | **+0.01799 V** |

The temporal behaviour is coherent with recovery from a long startup transient in the LF353 servo path.

## 5. Discriminator result

**PASS — startup-transient hypothesis confirmed.**

The earlier apparent ~±15.6 V ceiling was caused by interpreting the still-settling 400 ms state as a DC operating point.

The evidence supports the following engineering conclusions:

1. The 400 ms RUN01 result is **not** a demonstrated DC output-voltage ceiling.
2. The LF353 servo recovers from its startup saturated state and converges close to zero output in the 8 s model.
3. The controlled model can reach the vicinity of ±17 V with plausible programming resistance values.
4. No further LF353 model investigation or simplified fallback discriminator is justified before powered hardware correlation.
5. The model should **not** be tuned to force an exact ±17.000 V result. The remaining difference is small relative to the uncertainty of the physical transformer, regulator references, component tolerances, and vendor macromodels.

## 6. Important non-closures

AE-073 does **not** demonstrate that the physical PSU is fully qualified for Shellac.

In the target-17 V case, the late raw rails are approximately ±19.16 V while the regulated outputs are approximately ±16.82 V, giving only about 2.3 V average regulator differential in this model. Because the transformer representation is intentionally approximate, this is a **bench-measurement requirement**, not a simulation failure and not a demonstrated dropout pass.

The following remain open until powered hardware qualification:

- actual ±17 V set-point capability and adjustment range;
- raw-rail DC voltage and ripple troughs at representative load;
- regulated output ripple;
- startup and overshoot behaviour;
- LM317/LM337 temperature under representative load;
- acceptable dropout margin under real mains/transformer conditions;
- final range-limiting resistor values, if range limiting is retained;
- final disposition of regulator protection diodes;
- formal reconciliation of the historical Shellac ±18 V requirement with the investigated ±17 V operating point.

## 7. Planned powered qualification

When the ordered load components are available, the physical PSU will be tested conservatively before any design freeze.

The currently intended 330 Ω / 10 W load set gives approximately:

- one 330 Ω resistor per rail at 17 V: ~51.5 mA/rail;
- two 330 Ω resistors in parallel per rail: ~103 mA/rail.

The powered session will record at minimum:

- regulated + and - output voltage;
- raw + and - rail DC voltage;
- raw-rail ripple and trough;
- regulated-output ripple;
- startup/overshoot;
- regulator case/heatsink temperature after stabilisation.

A material failure of regulation, dropout, noise, startup, or thermal margin will stop the AIYIMA qualification path. A satisfactory result will freeze the PSU choice and return engineering effort to the main Shellac build.

## 8. Retained compact evidence

Controlled evidence directory:

`simulation/psu/evidence/ae073_long_settle/`

Retained files:

- `AE073_RUN01_LONG_SETTLE_DISCRIMINATOR.py`
- `long_settle_summary.csv`
- `run01_400ms_load_trim_summary.csv`
- `run01_400ms_servo_topology_summary.csv`
- `as_found_nominal_rprog.cir`
- `as_found_nominal_rprog.log`
- `as_found_nominal_rprog_combined.txt`
- `as_found_measured_rprog.cir`
- `as_found_measured_rprog.log`
- `as_found_measured_rprog_combined.txt`
- `target17_estimate.cir`
- `target17_estimate.log`
- `target17_estimate_combined.txt`

Large LTspice `.raw`, `.db`, caches and duplicated exploratory diagnostics are intentionally excluded from the controlled evidence package. They are generated artefacts, not required to reproduce or audit the engineering conclusion.

## 9. Disposition

**AE-073 simulation discriminator: CLOSED / PASS.**

**AIYIMA P1-V powered qualification: OPEN.**

No production release, PCB routing release, or Shellac rail-authority change is made by this record.

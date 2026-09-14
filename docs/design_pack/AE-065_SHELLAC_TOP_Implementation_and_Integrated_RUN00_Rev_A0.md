# AE-065 — SHELLAC_TOP Implementation and Integrated RUN00 — Rev A0

**Project:** Shellac
**Status:** INTEGRATED MODEL IMPLEMENTED / NOMINAL RUN00 SANITY PASSED / FULL QUALIFICATION OPEN
**Execution baseline:** `develop` commit `e83eee5a16ac35ef81046f93e9b37ffd5ce83f3b`

## 1. Purpose

AE-065 implements the first genuine integrated `SHELLAC_TOP` electrical candidate-analysis model and executes the first genuine integrated RUN00 sanity gate defined by AE-048, AE-049 and AE-050.

The model remains `SELECTED_NEXT_CANDIDATE_ANALYSIS`. AE-065 does not migrate AE-042 or AE-052 into the live product generator and does not create manufacturing authority.

## 2. Controlled nominal vector

The executed vector is:

- Grado Prestige 78C;
- SCH101 DEFAULT/no-shunt approximately 18 dB state;
- complete RIAA: TRUE-RIAA LF branch plus 2121 Hz treble;
- rumble BYPASS;
- AE-052 branch-local 1 uF / 330 kOhm direct-path DC block;
- STEREO matrix state;
- SW905 RUN;
- 100 pF differential cartridge cable capacitance;
- BASE additional cartridge-capacitance state;
- 100 kOhm balanced output load;
- nominal +18 V / -18 V rails;
- direct 0VA-to-CHASSIS nominal representation.

Cartridge generated EMF is zero for RUN00 while preserving the floating two-terminal behavioural-source semantics.

## 3. Controlled model provenance

RUN00 used the exact previously qualified model hashes for OPA1656, OPA1612, THAT1646, Vishay S1G and LT5400-7. Vendor macro-model payloads remain external to Git in accordance with AE-062 redistribution controls. No unqualified substitution was accepted.

## 4. RUN00 acceptance

AE-050 defines RUN00 as structural/operating-point sanity: convergence, no impossible valid-state node condition, no uncontrolled floating state and no unexpected saturation. AE-049 provides the XLR DC acceptance limits.

For this deliberately narrow gate:

- representative internal nodes must remain within +/-1 V of 0VA; this is a gross-bias/saturation sanity bound, not an offset specification;
- XLR differential DC must be <=25 mV magnitude;
- XLR common-mode DC must be <=250 mV magnitude;
- LTspice must return successfully with no controlled fatal/convergence term.

## 5. Executed result

| Measurement | Result | RUN00 limit | Disposition |
|---|---:|---:|---|
| N101_L output | +2.5009 mV | +/-1 V | PASS |
| N103_L output | +215.6354 mV | +/-1 V | PASS |
| N104_L output | +0.4969 mV | +/-1 V | PASS |
| N105_L output | +1.0365 mV | +/-1 V | PASS |
| N108_L input | +1.0365 mV | +/-1 V | PASS |
| XLR L differential | -1.9083 mV | +/-25 mV | PASS |
| XLR L common mode | -0.5850 mV | +/-250 mV | PASS |
| XLR R differential | -1.9083 mV | +/-25 mV | PASS |
| XLR R common mode | -0.5850 mV | +/-250 mV | PASS |

LTspice return code was 0. All nine controlled checks passed. The structured evidence record is `simulation/results/run00_sanity/ae065_integrated_run00.json`.

### SCH103 DC observation

`N103_L` is approximately +215.6 mV with zero generated cartridge EMF. This is well inside the deliberately loose RUN00 gross-saturation bound, but AE-065 does not interpret it as ideal or production-qualified DC performance. The AE-052 branch-local direct-path capacitor reduces the downstream `N104_L` DC to approximately +0.497 mV. SCH103 DC/headroom behaviour remains part of the later integrated qualification campaign under R-024.

## 6. Numerical-model boundaries

For RUN00 only:

1. each THAT1646 sense capacitor has a 1 GOhm parallel numerical leakage path to establish a finite DC solution; this is not a product BOM item;
2. each output ferrite is represented by a 0.05 Ohm DC equivalent; frequency-dependent ferrite behaviour is deferred to RUN06;
3. ideal nominal +/-18 V sources are appropriate to the nominal sanity vector; non-ideal rail/ripple and fault behaviour remain later-run work.

## 7. What AE-065 does not establish

AE-065 does not qualify RIAA/replay-curve frequency accuracy, cartridge loading/HF response, CMRR, rumble response, all matrix/control states, output capacitive-load stability, headroom and overload/recovery, noise, tolerance or Monte Carlo sensitivity, switching transients, rail/ripple sensitivity, or phantom-power fault survival.

Those remain within RUN01-RUN14 and the wider AE-048/049/050 campaign.

## 8. Risk/configuration disposition

A passing genuine integrated RUN00 mitigates R-026 because `SHELLAC_TOP` now exists and executes coherently.

R-020 remains `OPEN_SYSTEM_QUALIFICATION`.
R-021 remains `VERIFY_ON_BENCH`.
R-024 remains `OPEN_SYSTEM_QUALIFICATION`.
R-018 and R-019 remain pending product implementation/qualification; candidate-analysis use in the integrated SPICE model is not generator migration.

Shellac nominal rails remain +/-18 V. Mechanical input mute authority and absence of automatic sequencing are unchanged.

No `main` promotion is authorised by AE-065.

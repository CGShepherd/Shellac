# AE-066 — Integrated AC RUN01–RUN03 and Infrastructure Consolidation — Rev A0

**Project:** Shellac
**Status:** PASS_WITH_GRADO_EXTENDED_BAND_OPEN
**Execution baseline:** `269f1273993ac40ccb51f6cab54fc46daf02e091`

## 1. Purpose

AE-066 executes the first substantial integrated AC tranche after AE-065 RUN00: RUN01 cartridge/loading, RUN02 SCH101 gain/CMRR and RUN03 all 25 SCH103 Bass x Treble states. It also establishes reusable exact-hash model acquisition/parsing infrastructure and prepares controlled component/model candidates for RUN04-RUN06.

The work remains `SELECTED_NEXT_CANDIDATE_ANALYSIS`. No product-generator or CAD migration is authorised by this record.

## 2. RUN01 — cartridge/loading

Executed 45 combinations across Grado Prestige 78C, Audio-Technica AT-VM95SP and non-gating Grado Gold/8MZ compatibility; cable capacitance 50/100/150/200/300 pF; service capacitance BASE/+47/+100 pF.

Disposition: **PARTIAL_GRADO_EXTENDED_BAND_MODEL_VALIDITY_OPEN**.

The AT-VM95SP cases inside its official 100-200 pF bookkeeping envelope all meet the AE-049 +1 dB below 20 kHz / +2 dB below 50 kHz peaking limits.

The nominal Grado 78C 100 pF cable / BASE state meets the below-20-kHz AE-049 criterion. Its extended 20-50-kHz R-L-only model result does not meet the +2 dB criterion. Where it does not meet, AE-066 does not waive AE-049: extended-band qualification remains open because the AE-064 model does not contain manufacturer-authoritative cartridge self-capacitance/mechanical high-frequency behaviour. R-021/R-024 remain open.

The qualification matrix is therefore allowed to reject particular cable/service combinations; AE-042 explicitly made BASE/+47/+100 pF provisional pending this sweep.

## 3. RUN02 — SCH101 gain/CMRR

Disposition: **QUALIFIED_NOMINAL**.

| State | Gain @1 kHz | CMRR 20 Hz | CMRR 1 kHz | CMRR 20 kHz | Pass |
|---|---:|---:|---:|---:|---|
| LOW | 13.9372 dB | 120.90 dB | 118.45 dB | 96.08 dB | PASS |
| DEFAULT | 18.0209 dB | 120.90 dB | 118.45 dB | 96.08 dB | PASS |
| HIGH | 21.9780 dB | 120.90 dB | 118.45 dB | 96.08 dB | PASS |

AE-049 nominal limits are +/-0.10 dB gain error, >=70 dB CMRR 20 Hz-1 kHz and >=60 dB at 20 kHz. Tolerance/mismatch qualification remains RUN10; nominal model success does not freeze resistor grades or LT5400 value-for-money decisions.

## 4. RUN03 — all 25 SCH103 states

Disposition: **QUALIFIED_NOMINAL_ALL_25_STATES**.

All 25 intended Bass x Treble states were executed with nominal left/right instances. The worst LTspice-versus-independent analytical normalised response error is **0.001118 dB**. The worst named target error is **0.031294 dB** in `500_Hz_78__1600_Hz`. True RIAA error is **0.008280 dB**.

The largest representative SCH103 DC magnitude observed in the state matrix is **0.015884 V** in `200_Hz__FLAT`. This is a nominal sanity observation only; headroom, overload, recovery and tolerance remain later-run work.

Unnamed combinations are retained as intentional adjustment states and are judged for model correlation/L-R consistency/DC sanity rather than invented historical target accuracy.

## 5. Infrastructure debt closed

AE-066 introduces:
- reusable exact-hash external-model acquisition metadata;
- reusable model resolution, LTspice execution and scalar/polar `.meas` parsing support;
- a qualification-only parameterised SCH101/SCH103 model rather than modifying AE-065 RUN00 evidence;
- controlled RUN01/RUN02/RUN03 JSON plus CSV/Markdown summaries;
- concise `.gitignore` policy with explicit controlled-result exceptions;
- `.gitattributes` line-ending policy to reduce Windows LF/CRLF churn without mass renormalisation.

Historical AE-065 evidence and runner are not rewritten.

Execution compatibility finding: LTspice 26.0.2 on this Windows/Dropbox environment is run from a local Windows temporary directory using `-b -run`, with absolute controlled model includes and UTF-16-aware log parsing. RUN03 uses separate AC and zero-input transient decks per state because this LTspice batch version rejects multiple analyses in one deck. These are orchestration accommodations only; the electrical models and AE-049 acceptance criteria are unchanged.

## 6. RUN04-RUN06 source preparation

The controlled source-candidate file identifies:
- Murata BLM21PG600SN1D and BLM21PG221SN1D as 0805 low/high impedance brackets for frequency-dependent RUN06 ferrite modelling;
- Panasonic ECEA1VN100U as a credible 10 uF / 35 V bipolar THAT1646 sense-capacitor candidate with 5 mm diameter, 11 mm body and 2 mm pitch;
- the current generator's H5.0 capacitor footprint as a mechanical inconsistency to reconcile before PCB freeze;
- WIMA MKS 2 family candidates for the AE-052 1 uF direct block and 470 nF SCH107 timing capacitors, with hand-matching retained as a value-engineering option;
- SCH103 timing-capacitor source feasibility, including a non-authoritative 100 nF + 33 nF C0G candidate for the 1600 Hz treble state where the current 120 nF + 12 nF decomposition has a 120 nF / 50 V / 1% sourcing weakness;
- exact NKK NR01 and Samtec service-hardware candidates for later mechanical/procurement closure.

No vendor simulation/CAD payload is committed merely because a download exists; redistribution remains controlled.

## 7. Configuration and risk disposition

- DR-038 remains selected pending product implementation.
- DR-039 remains implementation/requalification open.
- R-020 remains open.
- R-021 remains bench/model-validation open.
- R-024 remains open because RUN04-RUN14 and any RUN01 Grado extended-band finding remain.
- Shellac remains +/-18 V.
- Mechanical SW905 mute and no-automatic-sequencing authority are unchanged.
- No `main` promotion is authorised.

## 8. Evidence

- `simulation/results/run01_input_loading/ae066_run01.json`
- `simulation/results/run02_gain_cmrr/ae066_run02.json`
- `simulation/results/run03_eq/ae066_run03.json`
- `simulation/results/ae066_summary.json`
- `simulation/results/ae066_summary.csv`
- `simulation/results/ae066_summary.md`
- `simulation/config/run04_run06_model_candidates.yaml`

Full structured results, rather than plot inspection, determine the dispositions above.

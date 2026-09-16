# AE-070 — RUN07 End-to-End Nominal Chain Evidence — Rev A0

**Project:** Shellac
**Status:** RUN07 NOMINAL AC QUALIFIED / BENCH CORRELATION AND LATER RUNS OPEN
**Execution baseline:** `2f1446881db130f91dbc7820f61a5887abe1ee97`

## Purpose
Execute AE-050 RUN07 as an integrated nominal-chain AC check using the previously qualified AE-066/067/068/069 block libraries. No product-generator migration is implied.

## Representative-state policy
- representative 78 state: 500 Hz / 3400 Hz, explicitly a RUN07 representative named target rather than a new global control default;
- alternate 78 state: 200 Hz / 5800 Hz using the AT-VM95SP;
- RIAA compatibility state: Grado Gold/8MZ with a 5 mV project reference level used for node-level bookkeeping, not asserted as a manufacturer output specification;
- rumble FILTER is judged by paired FILTER/BYPASS transfer so intentional LF filtering is not misclassified as replay-EQ error;
- mono uses equal in-phase channels and is compared with the matched stereo case;
- both AE-069 ferrite engineering brackets are swept; AE-070 does not select a ferrite;
- integrated vendor THAT1646 Rev02 operating-point composition is non-convergent, so RUN07 uses a qualification-only small-signal AC surrogate correlated to AE-069; this surrogate cannot support DC, CM, stability, distortion, overload, switching or fault claims;
- the surrogate output-stage phase contribution is separately correlated against the isolated vendor macro at 20 Hz, 1 kHz and 20 kHz under the RUN07 load/cable condition and both ferrite brackets; the sidecar prevents the surrogate phase from being mistaken for vendor-macro phase authority.

## Qualification boundary
Replay accuracy is evaluated from loaded cartridge terminals to balanced output. Generated cartridge EMF to output is separately recorded as the complete system transfer. Nominal node levels are recorded at 1 kHz. L/R comparison in RUN07 is nominal model symmetry only; tolerance tracking remains RUN10/RUN11 work. RUN07 does not perform clipping, overload recovery, noise, switching, rail or phantom-fault qualification.

## Headline gates
- replay and L/R nominal model symmetry: PASS; tolerance tracking remains RUN10/RUN11 work.
- integrated rumble response: PASS;
- integrated mono insertion: PASS;
- overall RUN07 nominal AC: PASS.

## Simulation infrastructure correction
AE-070 exposed a shared LTspice `ph(...)` tuple-parser defect: LTspice 26 reports phase expressions as `(magnitude dB, phase degrees)`, while the former parser returned the first tuple member. The parser is corrected and regression-tested using the exact observed LTspice format.

Blast-radius review found phase/group-delay fields in AE-066 RUN03, AE-067 RUN04 and AE-068 RUN05. Their qualification gates do not depend on those fields; the affected structured evidence is regenerated under the corrected parser without changing their historical architecture decisions or baseline metadata.

## Deferred
- RUN08 first-clipping/headroom/recovery;
- RUN09 system noise;
- RUN10 sensitivity/value engineering;
- RUN12 switching;
- RUN13 rail variation/ripple;
- RUN14 phantom fault;
- prototype bench correlation, including the still-open RUN06 load-stability and dynamic-THD gates.

## Evidence
- `simulation/results/run07_end_to_end/ae070_run07.json`
- `simulation/results/run07_end_to_end/ae070_run07.csv`
- `simulation/results/run07_end_to_end/ae070_run07.md`
- `simulation/results/run07_end_to_end/ae070_output_phase_correlation.json`

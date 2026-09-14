# AE-049 — Shellac SPICE Numerical Acceptance Criteria
**Project:** Shellac
**Status:** INTERIM / PRE-SPICE ACCEPTANCE AUTHORITY
**Date:** 2026-09-11

## Purpose
Define numerical pass/fail thresholds for the full-system SPICE qualification matrix. These limits are intended to prevent post-hoc rationalisation of simulation results.

These are engineering acceptance criteria, not manufacturing release limits until correlated with bench measurements.

---

## 1. General hierarchy
Where requirements conflict, apply in this order:
1. safety / device absolute maximum;
2. functional correctness;
3. stability;
4. headroom / overload;
5. channel symmetry / CMRR;
6. frequency-response accuracy;
7. noise;
8. switching behaviour;
9. value engineering.

No cost saving may violate a higher-level criterion.

---

## 2. RIAA replay accuracy
RIAA is the most tightly defined replay condition and shall be treated separately from historical 78 curves.

### Nominal response
Reference to 1 kHz, 20 Hz to 20 kHz:
- target: <= +/-0.10 dB
- design objective: <= +/-0.05 dB
- warning band: 0.05 to 0.10 dB
- fail: > +/-0.10 dB

### L/R tracking
RIAA channel mismatch:
- target: <= 0.10 dB, 20 Hz to 20 kHz
- design objective: <= 0.05 dB
- fail: > 0.10 dB

Existing nominal analytical errors of order 0.01 dB are therefore comfortably inside requirement and should not by themselves justify expensive component precision.

---

## 3. Historical replay EQ accuracy
Historical curves are intrinsically less exact than RIAA and records/mastering vary materially.

For named historical target curves:
- target deviation: <= +/-0.50 dB over 30 Hz to 15 kHz
- preferred design objective: <= +/-0.25 dB
- extended-band informative check: 20 Hz to 20 kHz
- fail: > +/-0.50 dB in the defined target band unless source evidence explicitly justifies otherwise.

For unnamed Bass x Treble combinations:
- no historical target-error criterion;
- must be monotonic/stable and free of unintended resonances or discontinuities;
- must remain valid operator adjustment states.

### Historical L/R tracking
- <= 0.15 dB preferred
- <= 0.25 dB maximum
- fail > 0.25 dB

This deliberately avoids buying precision beyond the uncertainty of the historical replay standards.

---

## 4. Gain accuracy
For SCH101 gain settings:
- LOW nominal 14 dB
- DEFAULT nominal 18 dB
- HIGH nominal 22 dB

Acceptance:
- absolute gain error <= +/-0.10 dB per setting
- L/R gain mismatch <= 0.05 dB preferred
- L/R mismatch <= 0.10 dB maximum

The selected fail-safe topology already analytically meets the nominal gain targets.

---

## 5. Input loading
Differential resistive load:
- nominal 47.4 kOhm
- accepted deviation: +/-2% unless cartridge-specific analysis demands tighter
- channel mismatch contribution should not create >0.05 dB response mismatch in-band.

Capacitive loading:
- BASE / +47 pF / +100 pF service states
- each state must remain stable and produce no unacceptable HF peaking with any qualified cartridge/cable combination.

Qualified cartridge response requirement:
- no > +1.0 dB unintended peaking below 20 kHz
- no > +2.0 dB peaking below 50 kHz
unless deliberately accepted for a documented cartridge/load combination.

---

## 6. CMRR
SCH101 / complete input stage:
- >= 70 dB from 20 Hz to 1 kHz
- >= 60 dB at 20 kHz
- design objective >= 75 dB mid-band.

Any tolerance relaxation that causes the complete stage to fall below these thresholds fails regardless of resistor cost saving.

---

## 7. Rumble filter
Selected response remains fourth-order Butterworth, nominal 15 Hz.

Acceptance:
- -3 dB frequency: 15 Hz +/-5%
- at 20 Hz: attenuation no worse than -0.60 dB including integrated DR-039 interaction
- at 30 Hz: attenuation no worse than -0.10 dB
- at 10 Hz: attenuation at least 13.5 dB
- at 5 Hz: attenuation at least 36 dB
- no passband peaking > +0.10 dB above 20 Hz
- L/R mismatch <= 0.10 dB, 10 Hz to 20 kHz.

The integrated DR-039 + SCH107 path, not isolated block responses, shall be judged.

---

## 8. DR-039 / LF coupling
For the final selected DC-block topology:
- additional attenuation in BYPASS at 20 Hz <= 0.10 dB preferred
- maximum acceptable at 20 Hz = 0.20 dB
- at 50 Hz <= 0.05 dB preferred
- no unintended LF resonance or interaction with SCH107.

This makes the current approximately -1.08 dB integrated 20 Hz result unacceptable and forces the interface defect to be resolved.

---

## 9. Mono matrix
Equal-input L+R:
- nominal arithmetic average
- insertion error <= 0.05 dB preferred
- <= 0.10 dB maximum.

L/R weighting mismatch in mono:
- <= 0.10% preferred
- <= 0.25% maximum.

Direct-path insertion:
- <= 0.01 dB.

Outside mono:
- no intentional resistive L-R path;
- electrical crosstalk criterion applies.

---

## 10. Crosstalk
Stereo mode, 20 Hz to 20 kHz:
- >= 80 dB separation at 1 kHz preferred
- >= 70 dB minimum at 1 kHz
- >= 60 dB minimum at 20 kHz.

DUAL L / DUAL R deliberate duplication is excluded from crosstalk criteria.

Switch parasitics shall be included in the high-frequency case.

---

## 11. Noise
Absolute noise criteria should be referred to both input and balanced output.

Provisional full-system acceptance:
- A-weighted output noise in DEFAULT/RIAA should remain comfortably below -90 dBu if the model supports the calculation;
- otherwise use comparative criterion: no proposed value-engineering change may degrade integrated 20 Hz-20 kHz output-noise RMS by >1.0 dB without explicit benefit.

For individual optimisation:
- <=0.25 dB system-noise increase: generally acceptable if cost/size benefit is meaningful;
- 0.25-0.75 dB: trade study required;
- >0.75 dB: reject unless compelling system benefit.

SCH107 impedance scaling shall be judged on system noise, not its isolated noise increase.

---

## 12. Headroom / overload
Normal qualified operating state:
- >= 6 dB margin to first clipping for nominal cartridge output preferred;
- >= 3 dB minimum.

Hot-record / high-velocity test:
- no earlier-stage clipping before the defined overload threshold.

Overload qualification:
- determine cartridge input RMS at first material clipping for every gain setting and representative EQ state;
- document HIGH gain as restricted operating envelope if required.

Recovery:
- after a 10x nominal transient burst, output must return to within 1% of steady-state amplitude within 100 ms unless an LF coupling network physically requires longer;
- any longer recovery must be explicitly explained and judged audibly benign.

No device absolute maximum may be exceeded during overload testing.

---

## 13. DC offsets
Normal RUN state:
- XLR differential DC <= 10 mV preferred
- <= 25 mV maximum.

XLR common-mode DC:
- <= 100 mV preferred
- <= 250 mV maximum consistent with THAT1646 expectations.

Internal DC may be higher where intentionally blocked, but no switch state may drive a downstream stage into saturation.

---

## 14. Switching transients
Measured at differential XLR output with realistic load.

With MUTE asserted:
- no transient exceeding 100 mV peak preferred
- 250 mV peak maximum.

Live switching stress case:
- no device saturation or instability;
- transient <= 1 V peak preferred;
- >1 V requires review even though live switching is not normal operation.

Settling:
- return to within 1% of steady state within 100 ms for matrix/mute switching unless DR-039 topology imposes a documented slower LF charge transient.

The operating rule remains MUTE -> change selector -> RUN unless bench evidence justifies relaxing it.

---

## 15. Output loading
For 100 kOhm, 20 kOhm and 10 kOhm balanced loads:
- differential gain variation <= 0.10 dB
- no oscillation
- no >0.1 dB passband peaking 20 Hz-20 kHz.

600 Ohm is a stress case:
- must remain stable;
- gain droop and distortion shall be recorded;
- it need not meet normal-load performance if 600 Ohm is outside the product requirement.

---

## 16. Rail variation
Normal rail sweep:
- +/-17.5 V to +/-18.5 V as primary tolerance band unless PSU evidence establishes a different range.

Acceptance:
- gain change <= 0.05 dB
- RIAA response change <= 0.02 dB
- no stability change
- no material DC-offset increase.

Rail asymmetry:
- test at least +/-0.5 V mismatch.
- output common-mode and distortion must remain acceptable.

---

## 17. Supply ripple
Inject representative 100 Hz ripple on rails.

Target:
- output-referred 100 Hz artefact at least 80 dB below a 1 kHz nominal reference signal where the model supports direct comparison.

At minimum:
- no visible gain modulation;
- no rectification-induced DC shift;
- no instability.

---

## 18. Phantom-power fault
This is a survival criterion, not an audio-performance criterion.

Mandatory:
- no THAT1646 pin exceeds datasheet absolute maximum;
- no rail exceeds any powered IC absolute supply maximum;
- clamp diodes remain within pulse-current and energy capability;
- regulator reverse-current/reverse-voltage remains within allowed behaviour;
- no electrolytic capacitor sees reverse polarity or overvoltage;
- no component exceeds safe dissipation transiently.

Preferred additional margin:
- rail peak <= 19.0 V where practical on nominal +18 V rail;
- any excursion >19 V requires explicit device-margin review;
- >=20 V rail excursion is presumptive FAIL until proven safe by all connected device limits.

Powered and unpowered cases both mandatory.

---

## 19. Stability
All op-amps and THAT1646:
- no sustained oscillation;
- phase/gain margin where obtainable should be >=45 degrees / >=6 dB;
- transient ringing should decay monotonically or be demonstrably benign.

Where macro-models do not permit robust loop-margin extraction, use load/capacitance transient sweeps plus bench verification.

---

## 20. Component-tolerance decision rules
After sensitivity analysis:

### Category A — absolute value matters
Specify the loosest absolute tolerance that preserves all relevant criteria with margin.

### Category B — matching matters
Prefer economical low-TCR components plus hand matching for the one-off build where measurement repeatability is adequate.

### Category C — low sensitivity
Use normal commercial tolerance; no premium grade.

A component upgrade must produce measurable requirement margin, not merely aesthetic precision.

---

## 21. Monte Carlo acceptance
For selected high-leverage cases:
- >= 1000 runs preferred where simulator speed permits;
- zero Cat-A safety/function failures;
- >= 99% of runs should meet performance criteria;
- any tail failures must be understood and converted into tighter component constraints or assembly selection rules.

Do not Monte Carlo every switch state indiscriminately.

---

## 22. Bench-correlation reserve
SPICE pass does not equal baseline.

Bench measurements shall confirm at minimum:
- gain;
- RIAA;
- representative historical EQ;
- noise;
- rumble response;
- mono balance;
- crosstalk;
- mute/matrix transient;
- output DC;
- load stability.

Final production limits may be tightened after correlation.

---

## Gate status
These criteria are suitable as PRE-SPICE acceptance authority.
They remain open to refinement only where component/device datasheets or simulation evidence demonstrate that a threshold is physically inappropriate.

## Confidence
- RIAA +/-0.10 dB acceptance: 98%
- historical +/-0.50 dB acceptance: 96%
- CMRR 70 dB LF/mid, 60 dB at 20 kHz: 97%
- rumble criteria aligned with established intent: 99%
- DR-039 <=0.20 dB at 20 Hz maximum: 98%
- switching thresholds are sensible provisional engineering limits: 92%
- noise change bands are suitable value-engineering criteria: 94%
- phantom fault absolute-maximum criterion: 100%

# G3-026 — Optional-RIAA Circuit Realisation and Manufacturing-Control Geometry

**Revision:** A0  
**Status:** candidate  
**Base:** G3-025 / `89dfc9f8493ba6327d5ce175ccaaa75bb410dda4`

## 1. Primary objective

Convert the G3-025 transfer-function contract for the optional 3180 us term into
a practical, polarity-preserving stereo circuit; select the internal switch; close
the nominal upper-cover stack where evidence permits; and add automated regression
testing so future pushed branches can be inspected without manual console relay.

## 2. Topology trade

Three implementation classes were considered.

### A. Passive RC plus buffer — rejected

A simple 3180 us passive low-pass gives approximately 26 dB insertion loss at
1 kHz. Recovering that loss elsewhere couples the optional section into the gain
architecture and makes BYPASS level discontinuous.

### B. Inverting active low-pass — rejected

An inverting first-order active filter can use lower impedances and has attractive
noise/headroom characteristics, but ON would invert polarity while straight-through
BYPASS would not. Restoring common polarity requires another inversion path and
roughly doubles active circuitry.

### C. RC before non-inverting gain — selected

Each channel uses:
- 31.5 kΩ, 0.1% series timing resistor;
- 68 nF + 33 nF in parallel, both 1%, 50 V, C0G/NP0;
- one OPA1656 non-inverting stage;
- gain resistors 267 Ω / 5.08 kΩ, 0.1%.

Nominal timing is 3181.5 us (50.025 Hz). Nominal 1 kHz magnitude is +0.0049 dB.
Worst-corner 1 kHz level error from the stated R/C/gain tolerances is about
-0.11 to +0.12 dB.

The RC precedes the gain stage so out-of-band high-frequency energy is attenuated
before the approximately 20x amplifier. This improves internal overload behaviour
relative to placing the gain before the pole.

OPA1656 is already a controlled Shellac device in SCH101, so its reuse improves BOM,
qualification and stocking commonality. Its FET input is also well suited to the
31.5 kΩ timing source impedance.

## 3. Internal switch

Selected: **Nidec Components ASE2D-2M-10-Z**.

Required characteristics are satisfied:
- DPDT ON-ON;
- through-hole PC pins;
- gold contact finish;
- non-shorting / BBM timing;
- low-level 50 mA / 60 V class;
- compact internal/service configuration control.

The switch is placed at the section output. Each common feeds the downstream left or
right signal. One throw receives the straight-through `RIAA_CORE_OUT`; the other
receives the corresponding filtered/amplified `RIAA_3180_OUT`.

The optional filter remains driven in BYPASS, but disconnected from the downstream
signal. This keeps both switch throws low impedance and makes BYPASS genuinely
straight-through. Change this internal configuration with the unit muted or powered
down.

## 4. Timing capacitors

The frozen replay timing-capacitor rule is retained. G3-026 therefore does not use a
cheap X7R 100 nF part.

Selected parallel pair per channel:
- KEMET `C1206C683F5GECAUTO7210`, 68 nF, 1%, 50 V, C0G/NP0;
- KEMET `C1206C333F5GEC7210`, 33 nF, 1%, 50 V, C0G/NP0.

Total nominal capacitance is 101 nF. The small offset is compensated by selecting
31.5 kΩ, yielding 3181.5 us.

## 5. Headroom and noise

The realisation model retains the existing conservative 10 V RMS design-output
limit. The optional section permits more than 0.53 V RMS input at 20 Hz before
that limit.

For context, a 30 mV cartridge test input at the 22 dB SCH101 setting gives a
modelled optional-section output of roughly 7.0 V RMS at 20 Hz when combined with
the invariant 318/75 core, leaving useful margin to the 10 V RMS design limit.

The model also records a first-order 1 kHz white-noise proxy below 110 nV/√Hz.
This is a design-comparison metric, not a claim for final integrated system SNR;
SPICE/bench verification remains part of electrical release.

## 6. Upper-cover stack

The M5502119 manufacturer drawing marks 2.00 mm as a typical sheet dimension in the
cover/base detail. G3-026 accepts **2.0 mm nominal** for stack analysis but does not
invent a missing sheet-thickness tolerance.

Against that nominal:
- Grayhill bushing length 7.92 mm leaves 5.92 mm above the cover;
- C&K 7201SYCBE bushing length 8.89 mm leaves 6.89 mm above the cover.

This clears the basic “can the bushing reach through the cover?” concern. It does
**not** release drilling: final nut/washer/anti-rotation/knob stack, footprint Z,
manufacturer tolerance and PCB datum still require verification.

## 7. CI risk reduction

G3-026 adds a GitHub Actions workflow which:
- installs the repository requirements;
- compiles generator/tests;
- runs the complete pytest suite on `main`, `feature/**` pushes and pull requests.

Once merged, pushed work can be inspected via GitHub CI instead of relying solely
on manually relayed local pytest output.

## 8. Not released

G3-026 does not release:
- final SCH103 KiCad conversion of the optional section;
- external-control custom footprints;
- final PCB placement coordinates;
- top-cover drilling coordinates;
- enclosure machining;
- PCB fabrication.

## 9. Acceptance

- selected optional section is polarity-preserving and factor-consistent;
- nominal pole is within 0.1 Hz of 50 Hz;
- 1 kHz nominal level mismatch is under 0.01 dB;
- worst stated tolerance corner remains inside ±0.13 dB at 1 kHz;
- internal switch is exact-MPN, DPDT, gold, BBM and through-hole;
- nominal top-cover bushing penetration is modelled without inventing tolerance;
- CI workflow is present;
- focused and full regression suites pass.

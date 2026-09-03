# AE-029 — Production Commissioning and Acceptance Closure

**Revision:** A0  
**Status:** MAJOR ELECTRICAL CLOSURE / PROTOTYPE ACCEPTANCE DEFINITION

## Executive finding

The Shellac electrical design is substantially more mature than the number of
open historical records suggests.

Most core architecture questions are already closed analytically or by generator
regression. The remaining production-release work is dominated by **physical
verification**, not unresolved circuit synthesis.

### Already analytically closed

- SCH101 14 / 18 / 22 dB gain architecture;
- complete-RIAA architecture;
- wanted-band headroom;
- nominal 1 kHz end-to-end output level;
- deterministic SCH101 tolerance CMRR model;
- DR-039 DC-isolation topology;
- complete-chain first-order noise model;
- SCH107 fourth-order 15 Hz rumble-filter transfer function;
- SCH105 Stereo / Dual-L / Dual-R / (L+R)/2 electrical truth table;
- mono-average gain error;
- low-frequency DC-block attenuation in the wanted band.

### Still requiring prototype evidence

- measured CMRR;
- measured electronics noise;
- measured output DC;
- measured L/R gain matching;
- measured True-RIAA and historical EQ curves;
- actual overload/clipping onset;
- balanced-output symmetry;
- channel-mode functional verification;
- switch transients;
- power-up and power-down transients.

### Genuine open design item

The principal remaining signal-path-adjacent design item is the rotary-switch
production hardware:

- exact Lorlin PT gold-contact MPNs;
- AE-028 mechanical sample validation;
- subsequent BOM/PCB/panel ECO.

That is a mechanical/procurement closure issue rather than an unresolved
equalisation/signal-chain topology issue.

## Production acceptance philosophy

AE-029 deliberately separates three evidence classes:

**ANALYTICALLY_CLOSED**  
The requirement is demonstrated by the controlled design model and regressions.
Prototype measurement confirms build quality but does not reopen the architecture
unless measurement disagrees materially.

**VERIFY_ON_PROTOTYPE**  
The model establishes a design expectation or provisional production limit, but
physical parasitics, component distribution or transient behaviour make hardware
measurement mandatory.

**OPEN_DESIGN**  
Information is still missing and production release is blocked.

## Provisional production limits

The following should be treated as commissioning limits for the first prototype,
then tightened or relaxed only from measured evidence.

| Parameter | Initial acceptance |
|---|---|
| SCH101 LOW gain | 14 dB nominal, model error <=0.10 dB |
| SCH101 DEFAULT gain | 18 dB nominal, model error <=0.10 dB |
| SCH101 HIGH gain | 22 dB nominal, model error <=0.10 dB |
| RIAA 1 kHz output, DEFAULT, 5 mV RMS | 0.62–0.67 V RMS differential |
| L/R gain matching at 1 kHz | <=0.10 dB provisional |
| True-RIAA shape | <=±0.20 dB, 20 Hz–20 kHz provisional |
| Historical EQ shape | <=±0.50 dB vs implemented nominal target provisional |
| CMRR 20 Hz–1 kHz | >=70 dB |
| CMRR 20 kHz | >=60 dB |
| Output electronics noise | <=150 µV RMS differential, 20 Hz–20 kHz provisional |
| Output DC after settling | <=25 mV differential provisional |
| Rumble FILTER loss at 20 Hz | >-0.50 dB |
| Rumble attenuation at 10 Hz | <-14 dB |
| Rumble attenuation at 5 Hz | <-38 dB |
| Mono equal-input error | <0.03 dB |
| Output leg amplitude mismatch | <=0.10 dB provisional |
| Power-up mute interval | >=2 s before MUTE release |

## Important interpretation of EQ limits

The True-RIAA position represents a formal standard and therefore receives the
tighter provisional ±0.20 dB production target.

The historical 78 positions approximate families of historical curves. Their
source standards and mastering practice are inconsistent, so ±0.50 dB against
the implemented nominal target is a build-verification tolerance, not a claim
that every historical record was mastered to that accuracy.

## Overload test plan

The prototype overload test should not be reduced to a 1 kHz clipping check.

Test each gain setting at minimum:

- 20 Hz;
- 50 Hz;
- 100 Hz;
- 1 kHz;
- 10 kHz;
- 20 kHz.

Include True RIAA and the highest-gain historical bass/treble combinations.

Record:
- input RMS at first visible waveform compression;
- SCH103 internal waveform where accessible;
- balanced XLR differential RMS;
- which stage limits first;
- recovery after overload.

This will convert the analytical 10 V RMS design ceiling into measured
production evidence.

## CMRR test plan

Use a genuinely symmetrical low-impedance common-mode source and verify all
three SCH101 gain settings.

Minimum points:
- 20 Hz;
- 100 Hz;
- 1 kHz;
- 10 kHz;
- 20 kHz.

The source and measurement fixture must provide substantially better intrinsic
balance than the acceptance threshold, otherwise fixture error will dominate.

## Noise test plan

Measure with both inputs terminated in the production source impedance condition.

Record:
- A-weighted only as supplementary information;
- primary result unweighted 20 Hz–20 kHz differential RMS;
- DEFAULT gain / True RIAA;
- rumble FILTER and BYPASS;
- output spectrum so hum components can be separated from broadband noise.

The current <=150 µV RMS criterion is deliberately looser than the ~0.1 mV
first-order prediction to avoid false precision before PCB/hardware evidence.

## Switching/transient plan

Scope differential XLR output for:
- MUTE engage/release;
- Rumble FILTER/BYPASS;
- all four channel-mode transitions;
- Bass selector changes;
- Treble selector changes;
- cold power-up;
- warm power-up;
- power-down.

Test with zero input and representative programme-equivalent sinusoidal input.

The first prototype should record transient peaks rather than impose an
arbitrary click/pop voltage limit. A production limit can then be frozen from
measured behaviour and audibility/service requirements.

## What this clears

AE-029 removes the need for further speculative redesign of:
- input gain partition;
- RIAA topology;
- rumble-filter order/corner;
- channel-mode matrix;
- post-EQ DC block;
- nominal noise architecture;
- basic headroom allocation.

Those areas should only be reopened if prototype evidence contradicts the
controlled model.

## Remaining electrical release blockers

After AE-029, the remaining blockers are predominantly:
1. physical rotary-switch closure;
2. first representative hardware;
3. measured commissioning evidence;
4. any corrective ECO arising from measurement.

The next useful design activity can therefore shift toward production PCB /
mechanical readiness and the commissioning fixture/procedure rather than more
signal-chain synthesis.

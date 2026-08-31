# AE-023 — Production Signal-Chain Assurance Closure

**Revision:** A0  
**Status:** ANALYTICAL CLOSURE — prototype measurements still required  
**Base commit:** `dce5c0ec36e12f979338d8c46106c44a79c7a023`

## Purpose

AE-023 reconciles the end-to-end analyses against the actually implemented
DR-038 and DR-039 circuit, rather than the earlier candidate/staging models.

## Implemented baseline verified

SCH101 now uses:

- 4.000x precision differential conversion;
- LT5400-7 1.25 kΩ / 5 kΩ network;
- 1 kΩ-scale gain ladder;
- hard service-link gain configuration;
- 100 Ω 0.1% RF series pair;
- 1 nF 0.5% matched common-mode C0G pair.

SCH103 now includes the DR-039 1 µF film / 330 kΩ DC block before the SCH107
FILTER/BYPASS split.

## CMRR closure

A 4096-corner frequency-dependent model was run for each gain setting at
20 Hz, 1 kHz and 20 kHz. It includes independent worst-case RF resistor,
common-mode capacitor, gain-ratio and LT5400 ratio errors.

Representative deterministic minima are approximately:

| Gain | 20 Hz | 1 kHz | 20 kHz |
|---|---:|---:|---:|
| LOW | 78.4 dB | 78.4 dB | 72.2 dB |
| DEFAULT | 72.4 dB | 72.4 dB | 69.8 dB |
| HIGH | 70.1 dB | 70.1 dB | 68.3 dB |

Therefore the proposed production requirements are met analytically:

- >=70 dB from 20 Hz through 1 kHz;
- >=60 dB at 20 kHz.

These values are resistor/RF-tolerance predictions, not a substitute for
prototype common-mode injection measurements.

## Gain/headroom

The implemented DR-038 values remain within the established 14/18/22 dB gain
architecture. DR-039 adds less than 0.01 dB attenuation at 20 Hz and negligible
loss in the normal replay band.

The AE-012 conclusion remains: DEFAULT is the normal 5 mV setting; HIGH is a
lower-output-cartridge setting with deliberately reduced low-frequency margin.

## Noise

The production closure uses DR-039 in the noise path unconditionally. The
first-order complete-RIAA result remains of order 0.1 mV RMS balanced output,
with electronics SNR in the mid-70 dB range at the nominal output.

No further circuit noise optimisation is justified before prototype
measurement; record/surface noise will generally dominate 78-rpm use.

## DC and transient behaviour

DR-039 removes the state-dependent DC weakness identified by AE-015.

Its time constant is:

`330 kΩ x 1 µF = 0.33 s`

A 2 s muted settling interval is more than six time constants, leaving less
than 0.3% of an initial capacitor-charging transient.

The mechanical mute philosophy is retained. Commissioning/maintenance guidance
therefore specifies MUTE during power-up/power-down and a >=2 s settling delay.

This is not yet a measured switching-transient closure. Prototype tests remain
required for:

- power-on;
- power-off;
- MUTE release/engage;
- rumble FILTER/BYPASS switching;
- channel-mode switching.

## Documentation-control finding

The authoritative decision index contained one stale contradiction: DR-038 was
marked CURRENT_IMPLEMENTED while retaining text that said active SCH101 was
still pre-DR038 pending migration.

AE-023 removes that stale staging language and adds an automated status/prose
consistency guard.

## Closure disposition

### Analytically closed

- complete RIAA architecture;
- gain partition;
- wanted-band headroom;
- SCH101 deterministic CMRR tolerance model;
- DR-039 DC isolation architecture;
- first-order electronics-noise budget.

### Prototype evidence still required

- measured CMRR;
- measured noise;
- measured output DC;
- actual clipping/overload onset;
- switching transients;
- power-up/power-down behaviour.

These should become production acceptance values after the first representative
hardware is commissioned.

## Next phase

The signal-chain design is now sufficiently mature to shift effort toward:

1. prototype/production commissioning test definition;
2. decision/document reconciliation across the complete project;
3. mechanical/PCB production-baseline closure;
4. release-pack and repository reproducibility work.

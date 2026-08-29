# Project Shellac — AE-011 End-to-End Signal-Chain Analysis and Closure

**Revision:** A0  
**Status:** formal review in progress; one RIAA integration blocker identified  
**Baseline:** GitHub `main` at commit `4581c49`  
**Date:** 28 August 2026

## 1. Purpose

This analysis reconstructs the complete Project Shellac analogue signal-chain assurance that predates the GitHub-controlled baseline. It deliberately does not assume that individually closed circuit blocks imply a closed complete system.

The authoritative review path is:

`cartridge -> SCH101 -> SCH103 -> SCH107 -> SCH104 -> SCH105 -> SCH108 -> XLR`

with the independent optional 3180 us RIAA function included where applicable.

The review covers:

- absolute gain and level at each principal node;
- frequency-dependent replay equalisation;
- SCH101 low/default/high gain settings;
- rumble-filter bypass and inserted states;
- mode-matrix level behaviour;
- final THAT1646 differential gain;
- overload margin against the 10 V RMS conservative internal design ceiling;
- compatibility of the legacy TRUE-RIAA branch with the independent optional 3180 us pole;
- residual verification needed for noise, CMRR, DC offset, switching and external loading.

## 2. Controlled signal-chain architecture

### SCH101 — balanced cartridge input

The current model implements:

- matched OPA1656 non-inverting gain on each floating cartridge leg;
- fixed 3.48x differential conversion;
- three allowed complete gains:

| Setting | Total gain | Realised |
|---|---:|---:|
| Low | 5.018x | 14.01 dB |
| Default | 7.900x | 17.95 dB |
| High | 12.563x | 21.98 dB |

The default is the reference setting for the historical downstream calculations.

### SCH103 — replay equalisation

The controlled values are:

- active LF P06/P91-derived stage;
- 100 kΩ principal feedback resistance;
- selectable complete historical bass branches;
- passive 750 Ω treble network;
- fixed OPA1612 recovery gain 2.100x (+6.444 dB).

Historical bass selections are FLAT, 200 Hz, 400 Hz and 500 Hz 78. The legacy TRUE-RIAA branch is separate and currently implements approximately the 3180 us pole and 318 us zero.

### SCH107 — rumble filter

Fourth-order Butterworth high-pass, nominal 15 Hz, unity pass-band gain, switchable by a linked stereo break-before-make bypass.

Representative realised attenuation:

| Frequency | Approximate response |
|---:|---:|
| 5 Hz | -38 dB |
| 10 Hz | -14 dB |
| 15 Hz | -3 dB |
| 20 Hz | -0.46 dB |
| 30 Hz | -0.04 dB |

### SCH104 — final isolation buffer

The current generator correctly implements **unity gain**.

This is important: the older 2x SCH104 proposal is superseded. The final +6.021 dB system gain is supplied by SCH108/THAT1646.

### SCH105 — mode matrix

Modes:

- Stereo: L, R
- Dual Left: L, L
- Dual Right: R, R
- Mono: (L+R)/2, (L+R)/2

The mono function averages rather than summing at unity, so equal correlated L/R signals do not acquire a 6 dB level increase. Post-switch OPA1656 buffers operate at unity.

### SCH108 — balanced output

THAT1646 differential line driver:

- 2.000x differential voltage gain (+6.021 dB);
- approximately 50 Ω output impedance per leg;
- conservative differential design ceiling: 10 V RMS;
- nominal historical calculation: 0.321 V RMS input -> 0.642 V RMS differential output;
- severe historical calculation: 3.21 V RMS input -> 6.42 V RMS differential output.

## 3. Reconstructed absolute gain model

For rumble bypass, Stereo mode and mute released:

`G_XLR(f) = G_SCH101 x |H_LF(f)| x |H_HF(f)| x 2.1 x 1 x 1 x 2`

where:

- `G_SCH101` is 5.018, 7.900 or 12.563;
- `H_LF` is the selected SCH103 active LF transfer;
- `H_HF` is the selected passive treble transfer;
- 2.1 is SCH103 recovery;
- SCH104 is unity;
- SCH105 is unity for a single-channel signal;
- 2 is THAT1646 differential gain.

When SCH107 is inserted, multiply by its fourth-order high-pass transfer.

### 3.1 Flat replay reference

With both EQ selectors FLAT, SCH103 contributes only its 2.1x recovery gain.

Therefore the approximate cartridge-to-XLR gains are:

| SCH101 setting | Complete flat gain | Gain |
|---|---:|---:|
| Low | 21.08x | 26.48 dB |
| Default | 33.18x | 30.42 dB |
| High | 52.76x | 34.45 dB |

For a 5 mV RMS cartridge signal this corresponds approximately to:

| SCH101 setting | XLR differential output |
|---|---:|
| Low | 105 mV RMS |
| Default | 166 mV RMS |
| High | 264 mV RMS |

These are flat-replay figures, not the maximum levels produced by historical or RIAA equalisation.

### 3.2 Historical 1 kHz level

The 200 Hz bass branch still has appreciable absolute gain at 1 kHz. With flat treble and default SCH101 gain, the reconstructed complete cartridge-to-XLR gain is approximately 128.8x (42.20 dB), producing approximately **0.644 V RMS differential** from 5 mV RMS cartridge input.

This independently reproduces the historical nominal ~0.642 V RMS output figure to within normal component/value rounding.

This is an important closure result: the long-standing 0.321 V / 0.642 V nominal budget is consistent with the actual current SCH101 + SCH103 + THAT1646 architecture rather than being an orphaned number from the superseded SCH104 design.

The current TRUE-RIAA combination gives a very similar 1 kHz result, approximately 0.638 V RMS differential from 5 mV RMS at the default input gain.

## 4. Headroom

The SCH103 first active LF stage remains the principal frequency-dependent overload constraint.

The controlled SCH103 electrical model computes cartridge overload from:

`10 V RMS / (SCH101 gain x active-LF gain)`

and asserts a worst-case input capability greater than 30 mV RMS at the default SCH101 setting.

Against the 5 mV nominal reference this is greater than 6x voltage margin (>15.6 dB).

Downstream:

- SCH104 is unity;
- SCH105 is unity;
- THAT1646 applies the final 2x differential gain;
- the established severe 3.21 V RMS THAT1646 input becomes 6.42 V RMS differential;
- margin to the conservative 10 V RMS differential ceiling is >3.8 dB.

### 4.1 Gain-selector implication

The existing >30 mV cartridge overload statement is explicitly a **default SCH101 gain** result.

The high SCH101 setting is 12.563 / 7.900 = 1.590x above default, so a first-order scaling of the same LF-stage overload envelope reduces the allowable cartridge input by the same ratio.

Accordingly, a 30 mV default-gain boundary would become approximately 18.9 mV on High gain.

This remains comfortably above the nominal 5 mV reference, but the formal closure model shall calculate the actual worst frequency/curve rather than rely on this scaled estimate.

## 5. Rumble-filter system effect

SCH107 is correctly located before the final routing/output stages.

At 20 Hz it costs only about 0.46 dB, while at 10 Hz it reduces downstream infrasonic level by about 14 dB and at 5 Hz by about 38 dB.

This materially improves practical headroom against warp, bearing and structural energy without changing the principal wanted-band gain budget.

**Review disposition: retain architecture.**

## 6. Mode-matrix system effect

Stereo, Dual Left and Dual Right do not increase the selected source-channel amplitude.

The mono function is `(L+R)/2`.

For equal correlated channels:

`(V + V)/2 = V`

so no +6 dB summing penalty occurs.

For equal anti-phase channels:

`(V + -V)/2 = 0`

which provides the expected mono cancellation test.

**Review disposition: no headroom penalty introduced by the approved mode matrix.**

## 7. Critical RIAA integration finding — BLOCKER

The repository presently contains two representations of the 3180 us / ~50 Hz RIAA term:

1. the legacy TRUE-RIAA SCH103 bass branch, which implements approximately:
   - 3180 us pole (~50 Hz);
   - 318 us zero (~500 Hz);

2. the newer independent operator-controlled 3180 us stage.

If the independent stage is enabled while the legacy TRUE-RIAA bass branch is selected, the 3180 us pole is applied twice.

This is not a documentation-only inconsistency. It changes the actual transfer function and therefore prevents complete end-to-end RIAA closure.

### Required correction

Resynthesise the TRUE-RIAA contribution such that:

- the 318 us zero remains in the RIAA core;
- the 75 us treble pole remains in the RIAA core/treble implementation;
- the 3180 us pole exists **only** in the independent optional stage when that stage is enabled;
- optional 3180 us BYPASS produces the defined core response without the low-frequency pole;
- optional 3180 us ON produces canonical three-time-constant RIAA when combined with the RIAA core.

The operator-controlled 3180 us function remains independent; no Bass/Treble interlock is required.

**Disposition: RED / release blocker until resynthesis and verification are complete.**

## 8. Current formal-review disposition

| Area | Disposition | Comment |
|---|---|---|
| SCH101 gain architecture | GREEN | Current generator matches AE-010 |
| SCH103 historical EQ topology | GREEN | Existing electrical/curve models retained |
| SCH103 absolute level budget | GREEN/VERIFY | Reconstructed nominal output is consistent |
| SCH107 rumble filter | GREEN | Correct order and unity pass-band architecture |
| SCH104 | GREEN | Generator confirms unity, superseded 2x design not present |
| SCH105 mode matrix | GREEN | No correlated-signal gain penalty |
| SCH108 output | GREEN | +6.021 dB correctly occurs here |
| Overall default gain budget | GREEN | ~0.64 V nominal figure independently recovered |
| High-gain overload envelope | AMBER | Needs explicit full frequency/curve sweep |
| End-to-end noise | AMBER | Needs one integrated input-referred/output-referred model |
| End-to-end DC offset | AMBER | Needs worst-case tolerance/bias analysis and bench acceptance |
| CMRR | AMBER | Needs tolerance-based SCH101 calculation and test target |
| Switching transients | AMBER | Needs integrated state-transition acceptance tests |
| Optional 3180 us RIAA integration | RED | Legacy 3180 us term is duplicated |

## 9. Closure work required

Before PCB release, complete these controlled actions:

1. add a machine-executable complete signal-chain model driven from existing controlled component constants;
2. sweep all allowed SCH101 gains;
3. sweep all historical bass/treble combinations over at least 5 Hz–20 kHz;
4. sweep rumble bypass/inserted;
5. include Stereo/Dual-L/Dual-R/Mono amplitude cases;
6. calculate node-by-node maximum RMS/peak levels and identify the limiting node;
7. resynthesise and verify the RIAA core so the independent 3180 us stage cannot duplicate the low-frequency pole;
8. produce integrated noise, CMRR and DC-offset budgets;
9. convert the resulting numerical limits into commissioning tests.

## 10. Review conclusion at Rev A0

The reconstruction has not exposed a general gain-chain design failure.

On the contrary, it confirms that the important historical correction — unity SCH104 followed by +6 dB differential gain in SCH108 — is present in the current generator, and it independently recovers the established ~0.64 V RMS nominal balanced output for representative historical/RIAA replay at the default input gain.

The formal review has, however, confirmed one substantive open architecture issue: the optional independent 3180 us RIAA stage is incompatible with the unmodified legacy TRUE-RIAA bass branch because the 3180 us term would be duplicated.

The project should therefore retain the present analogue architecture, close the RIAA-core resynthesis, and then complete the quantitative all-state sweep before declaring the end-to-end signal chain formally closed.

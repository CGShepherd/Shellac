# Project Shellac — AE-011 End-to-End Signal-Chain Analysis and Closure

**Revision:** A1  
**Status:** formal review in progress; architecture coherent  
**Date:** 28 August 2026  
**Baseline reviewed:** GitHub `main` at `4581c49`  
**Superseding decision:** DR-037 Restore Legacy Complete-RIAA Architecture

## 1. Purpose

Reconstruct and formally control the complete Project Shellac signal-chain assurance from cartridge input to balanced XLR output.

Authoritative active path:

`Cartridge -> SCH101 -> SCH103 -> SCH107 -> SCH104 -> SCH105 -> SCH108 -> XLR`

The independent optional 3180 us RIAA stage introduced during G3-025/G3-026 is removed from the active architecture by DR-037.

## 2. RIAA architecture

Complete RIAA is provided entirely by SCH103:

- TRUE-RIAA bass branch: approximately 3180 us pole and 318 us zero;
- 2121 Hz RIAA treble branch: approximately 75 us pole.

Together these realise the complete three-time-constant RIAA replay response.

No additional 3180 us stage or switch is required.

## 3. Absolute gain chain

For Stereo mode, rumble bypass and mute released:

`G_XLR(f) = G_SCH101 × |H_LF(f)| × |H_HF(f)| × 2.1 × 1 × 1 × 2`

where:

- SCH101 = 5.018x / 7.900x / 12.563x;
- SCH103 recovery = 2.100x;
- SCH107 pass-band gain ≈ 1;
- SCH104 = unity;
- SCH105 = unity;
- SCH108 THAT1646 = 2.000x differential gain.

## 4. Key reconstructed result

At default SCH101 gain, with the 200 Hz bass branch and flat treble at 1 kHz, a 5 mV RMS cartridge input produces approximately 0.64 V RMS differential at the XLR.

The restored TRUE-RIAA + 2121 Hz RIAA combination produces a closely similar nominal 1 kHz output.

This independently confirms that the long-standing ~0.642 V RMS nominal output budget is consistent with the current corrected architecture and is not an artefact of the superseded 2x SCH104 design.

## 5. Headroom

The first active SCH103 LF stage remains the principal frequency-dependent overload constraint.

At default SCH101 gain the existing controlled model demonstrates worst-case cartridge-input overload capability above 30 mV RMS against a 5 mV nominal reference.

SCH104 and SCH105 are unity.

THAT1646 provides the final 2x differential gain. The established severe case of 3.21 V RMS input gives 6.42 V RMS differential, leaving more than 3.8 dB to the conservative 10 V RMS differential design ceiling.

## 6. Rumble filter

SCH107 remains correctly located before later routing and output conversion.

Its fourth-order 15 Hz Butterworth response materially suppresses infrasonic energy while preserving the wanted band:

- ~-38 dB at 5 Hz;
- ~-14 dB at 10 Hz;
- ~-0.46 dB at 20 Hz;
- ~-0.04 dB at 30 Hz.

No architecture change required.

## 7. Mode matrix

Stereo, Dual Left and Dual Right do not increase selected-channel level.

Mono is `(L+R)/2`, so equal correlated channels retain their original amplitude rather than acquiring a +6 dB summing penalty.

No headroom penalty is introduced by the selected mode architecture.

## 8. Formal review disposition

| Area | Disposition | Comment |
|---|---|---|
| SCH101 gain architecture | GREEN | Current generator matches selected 14/18/22 dB architecture |
| SCH103 historical EQ | GREEN | Existing controlled model retained |
| Complete RIAA | GREEN | Legacy TRUE-RIAA + 2121 Hz treble restored as authority |
| SCH107 rumble filter | GREEN | Architecture retained |
| SCH104 | GREEN | Current generator correctly implements unity |
| SCH105 mode matrix | GREEN | No correlated-signal gain penalty |
| SCH108 | GREEN | Final +6.021 dB occurs only here |
| Nominal end-to-end gain | GREEN | ~0.64 V RMS result reconstructed independently |
| Optional 3180 stage | REMOVE | Superseded by DR-037 |
| Full high-gain overload sweep | AMBER | Explicit all-state sweep still required |
| Integrated noise budget | AMBER | To be consolidated |
| CMRR budget | AMBER | Tolerance-based calculation required |
| DC-offset budget | AMBER | Integrated calculation + bench limits required |
| Switching transient acceptance | AMBER | Integrated test required |

## 9. Remaining closure tasks

1. implement DR-037 in generator/BOM/layout;
2. run an all-state gain/headroom sweep over SCH101 gain, historical EQ, RIAA, rumble state and frequency;
3. consolidate end-to-end noise;
4. calculate SCH101 tolerance-based CMRR;
5. consolidate DC offset propagation;
6. define switching-transient acceptance tests;
7. convert quantitative limits into commissioning tests.

## 10. Conclusion

The formal end-to-end review no longer identifies an RIAA architecture blocker.

The additional independent 3180 us stage is unnecessary because the older SCH103 architecture already implements complete RIAA. Restoring that architecture simplifies Shellac and removes the double-3180 failure mode without sacrificing capability.

The analogue signal-chain architecture can therefore be retained, subject to the remaining quantitative assurance work listed above.

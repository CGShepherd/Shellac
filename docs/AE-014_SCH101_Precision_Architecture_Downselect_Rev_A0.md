# AE-014 — SCH101 Precision Architecture Down-Selection

**Revision:** A0  
**Status:** DESIGN RECOMMENDATION — ready for schematic implementation after owner acceptance  
**Date:** 29 August 2026  
**Base commit:** `27f0a0eb641347925cb5e99e2c4f821553961bac`

## Executive conclusion

AE-013 identified two coupled weaknesses in the controlled SCH101 implementation: resistor-network Johnson noise and tolerance-limited CMRR.

AE-014 recommends solving both without changing the fundamental balanced-input topology or the established 14/18/22 dB user gain choices.

**Recommended architecture:**

1. retain the four OPA1656 non-inverting input legs;
2. reduce each leg's gain-setting impedance by approximately 10:1;
3. change the differential converter from the non-standard 3.48 ratio to a precision **4.000 ratio**;
4. implement the converter with **LT5400-7 A-grade, 1.25 kΩ / 5 kΩ**;
5. re-partition the selectable feedback ladder around **Rg = 1.000 kΩ**;
6. use **249 Ω fixed + 750 Ω DEFAULT addition + 1.91 kΩ HIGH addition**;
7. require approximately **0.01% relative matching** between corresponding gain-leg resistors.

This preserves the signal-chain gain budget while making a standard precision resistor network usable in the most CMRR-critical differential stage.

## 1. Why 4.00x rather than retaining 3.48x

The controlled 3.48x converter uses 10 kΩ / 34.8 kΩ. It is electrically valid but awkward as a high-precision monolithic ratio.

Analog Devices' current LT5400 catalogue provides standard ratios including 1:1, 1:4, 1:5, 1:9 and 1:10. The LT5400-7 is **1.25 kΩ / 5 kΩ = 1:4**. A-grade parts specify 0.01% general matching and 0.005% matching under the datasheet CMRR definition, with very low matching drift.

Moving to 4x therefore replaces an awkward custom precision ratio with a standard, characterised difference-amplifier network.

The required total gain is then restored in the preceding non-inverting legs.

## 2. Candidate realised gains

| Setting | Total RF per leg | Realised SCH101 gain | Error from target | Input-referred white-noise estimate | Deterministic CMRR floor* |
|---|---:|---:|---:|---:|---:|
| LOW | 249 Ω | 13.972 dB | -0.028 dB | 10.32 nV/√Hz | 78.4 dB |
| DEFAULT | 999 Ω | 18.057 dB | +0.057 dB | 9.21 nV/√Hz | 72.4 dB |
| HIGH | 2159 Ω | 22.032 dB | +0.032 dB | 8.88 nV/√Hz | 70.1 dB |

\* Corner model combines 0.01% gain-leg ratio uncertainty and 0.005% differential-converter CMRR matching. It does not include PCB, RF capacitor or switch parasitic imbalance.

All three established system gain choices remain within 0.07 dB of target. No downstream gain/headroom philosophy changes.

## 3. Gain ladder

Candidate per leg:

- Rg = 1.000 kΩ;
- LOW: RF = 249 Ω;
- DEFAULT: RF = 249 Ω + 750 Ω = 999 Ω;
- HIGH: RF = 249 Ω + 1.91 kΩ = 2.159 kΩ.

Resulting per-leg gains are approximately 1.249x, 1.999x and 3.159x. With the 4x converter these realise approximately 14, 18 and 22 dB total SCH101 gain.

The existing two-bit selector logic can therefore be retained conceptually. The switch still selects matched added feedback segments across all four balanced legs.

## 4. Precision-network strategy

### Differential converter — DOWN-SELECTED

**Preferred:** Analog Devices LT5400-7 A-grade.

Reasons:

- exact standard 1:4 ratio;
- 1.25 kΩ / 5 kΩ values are already in the desired low-noise impedance region;
- 0.01% A-grade matching;
- datasheet CMRR matching specification of 0.005%;
- 0.2 ppm/°C typical matching drift and ±1 ppm/°C maximum specification;
- MSOP-8 footprint;
- explicitly intended for difference-amplifier service;
- recommended for new designs by Analog Devices.

The exposed pad is electrically floating according to the datasheet. Layout should follow the manufacturer's symmetry guidance and avoid thermal gradients across the package.

### Gain legs — PREFERRED POLICY, PART FAMILY NOT YET FROZEN

The four corresponding resistors for each segment should track one another. There are three useful implementation levels:

**A — preferred production solution:** four-equal-resistor thin-film network per segment, 0.01% ratio class. Vishay MORN is technically attractive: four isolated resistors, ratio tolerance to 0.01%, tracking to 1 ppm/°C typical / 2 ppm/°C maximum, 400 Ω–100 kΩ per element, with factory consultation for additional values. The 249 Ω LOW segment is below the stated MORN 400 Ω range, however, so MORN cannot implement the complete proposed ladder unchanged.

**B — practical prototype solution:** individually selected 0.01% thin-film resistors for the 249 Ω / 750 Ω / 1.91 kΩ segments, placed as geometrically and thermally matched quartets. This meets the AE-014 deterministic tolerance model but has weaker guaranteed temperature tracking than a monolithic network.

**C — ACAS arrays:** Vishay ACAS is readily attractive mechanically and offers four isolated elements, but standard ACAS relative tolerance is 0.05%, not the 0.01% assumed by the preferred CMRR model. It is therefore not sufficient by itself for the final gain-leg precision target.

## 5. Alternative considered: preserve 3.48x

Retaining 3.48x would minimise mathematical change, but it forces either:

- custom precision networks;
- independent ultra-precision resistors with poorer thermal tracking;
- or a relaxed CMRR guarantee.

The 4x solution is cleaner because the precision-critical difference ratio becomes a standard catalogue component and the gain correction occurs in low-noise non-inverting feedback.

**Recommendation: reject the 3.48x converter for the next SCH101 revision.**

## 6. Noise consequence

AE-013 estimated the current DEFAULT front end at roughly 18 nV/√Hz input-referred.

The AE-014 candidate is below 9.5 nV/√Hz in the same first-order model. The improvement is approximately 6 dB and comes mainly from lowering the feedback/difference-network impedances.

This is a worthwhile improvement even though record surface noise will dominate practical 78-rpm replay.

## 7. Switch resistance sensitivity

The feedback-selector contacts are in series with selected RF additions. At approximately 1 kΩ-scale impedances, contact resistance matters more proportionally than in the original 10 kΩ-scale network.

Therefore the schematic implementation must not blindly retain the present DIP-switch assumption. The next implementation review shall:

- establish maximum and tracking contact resistance;
- place the switch so that any contact resistance appears symmetrically in corresponding legs;
- determine whether a sealed low-resistance DIP/relay arrangement is preferable;
- include contact resistance in gain-match/CMRR corners.

This is the principal new trade introduced by the lower-impedance ladder.

## 8. RF network and source balance

The two 100 Ω input series resistors and common-mode 1 nF capacitors must also be treated as a matched differential pair if high-frequency CMRR is to be meaningful.

The current 1% 100 Ω parts are acceptable for RF isolation but are not compatible with claiming a precision wideband CMRR number without further analysis.

Recommendation for the next schematic pass:

- move the two 100 Ω series resistors to 0.1% thin film or a matched pair;
- retain C0G/NP0 dielectric;
- use matched/tight-tolerance common-mode capacitors and symmetric placement;
- model the 220 pF differential capacitor separately because its mismatch mechanism differs.

## 9. Proposed acceptance requirements

AE-013 found no controlled system CMRR requirement. AE-014 therefore proposes requirements for formal adoption:

- **CMRR ≥ 70 dB from 20 Hz to 1 kHz** at all three gain settings;
- **CMRR ≥ 60 dB at 20 kHz**;
- DEFAULT SCH101 input-referred electronics noise target **≤ 10 nV/√Hz at 1 kHz**, excluding cartridge Johnson noise where measurement methodology requires;
- gain accuracy **±0.10 dB** at each gain setting;
- inter-leg/channel gain matching sufficiently tight that the above CMRR limits are met without calibration.

These are proposed engineering requirements, not retroactive baseline claims.

## 10. Decision state

Recommended for owner acceptance:

**DR-038 — SCH101 precision architecture**
- replace 3.48x converter with 4.00x precision converter;
- LT5400-7 A-grade preferred;
- reduce gain-ladder impedance around Rg = 1 kΩ;
- preserve 14/18/22 dB total gains;
- require 0.01% class gain-leg ratio control;
- requalify selector contact resistance and RF-input matching.

No SCH101 schematic is modified by this package. This keeps the design-history boundary clean: analysis/down-selection first, implementation after acceptance.

## 11. Next implementation phase

After DR-038 acceptance:

1. revise `balanced_input.py`;
2. revise SCH101 builder and footprints;
3. select exact gain resistor technology and switch;
4. extend CMRR model with switch resistance and RF tolerances;
5. rerun AE-012 headroom regression;
6. rerun AE-013/014 noise regression;
7. then continue full-chain integrated noise through SCH103, SCH107, SCH104, SCH105 and SCH108.

## Sources consulted

- Analog Devices, LT5400 product page and LT5400 Rev C datasheet.
- Vishay, MORN precision resistor-network datasheet/product page.
- Vishay, ACAS 0612 / ACAS 0612 AT precision-array datasheets/product pages.

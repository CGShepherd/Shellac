# AE-015 — Full-Chain Noise and DC-Offset Review

**Revision:** A0  
**Status:** NOISE ACCEPTABLE; DC ARCHITECTURE ACTION REQUIRED  
**Date:** 29 August 2026  
**Base commit:** `f51ef216c881773371359a5567a1a495f5815b9d`  
**Analysis basis:** DR-038 candidate SCH101 architecture

## 1. Scope

AE-015 extends the end-to-end review beyond gain/headroom into:

- output-referred electronics noise;
- source contribution by functional block;
- effect of SCH107 rumble filter on electronics noise;
- conservative DC-offset propagation from SCH101 to XLR;
- architectural mitigation of DC without compromising replay response.

No controlled schematic values are changed by this package.

## 2. Full-chain noise result

The numerical model propagates noise through the actual full-RIAA transfer function from 20 Hz to 20 kHz.

Included:

- DR-038 SCH101 candidate front-end: 9 nV/√Hz input-referred working figure;
- SCH103 OPA1612 voltage noise;
- exact thermal-noise contribution of the active LF feedback impedance;
- SCH103 750 Ω passive treble resistor;
- SCH103 10 kΩ / 11 kΩ recovery feedback network;
- SCH107 conservative Sallen-Key resistor/op-amp upper bound;
- SCH104 and SCH105 OPA1656 plus 100 Ω isolation;
- THAT1646 specified -101 dBu balanced output noise.

Approximate full-RIAA results at the default gain are:

| Condition | Balanced output noise | Electronics SNR vs nominal ~0.65 V RMS |
|---|---:|---:|
| Rumble bypass | ~109 µV RMS | ~75.5 dB |
| Rumble inserted | ~109 µV RMS | ~75.4 dB |

The result is dominated by SCH101 noise propagated through RIAA equalisation.

This is useful confirmation of the DR-038 direction: reducing the original SCH101 input-referred estimate from ~18 nV/√Hz to ~9 nV/√Hz buys nearly the expected 6 dB at system level.

The practical SNR of 78-rpm replay will generally be dominated by record/surface noise rather than this electronics figure.

## 3. Rumble-filter noise

A deliberately conservative upper-bound treatment of the two SCH107 Sallen-Key sections adds only about 12 µV RMS at the final balanced output.

Because SCH101 contributes roughly 108 µV RMS after the RIAA transfer, the filter changes the total electronics-noise result by well under 5%.

**Disposition: SCH107 noise does not justify redesign.**

A later SPICE noise analysis can replace the conservative resistor bound, but it is not a release blocker.

## 4. DC-offset finding

The direct-coupled signal path is much less comfortable.

The non-flat SCH103 active LF stage has DC noise gain:

`1 + 100k / 2.7k ≈ 38.0`

This means millivolt-scale static offset arriving from SCH101 is strongly amplified even though no useful audio signal exists at DC.

Using conservative data-sheet maximum offsets:

- OPA1656: 1 mV;
- OPA1612: 0.5 mV;
- THAT1646 differential output offset: 15 mV;

the DR-038 default-gain front-end can produce approximately **21 mV worst-case PRE_EQ offset** when all independent offsets take adverse signs.

The non-flat SCH103 path can then produce approximately **1.7 V DC at POST_EQ**, and the direct-coupled complete chain can exceed **3 V differential DC at the XLR** in a deliberately conservative worst-case stack-up.

This is not an acceptable architecture claim, even though a real unit is unlikely to hit every maximum with the same sign.

## 5. Why the rumble filter does not fully solve it

When SCH107 is inserted, its fourth-order high-pass response blocks DC.

However, the operator-selectable bypass path routes around that protection.

Therefore Shellac currently has a state-dependent DC behaviour:

- rumble FILTER: upstream DC rejected;
- rumble BYPASS: upstream DC can reach SCH104/SCH105/SCH108.

The bypass function should change frequency response, not determine whether multi-volt worst-case DC can reach the output.

## 6. Recommended architectural correction

Add one common DC-blocking network per channel at the **SCH103 output, before the SCH107 filter/bypass split**.

Proposed first-pass values:

- series capacitor: **1.0 µF film**;
- bias/reference resistor: **330 kΩ to 0VA**;
- first-order corner: approximately **0.48 Hz**.

At 20 Hz the additional amplitude loss is less than 0.01 dB, so it is effectively invisible to the replay curves and to the 15 Hz rumble-filter characteristic.

Because the capacitor is common to both SCH107 paths:

- FILTER remains DC-blocked;
- BYPASS becomes DC-blocked;
- SCH101 and SCH103 static offsets no longer propagate to the output;
- no electrolytic is required if suitable 1 µF film packaging is accepted.

The conservative remaining downstream differential DC estimate becomes approximately **19 mV**, dominated by downstream op-amp maxima plus the THAT1646 differential offset specification.

## 7. Why the block belongs after SCH103

Placing the capacitor between SCH101 and SCH103 would protect SCH103 from front-end offset but would not remove SCH103's own amplified input offset.

Placing it after SCH103 removes both:

- SCH101-originated offset;
- SCH103 LF-stage and recovery-stage offset.

It also gives one common DC architecture for both rumble-filter states.

This is therefore the preferred location.

## 8. Interaction with replay equalisation

The proposed 0.48 Hz high-pass pole is more than an order of magnitude below the existing 15 Hz rumble filter and about two orders below the 50 Hz RIAA low-frequency break.

Its calculated loss at 20 Hz is negligible.

Nevertheless the final implementation must rerun:

- AE-003 replay-curve error;
- AE-012 headroom;
- AE-015 noise;
- phase response below 20 Hz;
- startup/mute transient analysis.

## 9. Interaction with switching

A post-EQ coupling capacitor creates a stored-charge node.

Therefore DR-039 must be implemented together with:

- a defined 330 kΩ DC reference on the downstream side;
- break-before-make rumble switching retained;
- mute-state transient testing;
- power-up/power-down settling test.

The large resistor gives a time constant of about 0.33 s. Five time constants is about 1.65 s, which should be considered when defining commissioning and mute timing.

## 10. Release disposition

### GREEN

- DR-038 noise improvement is materially beneficial at system level;
- complete-RIAA electronics noise;
- SCH107 noise contribution;
- THAT1646 intrinsic noise contribution.

### RED / ARCHITECTURE ACTION

- direct-coupled POST_EQ -> rumble-bypass -> output DC path.

## 11. Proposed decision

**DR-039 — Common post-EQ DC block**

Add a 1.0 µF film / 330 kΩ first-order DC block per channel immediately after SCH103 and before the SCH107 bypass split.

This should be accepted before final SCH101 physical implementation because the resulting transient/commissioning behaviour belongs in the same end-to-end closure.

## 12. Next phase after acceptance

1. implement DR-039 in the controlled model and SCH103/SCH107 interface;
2. implement DR-038 physically, including the LT5400-7 and precision gain configuration;
3. rerun all replay-curve and headroom tests;
4. add switching/power transient acceptance;
5. then close AE-011 end-to-end electrical review.

# AE-012 — Project Shellac All-State Gain and Headroom Closure

**Revision:** A0  
**Status:** CONTROLLED ANALYSIS — gain/headroom architecture closed with operating-envelope constraint  
**Date:** 29 August 2026  
**Base commit:** `da19a2721c8adfa4d6fedcc0a4f419fa32c4b796`  
**Depends on:** DR-037, AE-011 A1

## 1. Scope

AE-012 performs a dense end-to-end gain/headroom sweep of:

`Cartridge -> SCH101 -> SCH103 -> SCH107 -> SCH104 -> SCH105 -> SCH108 -> XLR`

Swept dimensions:

- SCH101 LOW / DEFAULT / HIGH;
- all 20 historical Bass/Treble combinations;
- constrained complete RIAA: TRUE RIAA 3180/318 us + 2121 Hz RIAA;
- rumble FILTER/BYPASS;
- 2001 logarithmically spaced frequencies from 5 Hz to 20 kHz;
- 5 mV RMS nominal cartridge reference.

SCH105 does not create a larger single-channel amplitude case: Stereo/Dual modes are unity and `(L+R)/2` preserves equal correlated-channel amplitude.

## 2. Principal result

The limiting nominal 5 mV RMS wanted-band case is:

- SCH101 HIGH;
- complete RIAA;
- rumble BYPASS;
- approximately 20 Hz;
- approximately **9.32 V RMS differential** at the XLR;
- approximately **0.61 dB margin** to Shellac's conservative 10 V RMS differential design ceiling.

This is not a predicted THAT1646 hardware clip. The controlled SCH108 model records approximately 18 V RMS datasheet capability; 10 V RMS is the deliberately conservative Shellac engineering ceiling.

## 3. Gain-setting comparison

| SCH101 gain | Worst wanted-band condition | XLR differential | Margin to 10 V RMS |
|---|---|---:|---:|
| LOW | full RIAA, rumble bypass, ~20 Hz | 3.72 V RMS | 8.58 dB |
| DEFAULT | full RIAA, rumble bypass, ~20 Hz | 5.86 V RMS | 4.64 dB |
| HIGH | full RIAA, rumble bypass, ~20 Hz | 9.32 V RMS | 0.61 dB |

DEFAULT therefore remains the correct normal setting for the 5 mV reference.

## 4. HIGH-gain operating envelope

At the limiting HIGH/RIAA/bypass point, the 10 V RMS conservative XLR ceiling corresponds to approximately **5.36 mV RMS cartridge input** near 20 Hz.

Therefore HIGH is retained as a lower-output-cartridge sensitivity setting. It should not be documented as a universally interchangeable louder setting for a nominal 5 mV cartridge.

No circuit-value change is recommended.

## 5. First active-stage headroom

The SCH103 first active LF stage retains substantially more margin than the conservative final XLR ceiling in the limiting case. The all-state nominal limit is therefore the deliberately conservative balanced-output ceiling, not an SCH103 active-stage overload.

## 6. Rumble-filter effect

Below the wanted band SCH107 materially improves system headroom. Around 20 Hz its attenuation is intentionally small, so the wanted-band worst case remains largely unchanged.

## 7. Disposition

**GREEN:** LOW, DEFAULT, complete RIAA, historical EQ, SCH104 unity, SCH105 mode behaviour, SCH108 gain placement.

**GREEN WITH OPERATING CONSTRAINT:** HIGH gain. Retain it for lower-output cartridges and document the reduced nominal 5 mV low-frequency margin.

## 8. Next assurance work

1. integrated noise;
2. tolerance-based SCH101 CMRR;
3. DC-offset propagation;
4. switching-transient acceptance;
5. commissioning limits incorporating the HIGH-gain operating envelope.

## 9. Conclusion

No circuit redesign is required. The end-to-end gain/headroom architecture is closed subject to the recorded HIGH-gain operating constraint.

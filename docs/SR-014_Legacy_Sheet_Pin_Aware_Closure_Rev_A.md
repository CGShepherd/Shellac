# Project Shellac — SR-014 Legacy Sheet Pin-Aware Closure Rev A

## Status

Implemented and regression validated against the accepted SR-013 repository.

## Purpose

Close the two remaining legacy renderer implementations, SCH101 and SCH106, by replacing coordinate-based illustrative wiring with semantic named-pin connectivity. No validated analogue target, component tolerance, supply voltage, gain target, or external interface is changed.

## SCH101 closure

SCH101 now emits pin-level connectivity for both input XLRs, RF filters, four balanced gain legs, the stereo gain selector, both precision differential converters, supplies, ground and pre-EQ outputs.

The audit exposed one physical-realisation gap in the previous gain-selector drawing: two DIP contacts per gain leg cannot select among three independent feedback resistors. The corrected implementation uses one fixed 4.42 kΩ feedback base and two series add-on segments shunted by the existing two DIP contacts:

| Setting | Inserted feedback | Effective feedback | Total SCH101 gain |
|---|---:|---:|---:|
| Low `00` | none | 4.42 kΩ | 14.011 dB |
| Default `01` | 8.28 kΩ | 12.70 kΩ | 17.952 dB |
| High `10` | 21.68 kΩ | 26.10 kΩ | 21.982 dB |
| Reserved `11` | both segments | 34.38 kΩ | not an approved operating setting |

The selector remains one eight-way SPST DIP bank: two contacts are repeated across L+, L−, R+ and R−. All four legs must use the same two-bit pattern. This is an implementation closure of the previously approved three gain settings, not a gain-policy change.

## SCH106 closure

SCH106 now emits semantic connections for the five-pin PSU inlet, input test points, rail links, local bulk and high-frequency bypassing, bleeders, configurable 0VA/chassis bond and antiparallel DNP clamps.

Connector assignment remains:

1. 0VA
2. +18VA input
3. −18VA input
4. chassis
5. reserved/no connection

## Evidence

- Python regression suite: 117 passed.
- Engineering Model: validation passed; 8 blocks and 27 signals.
- Model-driven build: 8 implemented, 0 pending.
- Readiness audit: all 8 sheets CAD-ready; root contains 8 sheets, 66 pins and 19 cross-sheet signals.
- Native KiCad hierarchical ERC: 286 findings, reduced from the accepted SR-013 baseline of 600.

The remaining ERC report is dominated by 239 library-resolution warnings from the deliberately isolated KiCad validation profile. The actionable balance is 28 dangling labels, 10 multiple-net-name findings, 8 footprint-library warnings and one power-not-driven finding. These are renderer/library closure tasks; they do not reopen the analogue design.

## Next critical-path increment

Close generated project library tables and root/child hierarchy label attachment, then repeat native KiCad ERC before the first visual schematic capture review.

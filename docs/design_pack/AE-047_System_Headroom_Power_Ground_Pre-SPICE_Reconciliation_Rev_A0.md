# AE-047 — System Headroom and Power/Ground Pre-SPICE Reconciliation
**Project:** Shellac
**Status:** INTERIM / ANALYSED / SPICE REQUIRED
**Date:** 2026-09-11

## Purpose
Reconcile the complete signal/headroom model and the SCH106 power/ground implementation before constructing the end-to-end SPICE model.

## 1. Signal-chain model status
The current `generator/model/signal_chain_analysis.py` remains useful historical evidence but is not yet release-authoritative.

It currently composes:
- SCH101 gain settings from the older `balanced_input.py`;
- SCH103 EQ;
- isolated DR-039 transfer;
- SCH107 rumble response;
- SCH108 x2 differential gain.

The current headroom sweep therefore does not yet represent all latest controlled decisions.

## 2. SCH101 model reconciliation
The live `balanced_input.py` still represents the older effective gain-network scheme:
- LOW effective RF = 249 Ohm
- DEFAULT effective RF = 999 Ohm
- HIGH effective RF = 2159 Ohm

The selected fail-safe architecture is instead:
- fixed RF = 999 Ohm
- fixed RG = 1000 Ohm
- LOW by 332 Ohm parallel RF shunt
- DEFAULT by no shunt
- HIGH by 866 Ohm parallel RG shunt.

However, the realised total gains are numerically nearly unchanged:
- LOW: old 13.97245 dB, new 13.97375 dB, delta +0.00130 dB
- DEFAULT: old 18.05746 dB, new 18.05700 dB, delta -0.00046 dB
- HIGH: old 22.03219 dB, new 22.01452 dB, delta -0.01767 dB

Conclusion:
- topology/implementation model = STALE
- existing headroom results are not materially invalidated by gain magnitude alone
- the model must still be updated before baseline because implementation evidence must match intent.

## 3. Cartridge assumption is more important than gain delta
The current SCH103 model defines one nominal cartridge level:
- NOMINAL_CARTRIDGE_RMS_V = 5 mV.

The current signal-chain test explicitly states that HIGH gain is not a universal 5 mV operating setting and that the existing 5 mV RIAA worst case leaves only about 0.5-0.8 dB output margin, with an inferred cartridge limit around 5.2-5.6 mV.

This is a genuine design-envelope result.

The revised qualification set must separately model:
- Grado 78E primary 78-rpm family
- Audio-Technica AT-VM95SP primary 78-rpm family
- Grado Gold / 8MZ LP compatibility
- optional tolerated generic 47 kOhm MM/MI envelope.

Gain settings should therefore be validated as operating envelopes, not assumed universally interchangeable.

## 4. DR-039 coupling model is no longer authoritative
The signal-chain model currently multiplies by the isolated `post_eq_dc_block` transfer.

AE-044 established that the real 1 uF / 330 kOhm network is materially loaded by continuously driven SCH107.

Therefore:
- current end-to-end response/headroom sweep is not an integrated model;
- if DR-039 is relocated or SCH107 impedance-scaled, the full-chain transfer changes;
- this change can increase wanted-band level relative to the current loaded hardware, reducing headroom compared with the present integrated circuit.

The final SPICE model must calculate the actual node voltages directly rather than multiply isolated scalar transfer functions.

## 5. Severe-signal constants are historically inconsistent
Older local models contain:
- SCH104 severe input = 3.21 Vrms
- SCH108 severe input = 3.21 Vrms -> 6.42 Vrms differential output
- later SCH105 model severe input = 6.42 Vrms.

These cannot all represent the same physical node.

Disposition:
- no local `SEVERE_INPUT_RMS_V` constant is release authority;
- establish one end-to-end node-by-node stress vector from cartridge input through XLR output;
- derive each node limit from the actual selected gain/EQ/filter/matrix state.

## 6. Headroom acceptance strategy
Full SPICE shall distinguish:
1. nominal cartridge output;
2. realistic hot-record / high-velocity transient;
3. overload test level;
4. absolute clipping onset.

The gain selector shall be treated as operator configuration:
- LOW: highest input-level tolerance;
- DEFAULT: normal default;
- HIGH: low-output cartridge / selected use case, not universal 5 mV mode.

Acceptance should specify minimum overload margin per qualified cartridge family and gain setting rather than one generic 'severe' number.

## 7. SCH106 power entry
The live power-entry generator confirms:
- external regulated +18 V / 0VA / -18 V / CHASSIS;
- 0 Ohm series entry links on each rail;
- 470 uF bulk per rail;
- 1 uF + 100 nF bypass per rail;
- 22 kOhm bleed per rail;
- R909 = 0 Ohm direct 0VA-to-CHASSIS bond fitted;
- C909 = 100 nF film 0VA-to-CHASSIS bond also fitted in parallel;
- opposed clamp diodes D901/D902 DNP.

## 8. Ground-bond minimality issue
With R909 = 0 Ohm fitted, C909 is electrically in parallel with an effective short circuit.

Therefore C909 provides no meaningful additional AC bonding function in the selected direct-bond configuration.

Disposition:
- R909 direct bond: RETAIN provisionally, pending system grounding/hum review.
- C909: DNP CANDIDATE in the selected direct-bond build.
- D901/D902: retain footprints only if a controlled alternative ground-lift configuration is still a requirement; otherwise later REMOVE/DNP review.

This is exactly the type of extraneous populated function the final minimality pass is intended to identify.

## 9. Phantom-fault energy path
SCH108 output clamps return fault current into the +/-18 V rails.

SCH106 provides:
- 470 uF local bulk rail storage;
- 22 kOhm bleeders;
- external regulated supply through effectively zero-ohm links.

The critical question is whether the external regulator and rail capacitance can safely absorb phantom-discharge energy.

The 22 kOhm bleeders are far too high in resistance to be meaningful pulse-energy sinks.

SPICE must therefore model:
- the external supply/regulator output impedance and reverse-current behaviour;
- cable/harness resistance and inductance;
- local 470 uF rail capacitors;
- THAT1646 clamp diodes;
- representative downstream phantom network.

Do not represent +/-18 V as ideal zero-impedance voltage sources for this fault test.

## 10. Required end-to-end SPICE model
The first release-intent full-chain model should include:
- cartridge R/L/source voltage;
- input loading and cable capacitance;
- actual fail-safe SCH101 gain network;
- LT5400 converter;
- SCH103 active LF and passive HF networks;
- DR-039 in its candidate integrated topology;
- SCH107 actual candidate impedance scale;
- SCH104 unity buffers and mono legs;
- SCH105 full matrix and 2.2 MOhm returns;
- SW905 mute;
- THAT1646;
- sense capacitors;
- ferrite/RFI network;
- realistic downstream balanced load/cable;
- non-ideal +/-18 V supply rails for transient/fault work.

## 11. Model hierarchy
Use one authoritative circuit netlist/model for node voltages.

Analytical helper models should then be used for:
- sanity checks;
- tolerance derivations;
- reporting;
- regression tests.

They should not independently define conflicting severe-level or isolated-transfer assumptions.

## 12. Intent/minimality disposition
RETAIN:
- regulated +/-18 V architecture;
- 470 uF local rail bulk;
- local bypassing;
- 22 kOhm bleeders;
- direct 0VA-CHASSIS bond provisionally;
- rail entry links;
- test points.

MODIFY / UPDATE:
- SCH101 analytical model to fail-safe gain topology;
- cartridge qualification set;
- signal-chain analysis to use integrated DR-039/SCH107 behaviour;
- severe-signal methodology.

DNP CANDIDATE:
- C909 when R909 0 Ohm direct bond is fitted.

EVIDENCE REQUIRED:
- direct-bond grounding/noise behaviour;
- phantom fault rail excursion;
- regulator reverse-energy tolerance;
- final gain/cartridge overload matrix;
- exact end-to-end node headroom.

## Gate status
System signal/headroom model = RECONCILIATION REQUIRED before baseline.
Power architecture = INTENT-CONFORMANT, phantom-fault qualification open.
Ground bond = DIRECT-BOND ARCHITECTURE PROVISIONALLY VALID, parallel C909 population appears redundant.

## Confidence
- existing SCH101 model topology is stale: 100%
- gain magnitude delta is negligible for prior headroom conclusions: 99%
- cartridge assumptions dominate gain-choice/headroom envelope more than the gain-topology delta: 99%
- severe-level constants require reconciliation: 100%
- C909 is electrically redundant when R909=0 Ohm is fitted: 100%
- phantom fault requires non-ideal rail modelling: 99%

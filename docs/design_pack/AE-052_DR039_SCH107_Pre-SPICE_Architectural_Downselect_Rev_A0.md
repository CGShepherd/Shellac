# AE-052 — DR-039 / SCH107 Pre-SPICE Architectural Down-Select
**Project:** Shellac
**Status:** INTERIM / ANALYSED / SPICE REQUIRED
**Date:** 2026-09-11

## 1. Purpose
Resolve as much of the DR-039 / SCH107 interaction defect as possible before full-system SPICE.

AE-044 established that the current common 1 uF / 330 kOhm post-EQ block is materially loaded by the continuously-driven SCH107 input and therefore does not behave as the isolated ~0.48 Hz pole assumed by the original DR-039 model.

## 2. Critical topology observation
The live SCH107 implementation is a conventional two-stage unity-gain Sallen-Key high-pass filter.

Each section uses:
- series C1;
- series C2;
- R1 feedback from the C1/C2 junction to op-amp output;
- R2 shunt from the second-capacitor / op-amp-input node to 0VA;
- OPA1656 unity follower.

Therefore the SCH107 filtered branch is intrinsically DC-blocking.

At DC:
- C1 and C2 are open circuits;
- the op-amp input is referenced to 0VA through R2;
- the unity follower output tends to 0 V apart from normal op-amp offset.

The filter therefore does not require the separate DR-039 series capacitor in order to reject SCH103 DC.

## 3. Preferred architecture
Move the dedicated DR-039 components from the common pre-split node into the direct bypass branch only.

Per channel:

SCH103_OUT
    |
    +---- 1 uF film ---- DIRECT_DC_BLOCKED ----> SW904 DIRECT
    |                     |
    |                    330 kOhm
    |                     |
    |                    0VA
    |
    +---- existing SCH107 HPF -----------------> SW904 FILTER

SW904 output then feeds SCH104 as presently intended.

## 4. Component-count consequence
This architecture uses exactly the same dedicated DR-039 population as the present design:
- one 1 uF film capacitor per channel;
- one 330 kOhm resistor per channel.

No additional coupling capacitor or bias resistor is required on the filter branch because SCH107 already performs that DC-blocking function.

Thus the change is primarily a topology/location correction, not a BOM increase.

## 5. Direct-path LF response
For 1 uF and 330 kOhm:

fc = 1 / (2*pi*330k*1u) = approximately 0.4823 Hz.

Approximate additional direct-path attenuation:
- 10 Hz: -0.0101 dB
- 15 Hz: -0.00449 dB
- 20 Hz: -0.00252 dB
- 30 Hz: -0.00112 dB
- 50 Hz: -0.00040 dB

This comfortably satisfies the AE-049 LF coupling criterion:
- 20 Hz preferred <= 0.10 dB;
- 20 Hz maximum <= 0.20 dB;
- 50 Hz preferred <= 0.05 dB.

## 6. Filter-path consequence
The filtered branch retains the original SCH107 component values:
Section A:
- C1=C2=470 nF
- R1=20.8 kOhm
- R2=24.3 kOhm

Section B:
- C1=C2=470 nF
- R1=8.66 kOhm
- R2=59.0 kOhm

No impedance scaling is required merely to correct DR-039 loading.

Benefits:
- preserves existing nominal 4th-order Butterworth synthesis;
- preserves prior noise assumptions;
- avoids high-value resistor thermal-noise trade;
- avoids new timing-capacitor tolerance optimisation solely caused by scaling;
- avoids changing a working filter to solve an interface error outside its core function.

## 7. Switching/DC consequence
SW904 would select between:
- DIRECT input referenced to 0VA by the post-capacitor 330 kOhm resistor;
- FILTER input whose output is naturally DC-referenced near 0VA by the high-pass topology and OPA1656 offset.

This is materially better than moving a common coupling capacitor after SW904.

The rejected post-switch common-block candidate could see a large branch-to-branch DC step and charge the common capacitor, producing a potentially long settling transient.

The preferred branch-local arrangement instead seeks to make both switch inputs approximately DC-neutral before selection.

Remaining transient mechanisms are therefore:
- OPA1656 output offset;
- capacitor charge mismatch;
- BBM break interval;
- switch parasitics;
- signal discontinuity between direct and filtered waveforms.

These still require transient SPICE and bench confirmation but are substantially lower-risk than switching raw DC into a downstream coupling capacitor.

## 8. Disposition of previous candidates

### REJECT
1. Current common pre-split 1 uF / 330 kOhm topology
   - integrated LF response fails due to SCH107 loading.

2. Post-switch common DC block
   - low component count but creates avoidable DC-step/charge-settling risk at SW904.

3. x2 / x5 SCH107 impedance scaling as sole correction
   - insufficient LF improvement with 1 uF and unnecessary filter redesign.

### DEPRIORITISE
4. x10 SCH107 scaling + approximately 1.2 uF
   - analytically viable;
   - ~-0.091 dB coupling loss at 20 Hz;
   - common 47 nF timing capacitors attractive;
   - but introduces higher resistor-noise risk and changes a previously coherent filter solely to solve the coupling-interface problem.

5. x20 scaling
   - electrically viable but unnecessarily high resistor values.

### PREFERRED FOR SPICE
6. Branch-local DR-039:
   - direct branch receives 1 uF / 330 kOhm;
   - filtered branch relies on intrinsic SCH107 DC blocking;
   - no additional filtered-branch coupling capacitor;
   - original SCH107 impedance retained.

## 9. SPICE questions remaining
The full-system model shall verify:
1. direct-path 20/30/50 Hz response;
2. filter-path nominal response unchanged;
3. DC at both SW904 inputs across worst-case SCH103 offset;
4. SW904 FILTER<->BYPASS transient under MUTE;
5. live-switch stress transient;
6. filter op-amp output DC offset contribution;
7. startup and shutdown charge behaviour;
8. noise versus present SCH107 design;
9. interaction with SCH104 input impedance and parasitics.

## 10. Design-intent conclusion
The original DR-039 requirement remains valid:
state-independent suppression of SCH103 DC before downstream gain/output stages.

However the requirement need not be implemented as one common capacitor ahead of both branches.

The preferred implementation uses each branch's natural architecture:
- explicit coupling capacitor on the direct branch;
- intrinsic high-pass DC blocking on the filtered branch.

This is more functionally minimal than changing SCH107 impedance or adding duplicated coupling components.

## Confidence
- SCH107 filtered branch intrinsically blocks DC: 100%
- branch-local direct-path 1 uF / 330 kOhm solves the analytical LF-loading defect: 99%
- dedicated DR-039 component count remains unchanged: 100%
- preserving original SCH107 values is preferable to x10 scaling before SPICE: 98%
- branch-local architecture is strongest current candidate: 98%
- transient/offset details still require SPICE and bench evidence: 100%

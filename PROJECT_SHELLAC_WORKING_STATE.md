# Project Shellac — Persistent Working State

**Purpose:** cross-chat continuity and execution index.
**Authority status:** NON-AUTHORITATIVE SUMMARY. If this file conflicts with controlled current authority, the controlled authority wins and this file must be corrected before further major work.
**Refresh rule:** update after every material engineering review, qualification pass, governed transaction, commit/push, or change to the critical path.

## 1. Repository baseline

- Branch: `develop`
- Verified parent baseline at start of current transaction: `46bfd380193fc6008cdcb2f7ae8acece597f8f80`
- Parent subject: `AE-076C: reconcile pre-layout authority and technical debt`
- Current working transaction: `AE-076D — executable authority, qualification delta, persistent state and one-off recoverability`
- Current transaction state: VALIDATED_UNSTAGED_CANDIDATE — authority audit PASS; full suite 754/754; `git diff --check` PASS; promotion status must be verified live from Git
- Routing: HELD
- Layout freeze: FALSE
- BOM freeze: FALSE
- Manufacturing release: FALSE

## 2. Current design essentials

- Regulated rails: `+17.0 V / 0VA / -17.0 V`.
- One main audio PCB carries all seven controls directly.
- PCB orientation: F.Cu down / B.Cu up toward removable upper cover.
- Six PCB-to-upper-cover primary supports selected in principle; exact XY/Z/hardware/tolerance open.
- Bass: NKK `NR01105ANG13-2C` x2.
- Treble: NKK `NR01105ANG13-2A` x2.
- Channel Matrix production part: C&K `A30403RNCB`; MRJE3404 is provenance/considered alternative only.
- Rumble/Mute: C&K `7201SYCBE`.
- SCH101 LT5400: `LT5400BIMS8E-7#PBF`; EP9 to quiet 0VA implemented.
- Gain programming: TSW-104-07-G-D / MNT-104-BK-G, approximately 14/18/22 dB; no LOW/HIGH shunt = fail-safe ~18 dB.
- Cartridge loading selected-next: two identical per-channel passive differential-load cards; no card=BASE; matched +47 pF and +100 pF L/R service pairs; audio path does not pass through card.
- Live cartridge-load implementation remains H120/H121/H122 until controlled migration to per-channel H120/H220.
- DR-039 current implementation: branch-local 1 uF / 330 kOhm only in DIRECT/BYPASS; FILTER uses intrinsic SCH107 high-pass DC blocking.
- Grounding population: R909=0 ohm fitted; C909/D901/D902 DNP.
- H801/H802 output harness is HOT/COLD only with no 0VA conductor.
- Five-pole regulated-DC interface: pin1=0VA, pin2=+17 V, pin3=-17 V, pin4=CHASSIS, pin5 NC_RESERVED; pin1-shell bond prohibited.

## 3. Current one-off build philosophy

Shellac is expected to be a one-off build, not an iterative prototype-to-production programme.

Before fabrication, unresolved items must be classified as:
- `CLOSE_BEFORE_FAB`;
- `ESCAPE_ROUTE_REQUIRED`;
- `BENCH_ONLY_ACCEPTABLE`.

Where a residual uncertainty could otherwise require board or mechanical respin, provide a controlled low-impact recovery mechanism when technically sensible. Do not add speculative flexibility, especially in the cartridge/SCH101 low-level region.

Controlled standard:
`docs/knowledge/ONE_OFF_BUILD_RECOVERABILITY_STANDARD.md`

## 4. Current pre-layout critical path

1. Promote AE-076D after final diff/semantic review.
2. Controlled personality/native-CAD migration:
   - exact SLW-102-01-G-D / TSW-102-07-G-D personality interface;
   - per-channel H120/H220 live migration;
   - diagonal duplicate-node pin-map verification;
   - H901 exact governed model binding;
   - C30060/C35060 governed model binding;
   - reproduce zero-missing-model PCB STEP.
3. RUN08-RUN14 design-driving closure against the current qualification delta.
4. Resolve RUN10-driven component/value issues including SCH103 timing-cap decomposition and personality-interface parasitics/matching.
5. Resolve SCH108 ferrite selection to the extent required before layout, retaining bench correlation where appropriate.
6. Complete exact seven-control pin/pad/orientation/footprint implementation.
7. Complete six-support/top-cover/control-plane/full-service MCAD.
8. Freeze bounded four-layer fabrication stack, quantitative DRC/netclasses and instantiate/audit In1 0VA plane.
9. Formal block-by-block independent review.
10. Consider routing release only with zero `HOLD` dispositions.

## 5. Formal block-review sequence

Review in this order:
1. cartridge / input XLR / harness;
2. SCH101 RF, loading, gain and precision front end;
3. SCH103 replay EQ;
4. SCH107 rumble/direct path/DC blocking;
5. SCH104 isolation and mono preparation;
6. SCH105 channel Matrix;
7. SCH108 mute, THAT1646, ferrites, clamps and output interface;
8. 0VA / CHASSIS / earthing;
9. +17 V / 0VA / -17 V distribution;
10. external PSU: mains inlet through transformer, rectification, regulation, protection and DC cable.

Each block must end as:
- `PASS_FOR_LAYOUT`;
- `PASS_WITH_CONTROLLED_RECOVERY`;
- `HOLD`.

For every block review: implementation, evidence, component authority, PCB/MCAD, interfaces, FMEA/fault behaviour, procurement, serviceability, recovery path and residual qualification must be explicit.

## 6. Known open design-driving items

- personality-interface exact CAD/native migration;
- H901/C30060/C35060 governed native 3D binding;
- gain-shunt physical pairing/orientation;
- RUN08 overload/clipping/recovery;
- RUN09 full-system noise;
- RUN10 tolerance/sensitivity/value engineering/parasitics;
- RUN11 Monte Carlo;
- RUN12 switching transients;
- RUN13 rail variation/ripple/start-up;
- RUN14 phantom/fault energy;
- SCH103 timing-cap source/value decomposition;
- SCH108 ferrite selection;
- exact seven-control B.Cu pin/pad/orientation mapping;
- six-support/control-plane/full-chassis MCAD;
- bounded fabrication stack, In1 plane and quantitative DRC/netclasses;
- Grado 20-50 kHz model-validity/measurement disposition;
- PSU powered set-point/dropout/ripple/startup/thermal qualification.

## 7. Explicitly deferred to build/commissioning where presently acceptable

These remain subject to the recoverability standard and may move back to pre-fabrication closure if review shows respin risk:

- physical harness/crimp continuity;
- actual cartridge body/return continuity measurement;
- measured noise/CMRR/distortion correlation where no PCB change is expected;
- final hum/grounding confirmation with controlled R909/C909/D901/D902 population options;
- thermal measurements with the final assembled enclosure;
- load/cable stability and high-level PRE90 confirmation where design margin/recovery remains adequate.

## 8. Validation

- AE-076C governed baseline full suite: 743 passed.
- AE-076D transaction: reported clean by local execution; this persistence transaction re-runs the current authority audit and complete regression suite.
- Persistence transaction full-suite result: PASS — 754 tests
- `git diff --check`: PASS on the validated FIX4 candidate; rerun after this semantic cleanup and before staging.

## 9. Continuity rule

Do not begin a major new Shellac phase from conversation memory alone.

At the start of a new chat:
1. read this file in full;
2. read `PROJECT_GUIDANCE.md`;
3. verify Git branch/HEAD/origin/working-tree state;
4. inspect the current authority files referenced by this summary for the task at hand;
5. update this file again before the next major phase transition.

This file is an index, not a substitute for controlled design records.

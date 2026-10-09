# Project Shellac — Persistent Working State

**Purpose:** cross-chat continuity and execution index.
**Authority status:** NON-AUTHORITATIVE SUMMARY. If this file conflicts with controlled current authority, the controlled authority wins and this file must be corrected before further major work.
**Refresh rule:** update after every material engineering review, qualification pass, governed transaction, commit/push, or change to the critical path.

## 1. Repository baseline

- Branch: `develop`
- Current governed `develop` baseline: `2a912eac1c63313443f99dc87f86e07232f1a40b`
- Governed subject: `AE-076E-B: reconcile native personality interface and STEP model authority`
- Promotion parent (historical AE-076E-A): `258751f56f536cc28e836c2d013dbde46aaf4cb6`
- Current working phase: `AE-076F — pre-layout qualification and mechanical-support comparison`
- Current transaction state: AE076E_B_PROMOTED_AE076F_QUALIFICATION_AND_MCAD_HELD — AE-076E-B promoted; read-only AE-076F startup PASS, 767 tests and authority audit; current physical/electrical holds unchanged
- Routing: HELD
- Layout freeze: FALSE
- BOM freeze: FALSE
- Manufacturing release: FALSE

## 2. Current design essentials

- Regulated rails: `+17.0 V / 0VA / -17.0 V`.
- One main audio PCB carries all seven controls directly.
- PCB orientation: F.Cu down / B.Cu up toward removable upper cover.
- Current selected architecture remains six PCB-to-upper-cover primary supports; exact XY/Z/hardware/tolerance open. AE-076F is evaluating rail-supported alternatives, including a 1.5/1.6 mm slot-engaging sheet with narrower bolted/bonded >=2 mm reinforcement and a two-level skeletal frame; no supersession authorised.
- Bass: NKK `NR01105ANG13-2C` x2.
- Treble: NKK `NR01105ANG13-2A` x2.
- Channel Matrix production part: C&K `A30403RNCB`; MRJE3404 is provenance/considered alternative only.
- Rumble/Mute: C&K `7201SYCBE`.
- SCH101 LT5400: `LT5400BIMS8E-7#PBF`; EP9 to quiet 0VA implemented.
- Gain programming: TSW-104-07-G-D / MNT-104-BK-G, approximately 14/18/22 dB; no LOW/HIGH shunt = fail-safe ~18 dB.
- Cartridge loading: live dual per-channel main-board sockets, separate service cards remain qualification-open; no card=BASE; matched +47 pF and +100 pF L/R service pairs; audio path does not pass through card.
- AE-076E-A exact primitive: Samtec `SLW-102-01-G-D`, controlled 2x2 PTH footprint, pins 1/4=POS and 2/3=NEG; no generic 3D model substituted.
- Live generator and native PCB now implement per-channel H120/H220; H121/H122/C103/C104/C203/C204 are absent from the PCB, while H120 retains pins 1/4=POS and 2/3=NEG.
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

1. AE-076E-B promotion: COMPLETE and locally verified at `2a912eac1c63313443f99dc87f86e07232f1a40b`; keep immutable AE-076E-A parent `258751f56f536cc28e836c2d013dbde46aaf4cb6` as provenance. AE-076F0 reconciles the execution index, continuity test and narrow risk-register drift without altering design/release authority.
2. Perform bounded preliminary RUN10 design-driving tolerance/parasitic assessment at current `+17.0 V / 0VA / -17.0 V`, especially LT5400/CMRR, gain shunts, Grado 78C cable/loading and H120/H220 service-card parasitics, and SCH103 timing-component source/value choices. This is not full RUN10 closure.
3. MCAD mechanical support comparison: retain current six-upper-cover-support selection pending dimensional evidence; evaluate 1.5/1.6 mm groove-engaging rail sheet with narrower >=2 mm reinforcement (bolted versus bonded), two-level 1.5/1.6 mm rail-engaged skeletal frames and other simpler stiffening. Check true slot throat, enclosure width, NKK 12.3 mm panel-to-PCB constraint, seven switch envelopes, F.Cu component/card clearance, cover drop fit, retention, grounding, deflection, access and assembly sequence. No carrier selected yet.
4. Complete RUN08-RUN14 under the current AE-076D qualification delta; preserve the AE-070 vendor THAT1646 full-chain AC model composition limit and prohibit transferring AC surrogate validity to nonlinear/noise/fault gates.
5. Resolve RUN10-driven SCH103 timing-cap decomposition and SCH108 ferrite selection before layout as justified; retain bench correlation where defensible.
6. Complete exact seven-control B.Cu footprint/pin/pad/orientation/3D and support implementation after mechanical selection; do not modify governed native placement prematurely.
7. Qualify ±17 V physical PSU set-point/dropout/ripple/startup/thermal behaviour, system rail fault-energy response and deliberate CHASSIS/0VA interfaces before system sign-off.
8. Freeze bounded four-layer fabrication stack, quantitative DRC/netclasses and instantiate/audit In1 0VA plane.
9. Conduct block-by-block independent design assurance, with explicit one-off recoverability classifications and documented dissent.
10. Consider routing release only after every relevant design-driving HOLD is resolved and a controlled permission transition is authorised.

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

- AE-076F preliminary RUN10, full RUN08-RUN14 and MCAD carrier/support trade; AE-076E-B promotion is complete;
- exact SLW/TSW mated mechanical envelope and RUN10 interface parasitics/matching;
- exact component-specific capacitor body/mechanical fit and full MCAD collision assessment after successful H901/C30060/C35060 solid STEP export;
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
- rail-support-vs-six-upper-cover-support comparison, control-plane/full-chassis MCAD and mounting selection;
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
- AE-076D governed baseline commit: `4975fba11a12f25744e35ea61e11578c66f3d50f`; promotion validated with 754 tests.
- AE-076E-A governed baseline: `258751f56f536cc28e836c2d013dbde46aaf4cb6`; promotion verified with 761 tests.
- AE-076E-B source-phase focused validation: PASS — 64 tests; current-decision audit and generated-SCH101 discriminator PASS.
- AE-076E-B native board SHA-256 `a5b519a21a2bbe2c9f3ad751134d43292a5b32184487100512ab045b6258861c`; H901 model `40cd349dcd35a3aa04844d09e13f92a40d90f1a664e1ad8baec2cd010259e87a`; capacitor model `35659ae3b9a50ddeb0aa5add4edfaea1770d99f3a8c2db7320eb8fb13be8ee1b`; actual-board STEP `84fae4cfe2fa5edc3436a36792f3da41c8f71d29e9cd711f469631b37200fe61`; KiCad CLI rc0 and no missing models, DNP excluded.
- AE-076E-B intermediate regression history: 764 passed/1 failed at superseded pre-F8 board assertion; subsequent 766 passed/1 failed at obsolete DR-038 wording. Both test contracts were reconciled to the live implementation.
- Full AE-076E-B governance-candidate regression on 2026-10-08: 767 passed in 45.34 seconds; decision/configuration authority audit PASS. Promoted Git `develop` baseline `2a912eac1c63313443f99dc87f86e07232f1a40b` was subsequently verified by read-only AE-076F startup on 2026-10-09: 767 passed in 47.46 seconds, authority audit PASS, hashes matched, local HEAD=origin/develop, clean index/tree. No routing/layout/BOM/manufacturing authorisation conferred.
- Reproducibility: the governed native PCB remains CRLF and SHA-256-pinned; .gitattributes uses a single-file -text -eol whitespace=cr-at-eol exception so staged/checked-out bytes remain identical without weakening Git whitespace verification.

## 9. Continuity rule

Do not begin a major new Shellac phase from conversation memory alone.

At the start of a new chat:
1. read this file in full;
2. read `PROJECT_GUIDANCE.md`;
3. verify Git branch/HEAD/origin/working-tree state;
4. inspect the current authority files referenced by this summary for the task at hand;
5. update this file again before the next major phase transition.

This file is an index, not a substitute for controlled design records.

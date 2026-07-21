# SR-021 — SCH107 Human-Reviewable Conversion — Rev A

## Purpose

Convert the validated SCH107 rumble-filter sheet from labelled pin stubs into
conventional schematic capture suitable for engineering review. No analogue
transfer function, component value, gain, bypass or power decision is changed.

## Frozen design retained

Each channel retains two cascaded unity-gain Sallen-Key high-pass sections:

| Section | R1 | R2 | C1 | C2 |
|---|---:|---:|---:|---:|
| A | 20.8 kΩ | 24.3 kΩ | 470 nF | 470 nF |
| B | 8.66 kΩ | 59.0 kΩ | 470 nF | 470 nF |

The two sections realise the accepted fourth-order Butterworth response with a
nominal 15 Hz cutoff. One dual OPA1656 package serves each channel. The filter
remains driven in both switch positions, and a stereo 2P2T break-before-make
selector chooses direct or filtered output.

## Presentation changes

Each channel now reads conventionally from left to right:

```text
POST_EQ -> input TP -> HP section A -> stage TP -> HP section B
        -> stage TP -> 100 Ω isolation -> bypass selector -> output TP -> FILTERED
```

The generated capture includes:

- continuous conductors through both capacitor pairs and op-amp stages;
- visible feedback branches from each C1/C2 junction to its stage output;
- visible shunt resistors from each op-amp input node to 0VA;
- in-line input, inter-stage and filtered-output test points;
- separate visible direct and filtered bypass routes;
- local ±18 V and 0VA connections for every active section;
- grouped 100 nF and 10 µF decoupling for each dual package;
- no internal stage-net labels substituting for physical relationships;
- deterministic junction dots at every true three-way branch; and
- orthogonal, zero-length-free signal wiring.

## Verification

- 147 Python tests pass.
- Engineering Model Rev A validates: 8 blocks and 27 signals.
- The model-driven build generates all eight block sheets and the root
  hierarchical schematic with no pending builders.
- Consecutive generated SCH107 files are deterministic.
- Native KiCad hierarchical ERC and final PDF visual inspection remain the
  Windows acceptance activities because `kicad-cli` is unavailable in the
  patch-generation runtime.

## Gate status

```text
Gate 2A machine readiness: PASS on the accepted SR-020 baseline
Human-reviewable blocks: 4/8
Gate 2B human-review readiness: FAIL
```

SCH101, SCH104, SCH106 and SCH107 are now classified as human-reviewable.
SCH103, SCH105, SCH108 and SCH109 remain open.

## Next increment

Convert SCH105 next. The mode matrix is electrically smaller than SCH108 and
SCH103, but it exercises conventional passive summing, a multi-pole selector,
unity buffers and mono/stereo signal-flow presentation.

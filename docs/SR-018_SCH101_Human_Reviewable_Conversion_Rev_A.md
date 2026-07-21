# SR-018 - SCH101 Human-Reviewable Conversion Rev A

## Purpose

SR-018 converts the balanced-input sheet identified during the first KiCad
visual review from a label-stub representation into a conventional schematic
capture suitable for engineering review.

The frozen AE-010 electrical design is unchanged:

- balanced left and right cartridge inputs;
- 100 ohm RF series isolation;
- 1 nF common-mode and 220 pF differential RF filtering;
- four matched OPA1656 gain legs;
- 14 dB, 18 dB and 22 dB total gain selections;
- eight-way internal DIP gain selector;
- 10 k / 34.8 k precision differential converters; and
- nominal +/-18 V supplies.

## Presentation changes

Each channel now reads from left to right:

```text
XLR input -> RF network -> two OPA1656 gain legs -> differential converter -> PRE_EQ
```

The capture includes:

- continuous visible conductors through the main signal path;
- the complete three-resistor feedback ladder for every gain leg;
- visible gain-to-ground resistors;
- visible differential-converter input, feedback and reference networks;
- a separate central DIP-selector block;
- labels only for hierarchy interfaces, supply/reference nets and the remote
  DIP contacts where eight long wires would impair readability; and
- controlled component references in standalone and hierarchical contexts.

## Verification

- 132 Python tests pass.
- Engineering Model Rev A validates: 8 blocks, 27 signals.
- Native KiCad hierarchical ERC reports zero violations.
- Standalone KiCad PDF export was visually inspected after two layout passes.
- SCH101 and SCH104 are now classified as human-reviewable.

## Gate status

```text
Gate 2A machine readiness: PASS
Human-reviewable blocks: 2/8
Gate 2B human-review readiness: FAIL
```

Gate 2B remains open until the same presentation standard has been applied to
SCH103, SCH105, SCH106, SCH107, SCH108 and SCH109.

## Next increment

Convert SCH106 next.  It is already electrically wired and is a useful proof
for readable power-entry, protection, rail and chassis/0VA-bond presentation
before returning to the more complex replay-EQ and rumble-filter sheets.

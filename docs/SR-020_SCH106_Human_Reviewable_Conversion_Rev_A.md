# SR-020 - SCH106 Human-Reviewable Conversion - Rev A

## Purpose

Convert the audio-box power-entry sheet nominated by SR-018 from labelled
component stubs into conventional schematic capture suitable for engineering
review. The accepted SR-019 electrical design is unchanged.

## Frozen design retained

- five-pin regulated DC inlet with pin 5 reserved and unconnected;
- +18VA_IN and -18VA_IN 0-ohm entry links;
- post-link +18 V and -18 V rail-source declarations;
- 470 uF, 1 uF and 100 nF local decoupling on each rail;
- 22 k rail bleeders;
- test points for both rails, 0VA and chassis;
- initial R909 0-ohm direct 0VA-to-chassis bond;
- C909 100 nF high-frequency bond; and
- opposed D901/D902 clamp options, both DNP.

## Presentation changes

The sheet now uses four continuous horizontal conductors for +18 V, 0VA,
-18 V and chassis. The physical inlet fans into those domains at the left.
Rail links and test points appear in-line, decoupling and bleeders are drawn
vertically between the appropriate rails, and the configurable bond network is
shown as four parallel branches between 0VA and chassis.

Intentional branch endpoints allow the accepted SR-019 writer to emit
deterministic conventional junction dots. Local labels identify the inlet nets
and the true hierarchy interfaces; they no longer substitute for visible
functional relationships.

## Verification

- 141 Python tests pass, including three new SCH106 presentation regressions.
- Engineering Model Rev A validates: 8 blocks and 27 signals.
- The model-driven build generates all 8 blocks and no pending blocks.
- Native KiCad 9 hierarchical ERC reports zero violations.
- Consecutive generated SCH106 files are byte-identical.
- Standalone SCH106 PDF export was rendered and visually inspected: rail flow,
  protection/bond branches, notes and title block are complete and unclipped.

## Gate status

```text
Gate 2A machine readiness: PASS
Human-reviewable blocks: 3/8
Gate 2B human-review readiness: FAIL
```

SCH101, SCH104 and SCH106 are now classified as human-reviewable. Gate 2B
remains open for SCH103, SCH105, SCH107, SCH108 and SCH109.

## Next increment

Convert SCH107 next. Its two-channel rumble-filter and bypass paths provide a
bounded signal-flow conversion before the denser SCH103 replay-EQ sheet.

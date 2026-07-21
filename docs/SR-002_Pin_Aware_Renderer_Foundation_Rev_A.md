# Project Shellac — SR-002 Pin-Aware Renderer Foundation

**Revision:** A  
**Status:** SCH104 proof complete; project Gate 2 remains open  
**Date:** 14 July 2026

## 1. Purpose

SR-002 introduces the minimum named-pin connectivity contract required for
builders to emit real electrical nets without hard-coding KiCad symbol-pin
coordinates.

SCH104 is the first proof block because its topology is simple enough to test
the renderer independently of complex analogue circuitry.

## 2. Implemented foundation

- Semantic pin contracts map names such as `IN`, `OUT`, `+V`, `-V`, and `0VA`
  to symbol pin numbers and local coordinates.
- Pin coordinates are transformed correctly for component rotation.
- `Sheet.connect_pins()` joins two named component pins.
- `Sheet.connect_pin_to_net()` creates a labelled electrical stub from a named
  component pin.
- The writer now embeds deterministic definitions for:
  - `ProjectShellac:OpAmp_Buffer_Block`
  - `ProjectShellac:TestPoint`
- The readiness audit reads the writer's actual embedded-symbol inventory
  rather than maintaining a separate duplicate list.

## 3. SCH104 proof result

SCH104 now emits:

- left and right signal-input nets;
- physical 100-ohm series output resistors;
- left and right output nets;
- input and output test-point nets;
- +18 V, -18 V and 0VA op-amp connections;
- four connected local decoupling capacitors.

The sheet no longer relies solely on labels and annotations to imply
connectivity.

## 4. Gate status

SCH104 and the already-wired SCH106 should now report:

```text
CAD ready: YES
```

The project Gate 2 remains open because:

- the other functional sheets are not yet converted;
- no root hierarchical schematic links the eight sheets;
- final KiCad symbol resolution and ERC have not yet been run on the user's
  installation.

## 5. Next sequence

Convert the remaining sheets in ascending implementation risk:

1. SCH105 mode matrix;
2. SCH107 rumble filter;
3. SCH108 balanced output;
4. SCH109 controls;
5. SCH103 replay equalisation;
6. finish any residual SCH101/SCH106 symbol gaps;
7. generate root hierarchy;
8. open in KiCad 9 and run ERC.

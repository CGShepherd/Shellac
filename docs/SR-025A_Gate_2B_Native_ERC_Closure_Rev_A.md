# SR-025A — Gate 2B Native ERC Closure

**Trigger:** SR-025 native ERC: 2 errors, 6 warnings.

## SCH103

The treble-selector COMMON pin was connected by a short wire whose endpoint lay
on a longer main-path wire. KiCad did not infer that overlap as a junction. The
main path is now split explicitly at COMMON: resistor-to-COMMON and
COMMON-to-recovery-input.

## Root hierarchy

Labels placed directly on hierarchical sheet pins produced
`label_multiple_wires` warnings. Each interface now has a short outward wire
stub with the label at its far endpoint, giving the label exactly one wire.

# AE-058 — LTspice 26 Correlation Compatibility and RUN00 Correction — Rev A2

## Status
Pre-SPICE design-assurance evidence. Not manufacturing baseline authority.

## Rev A2 changes
Target-machine evidence showed one sequential matrix case return code 0 while its native log reported that the sibling `.log` file had been treated as the input deck. The controlled invocation contract is therefore revised to the current Analog Devices documented batch form `-b -run <netlist>`.

The correlation runner now deletes any stale sibling native log before each run, checks the native log `Circuit:` identity against the requested netlist, retries once with a bounded delay only when invocation/log identity is invalid or LTspice reports `Could not open input deck for reading`, and fails closed if the second attempt is still invalid.

The regression assertion is reconciled to the intentional four deterministic matrix cases that replaced the unsupported `.alter` topology. No analogue authority, tolerances, or intended matrix arithmetic are changed.

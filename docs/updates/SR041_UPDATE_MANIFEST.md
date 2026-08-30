# SR-041 update manifest

Base: `develop` commit `56c74250507a2f4d4b4dc04641096c7883512740`.

Adds a routing-release contract on top of SR-040:
- accepts deterministic manual-authority clusters as routing baseline;
- explicitly permits controlled local XY refinement during manual routing;
- audits all component envelopes against frozen mounting-hole keep-outs;
- freezes critical-net routing authority and routing order;
- emits accepted placement and mounting-hole CSV reports.

Run `APPLY_SR041.bat`.

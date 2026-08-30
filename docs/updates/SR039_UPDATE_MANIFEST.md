# SR-039 update manifest

Base branch: `develop`
Base commit expected: `70296c1efb9ac469ab1865f0d11b4a41ddb05563`

This package:
- reconciles stale DR-038/DR-039/DR-040 decision documentation;
- records the validated 374/374 + native ERC 0/0 electrical baseline;
- adds a formal schematic-to-layout release-gate model;
- adds LT5400 / PRE_EQ / DR-039 layout-critical constraints;
- preserves the mechanical-datum and full-BOM gates;
- adds an automated Windows validation entry point.

Apply at repo root with `APPLY_SR039.bat`, then run `VALIDATE_SHELLAC.bat`.

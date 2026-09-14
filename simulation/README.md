# Project Shellac — Controlled LTspice/Python Toolchain

This directory implements the AE-053 simulation architecture under the governing
qualification/acceptance/execution authorities AE-048, AE-049 and AE-050.

Stage 1 scope is deliberately narrow:

- controlled tool/version discovery;
- deterministic run configuration;
- model/include provenance and SHA-256 manifests;
- reproducible LTspice batch invocation;
- structured measurement extraction;
- central acceptance mapping;
- RUN00 model-sanity harness;
- anomaly recording;
- deterministic rerun comparison.

This stage does **not** implement DR-038 or DR-039 circuit changes and does not
constitute manufacturing authority.

## First use

From the repository root:

```cmd
python -m simulation.scripts.shellac_spice doctor
python -m simulation.scripts.shellac_spice manifest
python -m simulation.scripts.shellac_spice prepare RUN00
```

If LTspice is installed and discovered:

```cmd
python -m simulation.scripts.shellac_spice run RUN00
python -m simulation.scripts.shellac_spice verify RUN00
```

If LTspice is not auto-discovered, set `LTSPICE_EXE` to the full executable path.

Generated artefacts live under `simulation/generated`, `simulation/results`,
`simulation/logs`, and `simulation/plots`. They are reproducible artefacts rather
than hand-edited design authority.

RUN00 is a toolchain/invocation sanity circuit, not the final integrated Shellac model.
Its purpose is to prove the controlled execution path before real block models are added.

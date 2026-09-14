# Project Shellac

Shellac is a controlled 78 rpm replay preamplifier design. `develop` is the working engineering authority; a tagged `main` release becomes production authority only after qualification and reproducibility gates close.

## Current authority

Read these first:

1. `config/decisions/current_decision_index.yaml`
2. `config/decisions/document_authority.yaml`
3. `docs/knowledge/DESIGN_PACK_INDEX.md`
4. current `generator/`, BOM and tests
5. current pre-SPICE assurance records in `docs/design_pack/`

Historical records are provenance and do not override later current authority.

## Live implementation versus selected-next architecture

- DR-037 complete RIAA: implemented.
- DR-038/SCH101: LT5400 4x converter is live; AE-042 fail-safe 14/18/22 dB service-shunt gain architecture remains pending qualification and controlled migration.
- DR-039/SCH107: the common post-EQ DC block is live; AE-052 branch-local DC blocking is the selected preferred SPICE candidate and is not yet implemented.
- AE-041 A1 controls: four independent NKK NR01-family EQ controls, C&K A30403RNCB 3P4T matrix, C&K 7201SYCBE rumble and mute toggles.
- SW905 mute: mechanical DPDT signal/0VA selection immediately before the THAT1646 drivers. No relay/timer/comparator architecture.

Do not change live circuitry merely to make it resemble a selected-next record. Migration requires a controlled qualification and implementation step.

## Power and grounding

Shellac nominal regulated rails are +/-18 V. The selected direct 0VA-to-chassis population is R909 = 0 Ohm fitted, with C909, D901 and D902 DNP. Shellac and Phoenix are independent designs.

## Simulation

AE-053 defines the LTspice/Python simulation architecture. AE-054 through AE-058 establish implemented toolchain and numerical-correlation evidence. The integrated full-system campaign remains governed by AE-048, AE-049 and AE-050. Analytical Python is an independent live-state regression/correlation aid, not final integrated analogue authority.

## Basic validation

    python -m pytest -q
    python tools/audit_current_decision_index.py
    git diff --check

This repository is not yet a manufacturing baseline.

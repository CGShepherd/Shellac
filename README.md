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
- DR-038/SCH101: AE-071A migrates the fail-safe 14/18/22 dB removable-shunt architecture and BASE/+47/+100 pF loading; AE-075B selects LT5400BIMS8E-7#PBF, bonds EP9 to quiet 0VA and selects compatible Samtec TSW/MNT service hardware. RUN10 complete-stage tolerance/CMRR, physical shunt pairing/orientation, short-route parasitics and bench qualification remain open.
- DR-039/SCH107: AE-074 migrates the AE-067 branch-local topology into the live generator: the retained 1 uF / 330 kOhm network exists only in each DIRECT/BYPASS branch, while the existing SCH107 high-pass branch provides intrinsic DC blocking. Native-PCB F8/net reconciliation is closed by AE-074; RUN09, RUN10, RUN12 and bench correlation remain open.
- AE-041 A1 + AE-075C controls: Bass L/R use NKK NR01105ANG13-2C and Treble L/R use NR01105ANG13-2A; channel matrix is C&K A30403RNCB and Rumble/Mute use C&K 7201SYCBE. Exact control hardware is frozen; B03 remains open for the control-plane Z/top-cover stack, PCB ownership, exact footprints/pin maps/courtyards and XY keep-outs.
- SW905 mute: mechanical DPDT signal/0VA selection immediately before the THAT1646 drivers. No relay/timer/comparator architecture.

Do not change live circuitry merely to make it resemble a selected-next record. Migration requires a controlled qualification and implementation step.

## Power and grounding

Shellac nominal regulated rails remain +/-18 V authority. AE-072 establishes the physically reconstructed AIYIMA P1-V PSU model/RUN00 baseline and AE-073 closes the long-settle discriminator, but powered set-point, dropout, ripple, startup and thermal qualification remain open; no rail-authority change is made by those records. The selected direct 0VA-to-chassis population is R909 = 0 Ohm fitted, with C909, D901 and D902 DNP. Shellac and Phoenix are independent designs.

## Simulation

AE-053 defines the LTspice/Python simulation architecture. AE-054 through AE-058 establish implemented toolchain and numerical-correlation evidence. The integrated full-system campaign remains governed by AE-048, AE-049 and AE-050. Analytical Python is an independent live-state regression/correlation aid, not final integrated analogue authority.

## Basic validation

    python -m pytest -q
    python tools/audit_current_decision_index.py
    git diff --check

This repository is not yet a manufacturing baseline.

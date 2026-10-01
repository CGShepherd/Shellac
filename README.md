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
- SCH108/output interface: AE-075G implements exact Molex 5055780221 two-circuit PCB headers H801/H802 for the short rear-panel balanced-output looms, validates HOT/COLD native pad mapping with no 0VA conductor, corrects THAT1646 source semantics to 25 Ohm per leg / 50 Ohm differential, and passes the application-specific PRE90 2 kOhm load discriminator. H801/H802 XY remains provisional pending manual placement reconciliation; RUN06 load/cable stability and dynamic-THD bench gates remain open.
- AE-041 A1 + AE-075C hardware + AE-076B controls: exact NKK/C&K hardware remains frozen. AE-076B supersedes the AE-075D/E/F four-local-control-board/carrier-era ownership architecture with one main audio PCB carrying all seven controls directly; the upper cover, main PCB and controls form one removable service module. Six PCB-to-upper-cover supports are selected in principle, but exact support XY/Z, the C&K fit at the NKK-constrained control plane, control XY, footprints/courtyards, panel apertures and RUN10 parasitic acceptance remain B03-open. SR-040/AE-071B MH1-MH4 native geometry is retained only as interim physical CAD pending the AE-076B2 MCAD/digital-mock-up migration; no control inter-board harnesses are selected.
- SW905 mute: mechanical DPDT signal/0VA selection immediately before the THAT1646 drivers. No relay/timer/comparator architecture.

Do not change live circuitry merely to make it resemble a selected-next record. Migration requires a controlled qualification and implementation step.

## Power and grounding

AE-076A establishes +17.0 V / 0VA / -17.0 V as current Shellac regulated-rail authority and migrates the live generator, current simulation contract, commissioning expectations and native PCB rail identities together. Historical +/-18 V assurance evidence remains immutable provenance. AE-073's target-17 PSU discriminator remains supporting model evidence only: powered set-point, dropout, ripple, startup and thermal qualification remain open under RUN13/RUN14 and bench work. The selected direct 0VA-to-chassis population remains R909 = 0 Ohm fitted, with C909, D901 and D902 DNP. Shellac and Phoenix are independent designs.

## Simulation

AE-053 defines the LTspice/Python simulation architecture. AE-054 through AE-058 establish implemented toolchain and numerical-correlation evidence. The integrated full-system campaign remains governed by AE-048 and AE-050 with AE-049 retained as the historical numerical-acceptance basis; AE-076A narrowly supersedes the current nominal-RUN00 rail criterion at +17 V / 0VA / -17 V and adds targeted rail/headroom requalification. Analytical Python is an independent live-state regression/correlation aid, not final integrated analogue authority.

## Basic validation

    python -m pytest -q
    python tools/audit_current_decision_index.py
    git diff --check

This repository is not yet a manufacturing baseline.

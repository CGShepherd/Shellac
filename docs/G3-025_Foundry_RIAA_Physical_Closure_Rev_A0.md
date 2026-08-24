# G3-025 — Foundry, RIAA Architecture and Physical-Control Closure

**Revision:** A0
**Status:** candidate
**Base:** G3-024 / `57716653d9b4c11d1c785863cb2c7ee03953d48a`

## Objective

Institutionalise Foundry in Git, reconcile the optional 3180 us RIAA requirement
against controlled SCH103 mathematics, capture selected-control mechanical evidence,
remove stale assumptions, and sharpen the manufacturing release gate.

## RIAA finding

The existing active branch is:

`H(s) = 1 + [Rf || (Rs + 1/sC)] / Rg`

Its pole and zero both scale as `1/C`. Switching/bypassing that single capacitor
cannot remove only the 3180 us pole while preserving the 318 us zero.

Required architecture:

`H_RIAA(s) = H_CORE(s) * H_3180(s)`

`H_CORE(s) = (1 + s*318 us) / (1 + s*75 us)`

`H_3180(s) = 1 / (1 + s*3180 us)`

The internal switch acts only on `H_3180`. BYPASS is straight-through around that
dedicated section in both channels. The 318 us and 75 us terms remain invariant.

G3-025 freezes this architecture contract, not the exact RC/gain realisation or
internal switch MPN.

## Physical-control evidence

Controlled catalogue evidence is recorded for:
- Grayhill 71BDF30-01-2-AJN;
- Grayhill 71BDF30-02-2-AJN;
- C&K 7201SYCBE;
- A104700BLACK LED bezel.

These facts are not yet manufacturing footprints.

## Foundry

`foundry/` and `config/foundry/` define authority hierarchy, evidence levels,
decision states, autonomous-decision rules, contradiction handling and the
manufacturing-release gate.

## Stale-assumption cleanup

G3-025 supersedes generic light-pipe/no-flying-indicator assumptions. Selected rail
indicators are panel-mounted in black brass bezels on short flying leads. External
switches remain PCB-mounted.

## Not released

- exact 3180 us RC/gain implementation;
- exact internal RIAA switch MPN;
- final custom switch footprints;
- top-cover drilling coordinates;
- PCB/manufacturing release.

## Acceptance

- Foundry baseline exists in Git and is machine-readable;
- tests prove RIAA factorisation and single-RC coupling;
- stereo internal bypass requirement is explicit;
- control mechanical evidence is explicitly not manufacturing-released;
- stale LED/light-pipe assumptions are removed;
- full repository regression remains green.

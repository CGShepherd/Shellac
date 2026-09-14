# AE-064 — Cartridge Behavioural Model Qualification and Integrated Source-Gate Closure — Rev A0

**Project:** Shellac  
**Status:** PRE-SPICE MODEL-SOURCE GATE CLOSED / SHELLAC_TOP IMPLEMENTATION NOT YET STARTED  
**Baseline:** `develop` at `2d8557b1d35e711a4311d2caa6f85dfba912dc14`

## 1. Purpose

AE-064 closes the remaining controlled model-source obligations that prevented the
first genuine integrated `SHELLAC_TOP` implementation from starting.

AE-064 does **not** implement `SHELLAC_TOP`, execute integrated RUN00, migrate
AE-042 or AE-052 into the product generator, or claim full-system simulation
qualification.

## 2. Controlled cartridge source equivalents

Three project-owned behavioural source equivalents are established:

- Grado Prestige 78C — primary 78 rpm cartridge;
- Audio-Technica AT-VM95SP — secondary/compatibility 78 rpm cartridge;
- Grado Gold / 8MZ — non-gating LP compatibility case.

The model interface is `P N DRIVE`.

`P` and `N` are the floating cartridge terminals. `DRIVE` represents the ideal
generated cartridge EMF referenced internally to `N`. The generated EMF drives
the controlled series source resistance and inductance, producing a floating
two-terminal Thevenin source at `P/N`.

Cable capacitance, optional board capacitance and the balanced SCH101 loading
remain outside the cartridge subcircuit so they can be swept independently by
the integrated execution package.

## 3. Controlled electrical values

### Grado Prestige 78C

- 475 ohm source resistance;
- 45 mH source inductance;
- 47 kohm recommended load;
- 5 mV nominal output at the controlled 1 kHz / 5 cm/s reference convention.

Parameter authority remains AE-061, using project identity plus corroborated
secondary electrical evidence.

### Audio-Technica AT-VM95SP

- 485 ohm source resistance;
- 550 mH source inductance;
- 47 kohm recommended load;
- 100–200 pF recommended load capacitance;
- 2.7 mV nominal output at 1 kHz / 5 cm/s.

Parameter authority remains AE-061 and its manufacturer-primary source evidence.

### Grado Gold / 8MZ

- 660 ohm source resistance;
- 50 mH source inductance;
- 47 kohm project nominal load.

This compatibility model is controlled from AE-037 and is not a gating source
for the first integrated RUN00.

## 4. Qualification

`simulation/scripts/ae064_cartridge_smoke.py` exercises each behavioural model in
LTspice against a 47.4 kohm differential load and compares the simulated 1 kHz
and 20 kHz terminal magnitudes against the analytical R-L Thevenin expectation.

Passing this gate establishes:

- LTspice parse/execution viability;
- correct project subcircuit interface;
- correct encoded resistance and inductance semantics;
- controlled parameter provenance;
- stable use as a behavioural electrical source model.

It does not establish intrinsic acoustic frequency response, stylus/mechanical
behaviour, magnetic nonlinearity, channel separation, body shielding, or
cartridge body/return isolation.

## 5. R-021 remains open

The Grado 78C body/return/isolation topology remains a bench-verification
obligation. AE-064 deliberately does not close R-021.

The controlled behavioural model is therefore an explicitly limited electrical
substitute of the kind permitted by AE-060: sufficient for source/loading
analysis, but not authority for unmodelled mechanical or body/isolation claims.

## 6. Integrated source-gate reconciliation

AE-062 qualified OPA1656, OPA1612, LT5400-7 and THAT1646.
AE-063 qualified the Vishay S1G reference model and reconciled the live SCH108
clamp identity.

With the two required cartridge source equivalents qualified by AE-064, all
seven `required_model_sources` in `simulation/config/integrated_baseline.yaml`
are now `RESOLVED`.

`simulation/scripts/integrated_preflight.py` is strengthened so static
`RESOLVED` labels are insufficient by themselves: each required source must map
to an allowed qualification state in `model_qualification.yaml`.

## 7. RUN00 boundary

After AE-064 passes:

- the controlled model-source gate is closed;
- `SHELLAC_TOP` implementation may begin;
- the historical divider RUN00 remains toolchain-only evidence;
- the real integrated RUN00 has **not** executed;
- no `SIMULATED` or manufacturing-baseline claim is created.

## 8. Explicit non-actions

AE-064 does not:

- modify product-generator circuitry;
- implement the AE-042 SCH101 gain migration;
- implement the AE-052 DR-039/SCH107 migration;
- change nominal Shellac rails from +/-18 V;
- alter EQ, matrix or mechanical mute architecture;
- close R-020 phantom-energy qualification;
- close R-021 cartridge body/return bench verification;
- claim `SHELLAC_TOP` exists;
- execute integrated RUN00;
- promote `develop` to `main`.

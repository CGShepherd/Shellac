# AE-036 — Repository-Wide Production Integrity Audit

**Revision:** A0  
**Audit baseline:** `develop` @ `ba63ffb11866115595543e3d415f7caee022dae4`  
**Scope:** electrical architecture, physical CAD, PCB ownership, mechanical integration, BOM/procurement, decision authority, CI/reproducibility, maintenance/release documentation  
**Disposition:** ROUTING HOLD — P0/P1 issues must be closed before further irreversible production routing

## Executive conclusion

The end-to-end signal-chain architecture remains broadly coherent. The audit did
not find a new error requiring the already-closed RIAA, gain, rumble-filter,
mode-matrix or balanced-output architectures to be reopened.

However, the audit found several integration defects that the 452-test suite
cannot detect because the tests largely validate internal consistency within each
model.

Three findings change the immediate production plan:

1. **P0 — normal clean build can delete the authoritative native PCB.**
2. **P0 — SCH101 cartridge interface lacks a defined resistive load/DC bias
   return and its RF capacitance is not included in the end-to-end response model.**
3. **P0/P1 — op-amp functional blocks and dual-package physical semantics are not
   reconciled.**

Further routing should pause until these are closed.

## F01 — Native PCB can be erased by the normal build

Current chain:
`build_shellac.bat` → `scripts/build_shellac_from_model.py` →
`generator.dispatch.build_project_from_model(... clean=True)` →
`generator.writers.kicad9.clean_output()`.

`clean_output()` recursively removes the output directory, while the editor-owned
native PCB lives at `out/kicad/ProjectShellac.kicad_pcb`.

This is a production-blocking ownership defect. `tests/test_clean_output.py`
currently checks retry/error handling only and does not prove native PCB
preservation.

Immediate action: preserve native PCB/design-rule artifacts during generator
cleanup. Long-term action: move authoritative native PCB source out of disposable
`out/`.

## F02 — SCH101 cartridge load, DC bias and RF response are incomplete

The current SCH101 implementation contains:
- 100 Ω series in each cartridge leg;
- 1 nF from each leg to CHASSIS;
- 220 pF directly across the differential input;
- OPA1656 non-inverting input stages.

No explicit cartridge-loading resistor or input common-mode bias-return resistor
was found in the controlled source.

With CHASSIS bonded to 0VA, the two 1 nF capacitors form approximately 500 pF
differential capacitance through the common reference, added to the 220 pF
differential capacitor: approximately **720 pF board differential capacitance**
before cable capacitance.

The current production response model starts downstream of this network and does
not include cartridge R/L, cable C, input series resistance, input RF C or the
missing load/bias network.

As a screening calculation using Grado Gold4's published 660 Ω / 50 mH source
parameters, the current 200 Ω total series resistance and ~720 pF board
capacitance produce a several-dB upper-audio resonance. This is not an acceptance
model, but is large enough that SCH101 must be re-closed before routing.

Required:
1. model Grado 78C;
2. model Grado Gold/8MZ;
3. include cable capacitance;
4. define differential loading;
5. define common-mode DC bias return;
6. optimize common-mode/differential RF capacitance;
7. propagate the complete interface into response/noise acceptance.

Do not simply insert 47 kΩ without analysing the balanced topology.

## F03 — Dual op-amp package semantics are not physically closed

The component abstraction gives each functional op-amp block a complete SOIC-8
footprint, while several circuit-builder comments say two amplifier functions are
intended to occupy one dual OPA1612/OPA1656 package.

This can produce excess packages, incorrect A/B-unit mapping, unused halves,
uncontrolled unused halves, incorrect BOM/current/placement and a schematic that
is electrically coherent but not physically faithful.

Required before routing:
- enumerate every OPA1656/OPA1612 amplifier function;
- pair intended functions into real dual packages;
- use correct multi-unit symbol/package semantics;
- explicitly stabilize any genuinely unused half;
- re-run current, BOM, noise and placement calculations.

## F04 — Control hardware authority is contradictory

Grayhill 71BDF30 is rejected by the current production-readiness decision, but is
still selected in live BOM/model/mechanical authority and is regression-enforced
by old tests. The running cost ledger already uses Lorlin PT.

Before the exact Lorlin MPN exists, live status should become something equivalent
to `LORLIN_PT_PLATFORM_SELECTED_MPN_OPEN`; Grayhill should remain only rejected
or historical evidence. Top-panel machining remains blocked pending AE-027/028.

## F05 — PCB-mounted top controls are not yet physical PCB objects

The mechanical architecture requires PCB-mounted top controls, while the current
control builder treats controls as panel/virtual and excludes them from the PCB
footprint contract. Final rotary/toggle footprints must be instantiated after the
Lorlin geometry gate.

## F06 — Supply rail margin needs a formal decision

Committed Shellac authority is ±18 V. OPA1656, OPA1612 and THAT1646 all have
recommended operating maxima at 36 V total / ±18 V. Nominal ±18 V therefore
uses the top of the recommended operating range.

This is not automatically incorrect, but regulator tolerance and operating margin
must be analysed before production. Compare ±17 V and ±18 V against required
headroom, output swing, LED current and PSU dissipation before changing authority.

## F07 — Current decision baseline/provenance is stale

`current_decision_index.yaml`, its tests, README and design-pack index still
anchor to an older DR-038/039-era baseline. Historical implementation tags should
remain evidence, but the current integrated working baseline needs separate,
current provenance.

## F08 — Native pipeline contains superseded mechanical state

`kicad_native_pipeline.py` and its tests still state manufacturing holes are
unfrozen, while SR-040/SR-043 subsequently froze and applied them.

## F09 — Native PCB audits are structurally weak

Several audits use literal text presence/counting. AE-035 demonstrated the
problem: the zone UUID was present and KiCad parsed the modified PCB, while a
literal `(zone ` count reported zero.

Move toward whitespace-tolerant S-expression parsing plus independent
`kicad-cli` validation.

## F10 — Procurement/BOM remains production-incomplete

Open items include exact Lorlin MPNs, precision passive manufacturer MPNs,
op-amp package count, output sense capacitors, connectors/wiring, PCB fab, PSU
electrical parts and hardware.

## F11 — CI does not exercise production CAD gates

Current CI runs Python compile/pytest, but does not run the real model build,
native-PCB preservation check, KiCad ERC/DRC or native-board audits.

## F12 — Final connector/interface arrangement needs confirmation

Committed mechanics currently place audio inputs at the front, outputs at the
rear and DC rear-centre. Confirm this is still the intended final user interface
before machining release.

## F13 — Maintenance/release pack awaits physical evidence

Commissioning structure is good, but final test-point IDs, reference readings,
fault isolation, measured performance, thermal evidence and fabrication hashes
remain open.

## Electrical areas reviewed with no new topology reopening required

No new architectural defect was identified in:
- 14/18/22 dB gain partition;
- complete RIAA topology;
- historical replay-curve architecture;
- fourth-order 15 Hz rumble filter;
- stereo / dual-L / dual-R / mono-average matrix;
- post-EQ DC block;
- unity final-gain stage;
- THAT1646 balanced-output architecture;
- nominal end-to-end headroom/noise/CMRR models.

These remain subject to prototype verification and to the newly required complete
cartridge-interface model.

## Revised critical path

### Stop before further native routing
1. protect native PCB from clean-build deletion;
2. close SCH101 cartridge load / bias / RF interface;
3. close op-amp package/unit semantics.

### Then
4. reconcile control authority and Lorlin physical footprints;
5. decide allowable audio supply-rail range;
6. regenerate/update native PCB from corrected schematic/packages;
7. rebuild In1/In2 copper with stronger structural audits;
8. route critical analogue nets;
9. complete BOM/procurement and supplier quotes;
10. fabricate and commission;
11. freeze measured acceptance;
12. complete maintenance/release pack;
13. clean-clone and repository cleanup;
14. production tag;
15. extract Foundry/Generator.

## Overall assessment

Shellac remains technically viable and substantially mature, but internal
regression completeness is ahead of physical-design completeness. The correct
response is not to discard the signal-chain work; it is to close the three
integration gaps above before the PCB layout becomes expensive to change.

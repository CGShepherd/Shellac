# AE-037 — SCH101 Cartridge Interface Closure

**Revision:** A0  
**Closes:** AE036-F02  
**Status:** ELECTRICAL CLOSURE — ROUTING STILL HELD BY AE036-F03

## Supported cartridge basis

Grado 78C:
- 475 Ω DC resistance;
- 45 mH inductance;
- 47 kΩ recommended load;
- 5 mV nominal output.

Grado Gold / 8MZ use case is conservatively modelled with the current Gold-family
electrical values:
- 660 Ω;
- 50 mH;
- 47 kΩ nominal design load within Grado's 10–47 kΩ recommendation.

## Balanced load and bias return

Each signal leg receives 23.7 kΩ to 0VA after the 100 Ω RF series resistor.

The floating cartridge therefore sees approximately:

`23.7 kΩ + 23.7 kΩ = 47.4 kΩ differential`

The same resistors provide explicit DC return paths for both OPA1656
non-inverting inputs. This removes the previous undefined common-mode DC state.

Use 0.1% matched resistors; tighter tolerance may be selected if cost difference
is negligible.

## RF network

Previous default:
- 1 nF each leg to CHASSIS;
- 220 pF differential.

AE-037 default:
- 47 pF C0G/NP0 each leg to CHASSIS;
- 22 pF C0G/NP0 differential footprint retained but DNP by default;
- existing 100 Ω matched series resistors retained.

The fitted common-mode pair contributes approximately 23.5 pF differential
board capacitance.

The optional differential capacitor remains available as a defensive EMI tuning
part for prototype testing without burdening the production default.

## Electrical acceptance model

For cable capacitance from 50 pF through 300 pF, the additional response change
caused by the fitted board RF capacitance is required to remain below 0.20 dB at
20 kHz for both supported cartridge models.

The model is deliberately an interface-loading model, not a claim about the
cartridge's intrinsic acoustic frequency response.

## Consequence

SCH101 cartridge loading, DC bias return and default RF capacitance are now
explicitly defined. AE036-F02 can close after generated schematic/ERC regression
passes.

Further PCB routing remains held until AE036-F03 closes the real dual-op-amp
package/unit semantics.

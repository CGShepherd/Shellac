# PSU RUN00 model qualification

Status: PASS (operator execution 2026-09-21)

Purpose: qualify controlled LTspice execution of the LM317, LM337 and LF353
manufacturer macromodel interfaces before physical P1-V PSU simulation.

Final observed measurements:

- LM317: VOUT_AVG = 5.00552415848 V; VOUT_MIN/MAX identical at reported precision.
- LM337: VOUT_AVG = -5.00489759445 V; VOUT_MIN/MAX identical at reported precision.
- LF353 U1A/U1B gain-2 smoke: HI = 0.199999288989 V both channels;
  LO = 4.21540417139e-06 / 4.21540416911e-06 V.
- PSU-RUN00: PASS.
- Full repository regression after parser reconciliation: 652 passed.

LF353 investigation root cause:
Some exploratory generated decks placed `VP VP 0 15` on the first SPICE line.
That line is the circuit title and was therefore not instantiated, producing a false
negative-rail saturation result near -13.48 V. FIX5 added an explicit title to the
controlled LF353 smoke deck and a fail-closed generated-deck title invariant.
No LF353 pin mapping, vendor model, electrical circuit or acceptance threshold was
changed to obtain PASS.

Parser reconciliation:
LTspice 26 expression measurements (`NAME: EXPR=number`), direct colon measurements,
and controlled legacy scalar measurements (`NAME = number`) are accepted. Known
numeric LTspice settings TNOM and TEMP are excluded from measurement parsing.

Vendor model payloads remain local/uncommitted. This record does not redistribute
vendor model text.

P1-V remains physically reconstructed pending powered validation. RUN00 PASS removes
the model-execution gate; it does not constitute powered validation of the PSU.

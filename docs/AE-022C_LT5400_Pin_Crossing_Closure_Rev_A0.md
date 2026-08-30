# AE-022C — LT5400 Pin-Crossing Closure

Root cause identified from the electrical-audit implementation:

The audit correctly treats every semantic pin lying on a conductor segment as a
connection. LT5400 pins 4/5 share a Y coordinate and pins 1/8 share a Y
coordinate. AE-022B routed from left pins 4 and 1 horizontally through the
symbol body, so those conductors passed through opposite-side pins 5 and 8,
shorting the plus-reference and feedback networks.

AE-022C routes left-side pins outward-left before changing direction. It also:
- corrects the AE-022B audit import;
- replaces direct-edge tests with path-aware connectivity checks;
- adds a regression specifically forbidding a left-pin conductor from passing
  through its opposite LT5400 terminal.

No electrical values or architecture decisions change.

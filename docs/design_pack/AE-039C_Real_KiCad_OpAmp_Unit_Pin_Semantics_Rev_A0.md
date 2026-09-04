# AE-039C — Real KiCad Op-Amp Unit and Pin Semantics

AE-039C is the F03 closure candidate. It maps logical amplifier functions to
real KiCad multi-unit symbols while retaining the validated 10-package /
246-item physical population.

Dual OPA1656/OPA1612 SOIC-8:
OUT A=1, -IN A=2, +IN A=3, V-=4, +IN B=5, -IN B=6, OUT B=7, V+=8.

OPA1655 SOIC-8:
-IN=2, +IN=3, V-=4, OUT=6, V+=7; pads 1,5,8 are NC.

The prior OpAmp_Buffer_Block exposed a synthetic 0VA pin. No such pin exists on
OPA1656. AE-039C removes it and emits explicit OUT-to-IN- follower feedback in
SCH104, SCH105 and SCH107.

F03 closes only after targeted tests, full pytest, build_shellac.bat and KiCad
ERC all pass, with board population remaining 246.

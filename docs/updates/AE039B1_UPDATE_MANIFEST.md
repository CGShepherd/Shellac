# AE-039B1

Apply directly on top of the current failed AE-039B working tree.

Run:

`APPLY_AE039B1.bat`

Expected:
- 10 physical op-amp packages
- board population 246
- no U3002/U3502 placement ownership errors

If green:
`build_shellac.bat`
then:
`python -m pytest`

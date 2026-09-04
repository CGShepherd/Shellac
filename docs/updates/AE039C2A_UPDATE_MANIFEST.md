# AE-039C2A — robust unit-instance regression correction

Supersedes AE-039C2.

C2 failed because its apply script matched a multi-line test block too
literally. C2A changes only the U401 reference-count assertion from 4 to 2 and
verifies that the existing regression still checks:
- no U402 physical reference;
- unit 1 is present;
- unit 2 is present.

Run:

`APPLY_AE039C2A.bat`

If green:

`build_shellac.bat`

then:

`python -m pytest`

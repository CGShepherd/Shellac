# AE-039C2B — canonical SCH104 unit-instance regression

Supersedes AE-039C2 and AE-039C2A.

C2/C2A were too dependent on the exact existing formatting/content of the
test body. C2B replaces the entire
`test_sch104_writer_emits_u401_units_one_and_two` function by name.

Canonical invariant:
- no U402 physical reference;
- exactly two U401 instance references;
- exactly one U401 unit 1 instance;
- exactly one U401 unit 2 instance.

No implementation file is modified.

Run:

`APPLY_AE039C2B.bat`

If green:

`build_shellac.bat`

then:

`python -m pytest`

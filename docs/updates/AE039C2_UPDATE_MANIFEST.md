# AE-039C2 — unit-instance regression correction

Apply on top of the current AE-039C/C1 working tree.

The implementation correctly emits two SCH104 U401 instances: unit 1 and unit 2.
The prior regression incorrectly expected four `(reference "U401")` occurrences.

C2 changes the invariant to:
- exactly two U401 instance references;
- no U402 physical reference;
- one U401 unit 1 instance;
- one U401 unit 2 instance.

Run:

`APPLY_AE039C2.bat`

If green:

`build_shellac.bat`

then:

`python -m pytest`

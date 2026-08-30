# AE-020A dependency repair

Replaces `tests/test_current_decision_index.py` so AE-020 does not introduce
PyYAML as an undeclared project/test dependency.

The authoritative YAML file is unchanged. The regression test now validates
the small controlled subset required by AE-020 using Python standard-library
text/regex operations.

Apply over the uncommitted AE-020 working tree, then run:

`python -m pytest`

Do not install PyYAML merely to satisfy AE-020.

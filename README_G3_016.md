# G3-016 Real-Footprint Audit

Apply this patch over the repository root, then run:

```cmd
python -m pytest
python scripts\report_real_footprint_audit.py
python scripts\build_populated_review_board.py
```

The audit is intentionally **BLOCKED**. This is a controlled engineering result: it prevents aggregate replay-EQ capacitor values and unresolved 10 uF capacitor technology from being mistaken for manufacturable footprint assignments.

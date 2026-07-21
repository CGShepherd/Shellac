# G3-004 — Commissioning and Verification Baseline Rev A0

G3-004 converts Rev A bring-up into ten gated stages from configuration control
through objective characterisation and controlled listening release.

Every stage records prerequisites, configuration, measurements, instruments,
limits, stop conditions and retained evidence.  Calculated expectations are
kept distinct from limits that require Rev A hardware characterisation.

The baseline is intentionally conservative: no stage may be bypassed after a
failure, listening cannot waive an objective defect, and mains/PE verification
is completed before the audio enclosure is connected.

Machine-readable output:

```
python scripts/report_commissioning_baseline.py
out/commissioning/commissioning_baseline.json
```

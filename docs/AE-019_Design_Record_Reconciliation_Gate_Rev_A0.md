# AE-019 — Design Record and Decision Register Reconciliation Gate

**Status:** READ-ONLY AUDIT

This audit runs in parallel with signal-chain revalidation. It inventories controlled decision and assurance records without rewriting history. The eventual design pack will distinguish the current design baseline, decision register, assurance evidence, production/commissioning record, maintenance guide, and historical archive.

Run `python tools/ae019_design_record_reconcile.py`, then `python -m pytest`. Review the generated report before changing any decision status.

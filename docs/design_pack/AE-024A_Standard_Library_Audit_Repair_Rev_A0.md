# AE-024A — Standard-Library Audit Repair

**Revision:** A0  
**Status:** REPAIR

AE-024 incorrectly introduced an undeclared PyYAML dependency.

AE-024A removes that dependency completely. The audit now uses a deliberately
narrow standard-library parser for the two Shellac decision-control YAML files.

The parser is not a general YAML implementation; it understands only the
structures required by:

- `config/decisions/decision_status.yaml`
- `config/decisions/current_decision_index.yaml`

This keeps the read-only audit self-contained and prevents tooling drift.

## Apply

Replace the AE-024 files with this package, then run:

`python tools/ae024_design_record_audit.py`
`python -m pytest`

No package installation is required.

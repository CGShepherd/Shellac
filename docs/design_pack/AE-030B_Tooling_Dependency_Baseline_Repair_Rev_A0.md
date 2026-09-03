# AE-030B — Tooling Dependency Baseline Repair

**Revision:** A0  
**Status:** TOOLCHAIN / REPRODUCIBILITY REPAIR

## Finding

AE-030A introduced a legitimate dependency on PyYAML for the controlled
machine-readable BOM cost ledger, but `requirements.txt` still declared only
pytest.

A fresh virtual environment would therefore fail when running the BOM-cost
audit.

## Resolution

Add:

`PyYAML==6.0.3`

to the root requirements file.

Version 6.0.3 is pinned because it is the version validated on the current
Windows/Python 3.13 Shellac development environment.

## Why keep PyYAML

The cost ledger is configuration data, not an intentionally narrow audit-only
format. Using a real YAML parser is preferable to maintaining another partial
YAML implementation as the BOM/procurement model grows.

## Clean-clone implication

The controlled setup sequence is now expected to include:

`python -m pip install -r requirements.txt`

before build, audit or test execution.

A future production reproducibility gate may pin the remainder of the Python
toolchain more tightly; AE-030B only fixes the newly demonstrated missing
dependency.

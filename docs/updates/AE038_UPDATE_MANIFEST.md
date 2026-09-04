# AE-038 update manifest

Read-only package/unit audit.

Adds:
- docs/design_pack/AE-038_Dual_OpAmp_Package_Unit_Audit_Rev_A0.md
- generator/model/opamp_package_audit.py
- tests/test_opamp_package_audit.py

Run:
`python -m pytest tests/test_opamp_package_audit.py -v`
then:
`python -m pytest`

AE-038 changes no schematic or PCB. The next increment implements real
multi-unit physical-package semantics.

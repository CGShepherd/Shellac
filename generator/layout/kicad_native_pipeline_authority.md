# AE-034 authority correction for kicad_native_pipeline.py

The current `generator/layout/kicad_native_pipeline.py` predates SR-040 and still describes manufacturing holes as unfrozen.

Current authority supersedes that provisional statement:
- SR-040 freezes enclosure/carrier/PCB datum.
- SR-043 applies and audits the four frozen mounting holes.
- AE-033 establishes four-layer native-board configuration.

Do not delete historical evidence merely to make the older provisional object appear current.

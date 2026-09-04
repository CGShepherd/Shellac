# AE-035 update manifest

Run:
1. `python tools/apply_ae035_in1_plane.py`
2. `python tools/ae035_native_plane_audit.py`
3. `python -m pytest`

Commit the modified native PCB and generated `docs/design_pack/AE-035_Generated_Native_Plane_Audit.json`. Do not commit `out/kicad/ProjectShellac.pre_AE035.kicad_pcb`.

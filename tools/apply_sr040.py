from pathlib import Path
import shutil

files = [
    ("generator/mechanical/sr040_audio_freeze.py","generator/mechanical/sr040_audio_freeze.py"),
    ("generator/procurement/full_bom_census.py","generator/procurement/full_bom_census.py"),
    ("generator/layout/sr040_routing_readiness.py","generator/layout/sr040_routing_readiness.py"),
    ("config/mechanical/sr040_audio_mechanical_freeze.yaml","config/mechanical/sr040_audio_mechanical_freeze.yaml"),
    ("docs/SR-040_Mechanical_BOM_Placement_Closure_Rev_A0.md","docs/SR-040_Mechanical_BOM_Placement_Closure_Rev_A0.md"),
    ("tests/test_sr040_mechanical_bom_placement.py","tests/test_sr040_mechanical_bom_placement.py"),
    ("tools/report_sr040.py","tools/report_sr040.py"),
]
# Files are already extracted to their final paths; validate existence rather
# than copying a path onto itself.
missing=[src for src,_ in files if not Path(src).exists()]
if missing:
    raise SystemExit("SR-040 package extraction incomplete: "+", ".join(missing))
print("SR-040 package files present.")

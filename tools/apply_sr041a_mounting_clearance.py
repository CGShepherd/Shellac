from pathlib import Path

def replace_exact(path_str, old, new):
    p=Path(path_str)
    text=p.read_text(encoding="utf-8")
    if new in text:
        print(f"{path_str}: already updated")
        return
    if old not in text:
        raise SystemExit(f"{path_str}: expected SR-041A anchor not found")
    p.write_text(text.replace(old,new,1),encoding="utf-8")
    print(f"{path_str}: updated")

# Move both mounting-hole columns outward while retaining the 8 mm Y inset.
replace_exact(
    "generator/mechanical/sr040_audio_freeze.py",
    "        hole_inset_x_mm=8.0,\n        hole_inset_y_mm=8.0,",
    "        hole_inset_x_mm=5.0,\n        hole_inset_y_mm=8.0,"
)

replace_exact(
    "config/mechanical/sr040_audio_mechanical_freeze.yaml",
    "    inset_mm: [8.0, 8.0]",
    "    inset_mm: [5.0, 8.0]"
)

# Update SR-040 deterministic mounting-hole test.
replace_exact(
    "tests/test_sr040_mechanical_bom_placement.py",
    "        (8.0,8.0),(212.0,8.0),(212.0,132.0),(8.0,132.0)",
    "        (5.0,8.0),(215.0,8.0),(215.0,132.0),(5.0,132.0)"
)

# Keep the controlled SR-040 narrative aligned with the corrected datum.
doc=Path("docs/SR-040_Mechanical_BOM_Placement_Closure_Rev_A0.md")
text=doc.read_text(encoding="utf-8")
text=text.replace(
    "Four non-plated M3-class PCB mounting holes are frozen at\n8 mm board-edge inset with 8 mm copper keep-out diameters.",
    "Four non-plated M3-class PCB mounting holes are frozen at\n5 mm X inset / 8 mm Y inset with 8 mm copper keep-out diameters."
)
doc.write_text(text,encoding="utf-8")

print("SR-041A mounting-hole clearance correction applied.")

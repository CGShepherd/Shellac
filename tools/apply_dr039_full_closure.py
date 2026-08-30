from pathlib import Path

def replace_once(path, old, new, label):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if new in text:
        print(label + ": already applied")
        return
    if old not in text:
        raise SystemExit(label + ": expected baseline text not found")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(label + ": applied")

old = """    output_end = Point(420, u2_out.y)
    output_tp = sheet.add_component(testpoint(
        f\"TP{base}4\", f\"{channel}_EQ_OUT\", Point(395, u2_out.y + 5.08)
    ))
    output_tp_pin = pin_position(output_tp, \"TP\")
    _wire_path(sheet, u2_out, output_tp_pin, output_end)
    sheet.add_label(post, output_end.x, output_end.y)
"""

new = """    # DR-039: common post-EQ DC block before SCH107 FILTER/BYPASS.
    raw_tp = sheet.add_component(testpoint(
        f\"TP{base}4\", f\"{channel}_EQ_RAW\", Point(395, u2_out.y + 5.08)
    ))
    raw_tp_pin = pin_position(raw_tp, \"TP\")
    dc_cap = sheet.add_component(capacitor(
        f\"C{base}60\", \"1u\", Point(425, u2_out.y),
        dielectric=\"PET film\", voltage=\"63V\",
        function=\"DR-039 common post-EQ DC block; WIMA MKS2 class\",
        rotation=90,
        footprint=\"Capacitor_THT:C_Rect_L7.2mm_W5.0mm_P5.00mm\"
    ))
    dc_bias = sheet.add_component(resistor(
        f\"R{base}60\", \"330k\", Point(455, u2_out.y + 15),
        tolerance=\"1%\", function=\"DR-039 downstream DC reference\"
    ))
    output_tp = sheet.add_component(testpoint(
        f\"TP{base}5\", f\"{channel}_EQ_OUT\", Point(455, u2_out.y + 5.08)
    ))
    output_tp_pin = pin_position(output_tp, \"TP\")
    output_end = Point(485, u2_out.y)
    _wire_path(sheet, u2_out, raw_tp_pin, pin_position(dc_cap, \"1\"))
    _wire_path(sheet, pin_position(dc_cap, \"2\"), output_tp_pin, output_end)
    sheet.connect_points(pin_position(dc_bias, \"1\"), pin_position(dc_cap, \"2\"))
    _label_on_dedicated_stub(
        sheet, pin_position(dc_bias, \"2\"), \"0VA\", dy=5.08, label_dx=5.08,
    )
    sheet.add_label(post, output_end.x, output_end.y)
"""
replace_once("generator/blocks/replay_eq.py", old, new, "SCH103 DR-039")

# Update the end-to-end gain/headroom model.
p = Path("generator/model/signal_chain_analysis.py")
text = p.read_text(encoding="utf-8")
if "post_eq_dc_magnitude" not in text:
    text = text.replace(
        "from .output_driver import DIFFERENTIAL_GAIN_LINEAR, DESIGN_OUTPUT_RMS_V",
        "from .output_driver import DIFFERENTIAL_GAIN_LINEAR, DESIGN_OUTPUT_RMS_V\\nfrom .post_eq_dc_block import magnitude as post_eq_dc_magnitude",
    )
    text = text.replace(
        "xlr = sch103 * rumble * DIFFERENTIAL_GAIN_LINEAR",
        "xlr = sch103 * post_eq_dc_magnitude(frequency_hz) * rumble * DIFFERENTIAL_GAIN_LINEAR",
    )
    p.write_text(text, encoding="utf-8")
    print("signal-chain DR-039: applied")

# Migrate SCH103 regression contract.
p = Path("tests/test_sch103_human_readable.py")
text = p.read_text(encoding="utf-8")
text = text.replace("for index in range(1, 5):", "for index in range(1, 6):")
needle = '        assert by_ref[f"R{base}41"].value == "11000"\n'
if 'C{base}60' not in text:
    addition = needle + (
        '        assert by_ref[f"C{base}60"].value == "1u"\n'
        '        assert by_ref[f"C{base}60"].footprint == "Capacitor_THT:C_Rect_L7.2mm_W5.0mm_P5.00mm"\n'
        '        assert by_ref[f"R{base}60"].value == "330k"\n'
    )
    if needle not in text:
        raise SystemExit("SCH103 test marker not found")
    text = text.replace(needle, addition, 1)
p.write_text(text, encoding="utf-8")
print("SCH103 regression contract: migrated")

# Update authoritative decision index.
p = Path("config/decisions/current_decision_index.yaml")
text = p.read_text(encoding="utf-8")
block_old = "  DR-039:\n    title: Common post-EQ DC block\n    status: CURRENT_SELECTED_PENDING_IMPLEMENTATION"
block_new = "  DR-039:\n    title: Common post-EQ DC block\n    status: CURRENT_IMPLEMENTED"
if block_old in text:
    text = text.replace(block_old, block_new, 1)
text = text.replace(
    "    implemented_baseline_still: SCH103 remains pre-DR039 until atomic CAD migration.",
    "    implementation: SCH103 includes 1uF film / 330k DC block before SCH107 FILTER/BYPASS.",
)
p.write_text(text, encoding="utf-8")
print("decision index: DR-039 CURRENT_IMPLEMENTED")

# Retire obsolete temporary migration scripts; historical AE records remain.
for name in (
    "APPLY_DR039_PATCH.py", "APPLY_SIGNAL_CHAIN_PATCH.py",
    "REPAIR_SIGNAL_CHAIN.py", "RESTORE_SCH103_BASELINE.py",
):
    q = Path(name)
    if q.exists():
        q.unlink()
        print("removed obsolete " + name)

from pathlib import Path


def replace_once(path: str, old: str, new: str, label: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    if new in text:
        print(f'{label}: already migrated')
        return
    if old not in text:
        raise SystemExit(f'{label}: expected text not found in {path}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8')
    print(f'{label}: migrated')

replace_once(
    'generator/layout/placement_clusters.py',
    '"R30030 C30020 C30021 C30022 C30023 C30024 C30025 C30026 U3002 R30040 R30041 TP3003 TP3004 C30050 C30051 C30052 C30053"',
    '"R30030 C30020 C30021 C30022 C30023 C30024 C30025 C30026 U3002 R30040 R30041 TP3003 TP3004 TP3005 C30050 C30051 C30052 C30053 C30060 R30060"',
    'Left SCH103 DR-039 cluster ownership',
)
replace_once(
    'generator/layout/placement_clusters.py',
    '"R35030 C35020 C35021 C35022 C35023 C35024 C35025 C35026 U3502 R35040 R35041 TP3503 TP3504 C35050 C35051 C35052 C35053"',
    '"R35030 C35020 C35021 C35022 C35023 C35024 C35025 C35026 U3502 R35040 R35041 TP3503 TP3504 TP3505 C35050 C35051 C35052 C35053 C35060 R35060"',
    'Right SCH103 DR-039 cluster ownership',
)

p = Path('tests/test_current_decision_index.py')
text = p.read_text(encoding='utf-8')
old = '''    assert _decision_status("DR-037") == "CURRENT_IMPLEMENTED"\n    for decision in ("DR-038","DR-039","DR-040"):\n        assert _decision_status(decision) == "CURRENT_SELECTED_PENDING_IMPLEMENTATION"\n'''
new = '''    assert _decision_status("DR-037") == "CURRENT_IMPLEMENTED"\n    assert _decision_status("DR-039") == "CURRENT_IMPLEMENTED"\n    for decision in ("DR-038", "DR-040"):\n        assert _decision_status(decision) == "CURRENT_SELECTED_PENDING_IMPLEMENTATION"\n'''
if old in text:
    text = text.replace(old, new, 1)
old2 = '''    assert re.search(r"(?m)^      converter_gain:\\s*3\\.48\\s*$", text)\n    assert "SCH103 remains pre-DR039 until atomic CAD migration." in text\n'''
new2 = '''    assert re.search(r"(?m)^      converter_gain:\\s*3\\.48\\s*$", text)\n    dr039 = text.split("  DR-039:", 1)[1].split("  DR-040:", 1)[0]\n    assert "status: CURRENT_IMPLEMENTED" in dr039\n    assert "SCH103 includes 1uF film / 330k DC block" in dr039\n'''
if old2 in text:
    text = text.replace(old2, new2, 1)
p.write_text(text, encoding='utf-8')
print('AE-020 decision-index regression: migrated')

replace_once(
    'tests/test_real_footprint_audit.py',
    'assert audit.board_population_count == 243',
    'assert audit.board_population_count == 249',
    'Real-footprint board population',
)

p = Path('generator/model/signal_chain_analysis.py')
text = p.read_text(encoding='utf-8')
old = 'expected = NOMINAL_CARTRIDGE_RMS_V * default.total_gain * RECOVERY_GAIN * DIFFERENTIAL_GAIN_LINEAR'
new = 'expected = (NOMINAL_CARTRIDGE_RMS_V * default.total_gain * RECOVERY_GAIN * post_eq_dc_magnitude(1000.0) * DIFFERENTIAL_GAIN_LINEAR)'
if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise SystemExit('AE-012 expected-value expression not found')
p.write_text(text, encoding='utf-8')
print('AE-012 DR-039 invariant: migrated')

print('AE-021B root-cause migration complete.')

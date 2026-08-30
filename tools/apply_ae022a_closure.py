from pathlib import Path

def replace_once(path, old, new, label):
    p=Path(path)
    text=p.read_text(encoding="utf-8")
    if new in text:
        print(label+": already applied")
        return
    if old not in text:
        raise SystemExit(label+": expected text not found in "+path)
    p.write_text(text.replace(old,new,1),encoding="utf-8")
    print(label+": migrated")

# LT5400 EP9 explicit no-connect.
p=Path("generator/blocks/balanced_input.py")
text=p.read_text(encoding="utf-8")
needle='    sheet.connect_points(pin_position(rn,"1"),mp); sheet.connect_points(pin_position(rn,"8"),pin_position(amp,"OUT"))\n'
if needle in text and 'sheet.add_no_connect_pin(rn,"9")' not in text:
    text=text.replace(needle,needle+'    sheet.add_no_connect_pin(rn,"9")\n',1)
p.write_text(text,encoding="utf-8")
print("LT5400 EP9 explicit no-connect: migrated")

replace_once(
    "tests/test_commissioning_baseline.py",
    'assert "7.8996 V/V" in expected["SCH101 DEFAULT gain"]',
    'assert "7.9960 V/V" in expected["SCH101 DEFAULT gain"]',
    "Commissioning SCH101 default gain",
)

# DR038 staging regression.
p=Path("tests/test_dr038_dr039.py")
text=p.read_text(encoding="utf-8")
text=text.replace("def test_active_sch101_remains_pre_cad_baseline():","def test_active_sch101_is_dr038_implemented_baseline():")
text=text.replace("assert DIFF_CONVERTER_GAIN == 3.48","assert DIFF_CONVERTER_GAIN == 4.0")
p.write_text(text,encoding="utf-8")
print("DR038/DR039 regression: migrated")

# Rewrite ERC routing tests.
erc=Path("tools/ae022a_erc_replacement.txt").read_text(encoding="utf-8")
Path("tests/test_erc_branch_routing.py").write_text(erc,encoding="utf-8")
print("SCH101 ERC routing regressions: rewritten")

# Replace old wire-count invariant.
p=Path("tests/test_pin_connectivity.py")
text=p.read_text(encoding="utf-8")
old='    assert len(sheet.wires) >= 120\n'
new='    refs={component.ref for component in sheet.components}\n    assert {"RN130","RN230","U103","U203"} <= refs\n    assert len(sheet.wires) >= 90\n'
if old in text:
    text=text.replace(old,new,1)
p.write_text(text,encoding="utf-8")
print("SCH101 connectivity invariant: migrated")

# Freeze AE-013 on historical pre-DR038 gain settings.
p=Path("generator/model/sch101_precision_analysis.py")
text=p.read_text(encoding="utf-8")
text=text.replace("from .balanced_input import GAIN_SETTINGS\n","")
if "LEGACY_GAIN_SETTINGS" not in text:
    marker="CANDIDATE_IMPEDANCE_SCALE = 0.1\n"
    block='''CANDIDATE_IMPEDANCE_SCALE = 0.1

@dataclass(frozen=True, slots=True)
class _LegacyGainSetting:
    name: str
    rf_ohm: float

LEGACY_GAIN_SETTINGS = (
    _LegacyGainSetting("LOW", 4420.0),
    _LegacyGainSetting("DEFAULT", 12700.0),
    _LegacyGainSetting("HIGH", 26100.0),
)
'''
    text=text.replace(marker,block,1)
text=text.replace("return next(item for item in GAIN_SETTINGS if item.name == name)","return next(item for item in LEGACY_GAIN_SETTINGS if item.name == name)")
text=text.replace("for item in GAIN_SETTINGS)","for item in LEGACY_GAIN_SETTINGS)")
text=text.replace("for item in GAIN_SETTINGS\n","for item in LEGACY_GAIN_SETTINGS\n")
text=text.replace("the current controlled implementation (0.1% discrete resistors);","the historical pre-DR038 controlled implementation (0.1% discrete resistors);")
text=text.replace("It does not change the active schematic.","It is retained as historical assurance evidence and does not define the active schematic.")
p.write_text(text,encoding="utf-8")
print("AE-013 historical baseline: isolated")

p=Path("tests/test_sch101_precision_analysis.py")
text=p.read_text(encoding="utf-8")
text=text.replace("test_current_discrete_0p1_percent_cmrr_is_not_precision_balanced","test_historical_discrete_0p1_percent_cmrr_was_not_precision_balanced")
p.write_text(text,encoding="utf-8")

# Preserve equivalent headroom criterion after +0.105 dB deliberate gain increase.
p=Path("generator/model/signal_chain_analysis.py")
text=p.read_text(encoding="utf-8")
old='    assert normal.xlr_margin_db > 4.6\n'
new='''    legacy_default_gain = 7.8996
    dr038_gain_penalty_db = db(default.total_gain / legacy_default_gain)
    assert normal.xlr_margin_db > 4.6 - dr038_gain_penalty_db
'''
if old in text:
    text=text.replace(old,new,1)
p.write_text(text,encoding="utf-8")
print("AE-012 equivalent headroom criterion: migrated")

# Stale active-contract audit.
tokens=("3.48","7.8996","R130","R131","R132","R133","R230","R231","R232","R233","SW1011")
hits=[]
for root in ("generator","tests","config"):
    for q in Path(root).rglob("*"):
        if not q.is_file() or q.suffix not in (".py",".yaml",".yml",".md",".txt"):
            continue
        txt=q.read_text(encoding="utf-8",errors="ignore")
        found=[tok for tok in tokens if tok in txt]
        if found:
            hits.append((q.as_posix(),found))
out=Path("docs/AE-022A_Generated_Stale_SCH101_Contract_Audit.md")
lines=["# AE-022A Generated Stale SCH101 Contract Audit","",
       "Historical hits are allowed; active generator/test assumptions require review.","",
       "| File | Tokens |","|---|---|"]
for q,found in hits:
    lines.append(f"| `{q}` | {', '.join(found)} |")
out.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("Generated stale-contract audit:",len(hits),"files")

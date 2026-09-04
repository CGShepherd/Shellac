from pathlib import Path
import re

REPO=Path(__file__).resolve().parents[1]
TEST=REPO/"tests/test_ae039c_real_kicad_opamp_units.py"

CANONICAL = r'''def test_sch104_writer_emits_u401_units_one_and_two(tmp_path: Path):
    sheet=Sheet("SCH104","SCH104.kicad_sch")
    add_final_gain(sheet)
    out=tmp_path/"SCH104.kicad_sch"
    write_schematic(sheet,out)
    text=out.read_text(encoding="utf-8")

    assert '(reference "U402")' not in text
    assert text.count('(reference "U401")')==2

    positions=[]
    cursor=0
    marker='(reference "U401")'
    while True:
        idx=text.find(marker,cursor)
        if idx<0:
            break
        positions.append(idx)
        cursor=idx+len(marker)

    assert len(positions)==2
    blocks=[]
    for idx in positions:
        end=text.find(')',idx+len(marker))
        blocks.append(text[idx:end+80])

    assert sum('(unit 1)' in block for block in blocks)==1
    assert sum('(unit 2)' in block for block in blocks)==1
'''

def main():
    text=TEST.read_text(encoding="utf-8")
    pattern=re.compile(
        r'^def test_sch104_writer_emits_u401_units_one_and_two\(tmp_path: Path\):\n'
        r'.*?(?=^def |\Z)',
        re.MULTILINE | re.DOTALL,
    )
    matches=list(pattern.finditer(text))
    if len(matches)!=1:
        raise SystemExit(f"Expected exactly one SCH104 unit-instance test function; found {len(matches)}.")

    text=pattern.sub(CANONICAL+"\n",text,count=1)
    TEST.write_text(text,encoding="utf-8")

    final=TEST.read_text(encoding="utf-8")
    assert final.count("def test_sch104_writer_emits_u401_units_one_and_two") == 1
    assert 'assert text.count(\'(reference "U401")\')==2' in final
    assert "sum('(unit 1)' in block for block in blocks)==1" in final
    assert "sum('(unit 2)' in block for block in blocks)==1" in final

    print("AE-039C2B APPLIED")
    print("Replaced SCH104 unit-instance regression with canonical function.")
    print("Implementation files were not modified.")

if __name__=="__main__":
    main()
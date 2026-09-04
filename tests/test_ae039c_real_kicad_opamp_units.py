from pathlib import Path
from generator.blocks.final_gain import add_final_gain
from generator.blocks.mode_matrix import add_mode_matrix
from generator.blocks.rumble_filter import add_rumble_filter
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.core.sheet import Sheet
from generator.layout.footprint_contract import build_footprint_contract
from generator.writers.kicad9 import local_symbol_library, opamp_render_identity, write_schematic

def _component(sheet,ref):
    return next(c for c in sheet.components if c.ref==ref)

def _wire_touches(sheet,a,b):
    endpoints={((w.x1,w.y1),(w.x2,w.y2)) for w in sheet.wires}
    pa=(a.x,a.y); pb=(b.x,b.y)
    return (pa,pb) in endpoints or (pb,pa) in endpoints

def test_writer_maps_logical_dual_units_to_one_physical_reference():
    a=type("C",(),{"ref":"U401"})(); b=type("C",(),{"ref":"U402"})()
    ia=opamp_render_identity(a); ib=opamp_render_identity(b)
    assert ia["reference"]==ib["reference"]=="U401"
    assert ia["unit"]==1 and ib["unit"]==2
    assert ia["pins"]==("1","2","3","4","8")
    assert ib["pins"]==("4","5","6","7","8")

def test_opa1655_single_identity_uses_real_soic8_pins():
    i=opamp_render_identity(type("C",(),{"ref":"U103"})())
    assert i["reference"]=="U103" and i["value"]=="OPA1655" and i["unit"]==1
    assert i["pins"]==("2","3","4","6","7")

def test_kicad_library_contains_real_multiunit_pin_numbers():
    lib=local_symbol_library()
    assert 'symbol "OpAmp_NonInv_Block_1_1"' in lib
    assert 'symbol "OpAmp_NonInv_Block_2_1"' in lib
    assert '(number "3"' in lib and '(number "5"' in lib
    assert '(number "8"' in lib and '(number "4"' in lib

def test_sch104_writer_emits_u401_units_one_and_two(tmp_path: Path):
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

def test_buffer_builders_have_explicit_follower_feedback():
    for title,builder,refs in (
        ("SCH104",add_final_gain,("U401","U402")),
        ("SCH105",add_mode_matrix,("U501","U502")),
        ("SCH107",add_rumble_filter,("U700","U720","U750","U770")),
    ):
        sheet=Sheet(title,f"{title}.kicad_sch"); builder(sheet)
        for ref in refs:
            op=_component(sheet,ref)
            out=pin_position(op,"OUT"); inv=pin_position(op,"IN-"); corner=Point(out.x,inv.y)
            assert _wire_touches(sheet,out,corner)
            assert _wire_touches(sheet,corner,inv)

def test_physical_population_unchanged():
    assert len(build_footprint_contract().board_population_refs)==246

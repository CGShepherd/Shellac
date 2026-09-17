from generator.blocks.balanced_input import add_sch101_rf_slice
from generator.core.sheet import Sheet

def _sheet():
    s=Sheet(title="test",filename="test.kicad_sch")
    add_sch101_rf_slice(s)
    return s

def test_rf_slice_components_and_service_headers():
    refs={c.ref for c in _sheet().components}
    for ref in (
        "J101","J201","R102","R103","R104","R105","C101","C102","C103","C104",
        "R202","R203","R204","R205","C201","C202","C203","C204",
        "H110","H111","H112","H120","H121","H122",
    ):
        assert ref in refs

def test_ae042_load_values_are_rendered_and_old_22p_dnp_is_gone():
    by_ref={c.ref:c for c in _sheet().components}
    assert by_ref["C101"].value=="47p"
    assert by_ref["C102"].value=="47p"
    assert by_ref["C103"].value=="47p" and not by_ref["C103"].dnp
    assert by_ref["C104"].value=="100p" and not by_ref["C104"].dnp
    assert by_ref["C203"].value=="47p" and not by_ref["C203"].dnp
    assert by_ref["C204"].value=="100p" and not by_ref["C204"].dnp
    assert all(c.value!="22p" for c in by_ref.values())

def test_ae042_gain_resistors_replace_old_series_link_topology():
    by_ref={component.ref:component for component in _sheet().components}
    assert by_ref["R112"].value=="999"
    assert by_ref["R113"].value=="332"
    assert by_ref["R114"].value=="866"
    assert by_ref["R122"].value=="999"
    assert by_ref["R123"].value=="332"
    assert by_ref["R124"].value=="866"
    for ref in ("R115","R116","R125","R126","R215","R216","R225","R226"):
        assert ref not in by_ref

def test_service_header_candidates_and_footprints_are_explicit():
    by_ref={component.ref:component for component in _sheet().components}
    for ref in ("H110","H111","H112"):
        c=by_ref[ref]
        assert c.footprint=="Connector_PinHeader_2.54mm:PinHeader_2x04_P2.54mm_Vertical"
        assert c.fields["Header candidate"]=="Samtec TSW-104-07-G-D"
        assert c.fields["Shunt candidate"]=="Samtec MNT-104-BK-G"
    for ref in ("H120","H121","H122"):
        c=by_ref[ref]
        assert c.footprint=="Connector_PinHeader_2.54mm:PinHeader_2x02_P2.54mm_Vertical"
        assert c.fields["Header candidate"]=="Samtec TSW-102-07-G-D"
        assert c.fields["Shunt candidate"]=="Samtec MNT-102-BK-G"

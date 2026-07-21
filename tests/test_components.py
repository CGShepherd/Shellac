from generator.core.components import resistor, xlr3
from generator.core.geometry import Point

def test_resistor_metadata():
    r = resistor("R101", "100R", Point(1, 2), tolerance="1%", function="RF isolation")
    assert r.ref == "R101"
    assert r.value == "100R"
    assert r.fields["Tolerance"] == "1%"
    assert r.fields["Function"] == "RF isolation"

def test_xlr_metadata():
    j = xlr3("J101", "LEFT INPUT XLR", Point(1, 2))
    assert j.lib_id == "Connector_Generic:Conn_01x03"
    assert j.fields["Pin 1"] == "CHASSIS"

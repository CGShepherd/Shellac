from generator.core.components import lt5400_network
from generator.core.pins import pin_position
from generator.core.geometry import Point

def test_lt5400_primitive_has_nine_unique_semantic_pin_locations():
    rn=lt5400_network("RNTEST","LT5400 TEST",Point(100,100))
    pts=[pin_position(rn,str(i)) for i in range(1,10)]
    assert len({(p.x,p.y) for p in pts}) == 9

def test_lt5400_opposite_terminals_are_spatially_separated():
    rn=lt5400_network("RNTEST","LT5400 TEST",Point(100,100))
    for a,b in (("1","8"),("2","7"),("3","6"),("4","5")):
        pa,pb=pin_position(rn,a),pin_position(rn,b)
        assert pa != pb
        assert abs(pa.x-pb.x) >= 20.0

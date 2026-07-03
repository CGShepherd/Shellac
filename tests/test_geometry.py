from generator.core.geometry import Point, Size, Box

def test_point_offsets():
    p = Point(10, 20)
    assert p.right(5) == Point(15, 20)
    assert p.left(3) == Point(7, 20)
    assert p.up(4) == Point(10, 16)
    assert p.down(2) == Point(10, 22)

def test_box_centre():
    b = Box(Point(0, 0), Size(10, 20))
    assert b.centre == Point(5, 10)

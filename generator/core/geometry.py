from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def right(self, dx: float): return Point(self.x + dx, self.y)
    def left(self, dx: float): return Point(self.x - dx, self.y)
    def up(self, dy: float): return Point(self.x, self.y - dy)
    def down(self, dy: float): return Point(self.x, self.y + dy)

@dataclass(frozen=True)
class Size:
    width: float
    height: float

@dataclass(frozen=True)
class Box:
    origin: Point
    size: Size

    @property
    def centre(self):
        return Point(self.origin.x + self.size.width / 2, self.origin.y + self.size.height / 2)

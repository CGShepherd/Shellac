from dataclasses import dataclass, field, replace
from .connectivity import Label, Wire
from .geometry import Point
from .grid import align_coordinate, align_point
from .pins import pin_position

@dataclass
class Sheet:
    title: str
    filename: str
    components: list = field(default_factory=list)
    labels: list[Label] = field(default_factory=list)
    wires: list[Wire] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    no_connects: list[Point] = field(default_factory=list)

    def add_component(self, component):
        """Add a component at a canonical electrical-grid origin.

        Components are copied rather than mutated so callers retaining the
        requested object cannot observe a partially normalised design state.
        """
        aligned = replace(component, at=align_point(component.at))
        self.components.append(aligned)
        return aligned

    def add_label(self, name, x, y):
        point = align_point(Point(x, y))
        self.labels.append(Label(name, point.x, point.y))

    def add_wire(self, x1, y1, x2, y2):
        start = align_point(Point(x1, y1))
        end = align_point(Point(x2, y2))
        if start == end:
            return None
        wire = Wire(start.x, start.y, end.x, end.y)
        self.wires.append(wire)
        return wire

    def add_note(self, note):
        self.notes.append(note)

    def add_no_connect_pin(self, component, pin_name: str):
        self.no_connects.append(align_point(pin_position(component, pin_name)))

    def connect_points(self, start: Point, end: Point):
        """Add a direct electrical wire between canonical sheet points."""
        return self.add_wire(start.x, start.y, end.x, end.y)

    def connect_pins(self, component_a, pin_a: str, component_b, pin_b: str):
        self.connect_points(pin_position(component_a, pin_a), pin_position(component_b, pin_b))

    def connect_pins_manhattan(self, component_a, pin_a: str, component_b, pin_b: str, *, via_x: float):
        start = pin_position(component_a, pin_a)
        end = pin_position(component_b, pin_b)
        lane_x = align_coordinate(via_x)
        self.connect_points(start, Point(lane_x, start.y))
        self.connect_points(Point(lane_x, start.y), Point(lane_x, end.y))
        self.connect_points(Point(lane_x, end.y), end)

    def connect_pin_to_net(self, component, pin_name: str, net_name: str, *, stub_dx: float = 0.0, stub_dy: float = 0.0):
        start = pin_position(component, pin_name)
        end = align_point(Point(start.x + stub_dx, start.y + stub_dy))
        self.connect_points(start, end)
        self.add_label(net_name, end.x, end.y)
        return end

    def connect_vertical_two_pin(self, component, pin1_net: str, pin2_net: str, *, stub: float = 4.0):
        if component.rotation % 180:
            raise ValueError("connect_vertical_two_pin requires a vertical symbol")
        self.connect_pin_to_net(component, "1", pin1_net, stub_dy=stub)
        self.connect_pin_to_net(component, "2", pin2_net, stub_dy=-stub)

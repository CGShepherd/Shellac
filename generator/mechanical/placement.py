"""Preliminary scalable board-region placement synthesis."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from generator.layout.constraints import build_layout_baseline


@dataclass(frozen=True, slots=True)
class RegionBox:
    identifier: str
    name: str
    x_mm: float
    y_mm: float
    width_mm: float
    depth_mm: float
    sequence: int
    route_direction: str
    notes: str

    @property
    def area_mm2(self) -> float:
        return self.width_mm * self.depth_mm


@dataclass(slots=True)
class PlacementSynthesis:
    identifier: str
    revision: str
    board_width_mm: float
    board_depth_mm: float
    edge_clearance_mm: float
    regions: list[RegionBox] = field(default_factory=list)
    invariants: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        payload = asdict(self)
        for region, raw in zip(self.regions, payload["regions"]):
            raw["area_mm2"] = region.area_mm2
        return payload


def _overlap(a: RegionBox, b: RegionBox) -> bool:
    return not (
        a.x_mm + a.width_mm <= b.x_mm
        or b.x_mm + b.width_mm <= a.x_mm
        or a.y_mm + a.depth_mm <= b.y_mm
        or b.y_mm + b.depth_mm <= a.y_mm
    )


def validate_synthesis(model: PlacementSynthesis) -> list[str]:
    issues: list[str] = []
    for region in model.regions:
        if region.x_mm < model.edge_clearance_mm or region.y_mm < model.edge_clearance_mm:
            issues.append(f"{region.identifier} violates lower/left edge clearance")
        if region.x_mm + region.width_mm > model.board_width_mm - model.edge_clearance_mm:
            issues.append(f"{region.identifier} violates right edge clearance")
        if region.y_mm + region.depth_mm > model.board_depth_mm - model.edge_clearance_mm:
            issues.append(f"{region.identifier} violates top edge clearance")
    for index, a in enumerate(model.regions):
        for b in model.regions[index + 1:]:
            if _overlap(a, b):
                issues.append(f"{a.identifier} overlaps {b.identifier}")
    return issues


def build_placement_synthesis(width_mm: float = 220.0, depth_mm: float = 140.0) -> PlacementSynthesis:
    baseline = build_layout_baseline()
    if width_mm < baseline.envelope.minimum_usable_width_mm or depth_mm < baseline.envelope.minimum_usable_depth_mm:
        raise ValueError("board dimensions are below the frozen minimum architecture envelope")

    edge = baseline.envelope.board_edge_clearance_mm
    usable_w = width_mm - 2 * edge
    usable_d = depth_mm - 2 * edge

    # G3-019 freezes front-to-rear equipment flow. Board y=front-to-rear;
    # x remains left-to-right when viewed from the component side.  Channel
    # functions may sit side-by-side within a flow band, while processing
    # sequence increases toward the rear panel.
    gap = 3.0
    available = usable_d - 3 * gap
    input_d = 0.20 * available
    eq_d = 0.29 * available
    middle_d = 0.27 * available
    rear_d = available - input_d - eq_d - middle_d

    front_y = edge
    eq_y = front_y + input_d + gap
    middle_y = eq_y + eq_d + gap
    rear_y = middle_y + middle_d + gap

    split_gap = 4.0
    half_w = (usable_w - split_gap) / 2.0
    control_gap = 3.0
    control_w = 0.16 * usable_w
    side_w = (usable_w - control_w - 2 * control_gap) / 2.0
    middle_left_w = side_w
    control_x = edge + middle_left_w + control_gap
    middle_right_x = control_x + control_w + control_gap
    middle_right_w = side_w

    # Rear band reserves a central high-level/DC entry corridor while keeping
    # the balanced-output region around it. It is a coarse architectural box;
    # exact rear connector coordinates remain enclosure/order-code dependent.
    dc_w = 0.38 * usable_w
    dc_x = edge + (usable_w - dc_w) / 2.0
    out_left_w = dc_x - edge - split_gap / 2.0
    out_right_x = dc_x + dc_w + split_gap / 2.0
    out_right_w = width_mm - edge - out_right_x

    regions = [
        RegionBox("REG-01", "Balanced input and RF protection", edge, front_y, usable_w, input_d, 10, "front-to-rear", "Immediately behind the front input XLRs; low-level input islands remain isolated from power and output wiring."),
        RegionBox("REG-02", "Replay EQ left", edge, eq_y, half_w, eq_d, 20, "front-to-rear", "Left-channel EQ occupies one side of the second flow band."),
        RegionBox("REG-03", "Replay EQ right", edge + half_w + split_gap, eq_y, half_w, eq_d, 30, "front-to-rear", "Right-channel EQ occupies the opposite side of the second flow band."),
        RegionBox("REG-04", "Rumble filter", edge, middle_y, middle_left_w, middle_d, 40, "front-to-rear", "Frequency-setting networks remain local; controls register vertically to the upper cover rather than through a harness edge."),
        RegionBox("REG-08", "Top-panel control and indicator logic", control_x, middle_y, control_w, middle_d, 80, "vertical-registration", "Dedicated PCB control/indicator logic region; operator hardware registers vertically to the upper cover with no flying switch/pot harness."),
        RegionBox("REG-05", "Final gain and mode matrix", middle_right_x, middle_y, middle_right_w, middle_d, 50, "front-to-rear", "Controlled transition to mode selection and output processing."),
        RegionBox("REG-06A", "Mute and balanced output left/rear", edge, rear_y, out_left_w, rear_d, 60, "front-to-rear", "Rear output region adjacent to one side of the rear connector field."),
        RegionBox("REG-07", "DC entry and bulk decoupling", dc_x, rear_y, dc_w, rear_d, 70, "rear-inward", "Regulated DC enters near rear centreline and feeds the rail spine without entering the cartridge-input zone."),
        RegionBox("REG-06B", "Mute and balanced output right/rear", out_right_x, rear_y, out_right_w, rear_d, 60, "front-to-rear", "Rear output region adjacent to the opposite side of the rear connector field."),
    ]
    model = PlacementSynthesis(
        identifier="G3-PLC-003",
        revision="Rev A1",
        board_width_mm=width_mm,
        board_depth_mm=depth_mm,
        edge_clearance_mm=edge,
        regions=regions,
        invariants=[
            "Board y-axis represents front-to-rear enclosure flow.",
            "Input region occupies the front board edge.",
            "Balanced-output and regulated-DC regions occupy the rear high-level edge.",
            "Regulated DC entry is reserved near the rear centreline.",
            "Left and right replay-EQ regions do not overlap.",
            "Operator controls register vertically to the upper cover; no control-harness edge is reserved.",
            "All regions remain inside the enclosure-dependent PCB edge clearance.",
        ],
    )
    issues = validate_synthesis(model)
    if issues:
        raise ValueError("invalid placement synthesis: " + "; ".join(issues))
    return model

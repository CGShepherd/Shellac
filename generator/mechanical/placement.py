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

    # The placement model uses two signal-flow rows.  Inputs are at the right
    # edge, outputs at the left edge, matching the established equipment and
    # panel-orientation preference.  Sequence increases from input to output,
    # although x decreases across the board.
    top_y = edge
    row_gap = 4.0
    row_d = (usable_d - row_gap) / 2
    lower_y = edge + row_d + row_gap

    widths = {
        "input": 0.18 * usable_w,
        "eq": 0.29 * usable_w,
        "middle": 0.25 * usable_w,
        "output": 0.20 * usable_w,
    }
    reserve = usable_w - sum(widths.values())
    x_right = width_mm - edge

    def take(w: float) -> float:
        nonlocal x_right
        x_right -= w
        x = x_right
        x_right -= reserve / 3 if x_right > edge + widths["output"] else 0
        return x

    input_x = take(widths["input"])
    eq_x = take(widths["eq"])
    middle_x = take(widths["middle"])
    output_x = edge

    regions = [
        RegionBox("REG-01", "Balanced input and RF protection", input_x, edge, widths["input"], usable_d, 10, "right-to-left", "Closest to the right-side input harness; isolated from control and output routing."),
        RegionBox("REG-02", "Replay EQ left", eq_x, edge, widths["eq"], row_d, 20, "right-to-left", "Left-channel feedback and selectors remain entirely inside this box."),
        RegionBox("REG-03", "Replay EQ right", eq_x, lower_y, widths["eq"], row_d, 30, "right-to-left", "Right-channel geometry mirrors the left only where loop-area performance is preserved."),
        RegionBox("REG-04", "Rumble filter", middle_x, edge, widths["middle"] * 0.46, usable_d, 40, "right-to-left", "Frequency-setting networks remain local and clear of control harnesses."),
        RegionBox("REG-05", "Final gain and mode matrix", middle_x + widths["middle"] * 0.50, edge, widths["middle"] * 0.50, usable_d, 50, "right-to-left", "Provides the controlled transition from channel processing to mode selection."),
        RegionBox("REG-06", "Mute and balanced output", output_x, edge, widths["output"], usable_d * 0.64, 60, "right-to-left", "Closest to the left-side output harness."),
        RegionBox("REG-07", "DC entry and bulk decoupling", output_x, edge + usable_d * 0.70, widths["output"], usable_d * 0.30, 70, "local", "Power enters at the high-level/output end and feeds a controlled rail spine."),
    ]
    model = PlacementSynthesis(
        identifier="G3-PLC-003",
        revision="Rev A0",
        board_width_mm=width_mm,
        board_depth_mm=depth_mm,
        edge_clearance_mm=edge,
        regions=regions,
        invariants=[
            "Input region occupies the right-side board edge.",
            "Output and DC-entry regions occupy the left-side high-level edge.",
            "Left and right replay-EQ regions do not overlap.",
            "No control-harness region is permitted inside the cartridge-input island.",
            "All regions remain inside the enclosure-dependent PCB edge clearance.",
        ],
    )
    issues = validate_synthesis(model)
    if issues:
        raise ValueError("invalid placement synthesis: " + "; ".join(issues))
    return model

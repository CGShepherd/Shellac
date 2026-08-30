"""AE-018 physical/electrical contracts for DR-038 precision CAD primitives.

These contracts are intentionally not wired into active SCH101 yet.  They give
the next atomic migration one authoritative source for LT5400-7 connectivity,
package requirements, and precision service-link behaviour.
"""
from __future__ import annotations
from dataclasses import dataclass

LT5400_FAMILY = "LT5400"
LT5400_OPTION = "LT5400-7"
LT5400_GRADE = "A"
LT5400_MANUFACTURER = "Analog Devices"
LT5400_DATASHEET = "LT5400 Rev C"

# Datasheet available-options table.
LT5400_R1_OHM = 5_000.0
LT5400_R2_OHM = 1_250.0
LT5400_R3_OHM = 1_250.0
LT5400_R4_OHM = 5_000.0
LT5400_RATIO = 4.0

# Top-view pin configuration, MS8E package.
LT5400_RESISTOR_PINS = {
    "R1": ("1", "8"),
    "R2": ("2", "7"),
    "R3": ("3", "6"),
    "R4": ("4", "5"),
}
LT5400_EXPOSED_PAD_PIN = "9"
LT5400_EXPOSED_PAD_ELECTRICAL = "FLOATING"

# Manufacturer specifications relevant to DR-038.
LT5400_A_MATCHING_MAX_PERCENT = 0.010
LT5400_A_CMRR_MATCHING_MAX_PERCENT = 0.005
LT5400_MATCHING_DRIFT_TYP_PPM_C = 0.2
LT5400_MATCHING_DRIFT_MAX_PPM_C = 1.0

# Physical contract.  Do not bind to a KiCad footprint name until the EP
# geometry has been verified against the package drawing/library footprint.
LT5400_PACKAGE = "MS8E: 8-lead plastic MSOP with exposed pad"
LT5400_CAD_FOOTPRINT_STATUS = "VERIFY_EP_GEOMETRY_BEFORE_BINDING"
LT5400_CAD_RULE = (
    "One physical MS8E component per channel; exposed pad present physically "
    "but not used as an electrical resistor terminal."
)

# DR-038 internal configuration is a service operation, not a user control.
SERVICE_LINK_TYPE = "solder bridge / hard configuration link"
SERVICE_LINK_NORMAL_SETTING = "DEFAULT"
SERVICE_LINK_PATTERNS = {
    "LOW": "00",
    "DEFAULT": "01",
    "HIGH": "10",
}
SERVICE_LINK_INVALID_PATTERN = "11"
SERVICE_LINK_RULE = (
    "Corresponding L+, L-, R+, R- gain segments must be configured identically. "
    "No ordinary DIP contact is permitted in the precision feedback ratio."
)


@dataclass(frozen=True, slots=True)
class PrecisionCadGate:
    name: str
    status: str
    acceptance: tuple[str, ...]


GATES = (
    PrecisionCadGate(
        "LT5400 footprint",
        "OPEN",
        (
            "MS8E exposed-pad land pattern verified against manufacturer drawing",
            "pin 1 orientation verified",
            "pin pairs 1-8, 2-7, 3-6, 4-5 verified",
            "pad 9 electrically floating in netlist",
        ),
    ),
    PrecisionCadGate(
        "Service links",
        "OPEN",
        (
            "no ordinary DIP contact in precision feedback path",
            "LOW/DEFAULT/HIGH patterns unambiguous on PCB/silkscreen",
            "11 state impossible or explicitly prohibited",
            "all four gain legs configured identically",
        ),
    ),
)


def validate_precision_cad_contract() -> None:
    assert LT5400_R1_OHM / LT5400_R2_OHM == LT5400_RATIO
    assert LT5400_R4_OHM / LT5400_R3_OHM == LT5400_RATIO
    assert set(LT5400_RESISTOR_PINS) == {"R1", "R2", "R3", "R4"}
    all_pins = [p for pair in LT5400_RESISTOR_PINS.values() for p in pair]
    assert sorted(all_pins, key=int) == [str(i) for i in range(1, 9)]
    assert LT5400_EXPOSED_PAD_PIN not in all_pins
    assert SERVICE_LINK_PATTERNS["DEFAULT"] == "01"
    assert SERVICE_LINK_INVALID_PATTERN not in SERVICE_LINK_PATTERNS.values()

"""Gate 3 quantitative performance and design-margin baseline.

The values here are derived from the frozen electrical models.  Where a
quantity still depends on cartridge data, enclosure geometry, transformer
choice, or bench measurement, it is explicitly marked provisional rather than
guessed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from math import log10

from generator.model.balanced_input import GAIN_SETTINGS
from generator.model.final_gain import DESIGN_OUTPUT_RMS_V as SCH104_CEILING_RMS_V
from generator.model.output_driver import (
    DATASHEET_MAX_OUTPUT_RMS_V,
    DESIGN_OUTPUT_RMS_V as DRIVER_DESIGN_OUTPUT_RMS_V,
    DIFFERENTIAL_GAIN_LINEAR,
)


class EvidenceStatus(str, Enum):
    VALIDATED = "validated"
    CALCULATED = "calculated"
    PROVISIONAL = "provisional"
    MEASUREMENT_REQUIRED = "measurement_required"


class Criticality(str, Enum):
    PERFORMANCE_DEFINING = "performance_defining"
    PERFORMANCE_INFLUENCING = "performance_influencing"
    RELIABILITY_DEFINING = "reliability_defining"
    COMMODITY = "commodity"
    MECHANICAL_DEPENDENT = "mechanical_dependent"


@dataclass(frozen=True, slots=True)
class GainSettingBudget:
    name: str
    input_stage_gain_linear: float
    input_stage_gain_db: float
    nominal_5mv_output_rms_v: float
    nominal_5mv_output_dbv: float


@dataclass(frozen=True, slots=True)
class MarginRecord:
    identifier: str
    parameter: str
    requirement: float
    design_value: float
    unit: str
    margin_ratio: float
    margin_db: float | None
    status: EvidenceStatus
    rationale: str


@dataclass(frozen=True, slots=True)
class CriticalityRecord:
    identifier: str
    item_pattern: str
    classification: Criticality
    substitution_policy: str
    verification: str


@dataclass(frozen=True, slots=True)
class PlacementConstraint:
    identifier: str
    loop_or_group: str
    maximum_component_distance_mm: float | None
    maximum_signal_vias: int
    required_adjacency: str
    prohibited_geometry: str
    verification: str


@dataclass(slots=True)
class PerformanceBaseline:
    identifier: str
    revision: str
    status: str
    nominal_cartridge_rms_v: float
    gain_settings: list[GainSettingBudget] = field(default_factory=list)
    margins: list[MarginRecord] = field(default_factory=list)
    criticality: list[CriticalityRecord] = field(default_factory=list)
    placement_constraints: list[PlacementConstraint] = field(default_factory=list)
    open_measurements: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _db(value: float) -> float:
    return 20.0 * log10(value)


def build_performance_baseline() -> PerformanceBaseline:
    nominal = 0.005
    gains = []
    for option in GAIN_SETTINGS:
        # SCH103's 1 kHz gain varies with replay curve, so the end-to-end values
        # below deliberately stop at SCH101.  Later stages are budgeted through
        # the existing replay-curve reports rather than collapsed into one
        # misleading nominal number.
        output = nominal * option.total_gain
        gains.append(GainSettingBudget(
            name=option.name,
            input_stage_gain_linear=option.total_gain,
            input_stage_gain_db=option.realised_total_db,
            nominal_5mv_output_rms_v=output,
            nominal_5mv_output_dbv=_db(output),
        ))

    margins = [
        MarginRecord(
            "MAR-001", "Worst validated cartridge input before SCH103 10 V RMS ceiling",
            0.005, 0.03581, "V RMS", 0.03581 / 0.005,
            _db(0.03581 / 0.005), EvidenceStatus.VALIDATED,
            "True-RIAA at 20 Hz is the limiting validated case; derived by report_sch103_electrical_closure.py.",
        ),
        MarginRecord(
            "MAR-002", "SCH104 unity-buffer severe-signal ceiling",
            3.21, SCH104_CEILING_RMS_V, "V RMS", SCH104_CEILING_RMS_V / 3.21,
            _db(SCH104_CEILING_RMS_V / 3.21), EvidenceStatus.VALIDATED,
            "Unity OPA1656 isolation buffer; severe input remains below conservative 10 V RMS design ceiling.",
        ),
        MarginRecord(
            "MAR-003", "THAT1646 severe differential-output design ceiling",
            3.21 * DIFFERENTIAL_GAIN_LINEAR, DRIVER_DESIGN_OUTPUT_RMS_V, "V RMS",
            DRIVER_DESIGN_OUTPUT_RMS_V / (3.21 * DIFFERENTIAL_GAIN_LINEAR),
            _db(DRIVER_DESIGN_OUTPUT_RMS_V / (3.21 * DIFFERENTIAL_GAIN_LINEAR)),
            EvidenceStatus.VALIDATED,
            "Frozen severe case is 6.42 V RMS differential against a 10 V RMS project design ceiling.",
        ),
        MarginRecord(
            "MAR-004", "THAT1646 severe differential-output datasheet capability",
            3.21 * DIFFERENTIAL_GAIN_LINEAR, DATASHEET_MAX_OUTPUT_RMS_V, "V RMS",
            DATASHEET_MAX_OUTPUT_RMS_V / (3.21 * DIFFERENTIAL_GAIN_LINEAR),
            _db(DATASHEET_MAX_OUTPUT_RMS_V / (3.21 * DIFFERENTIAL_GAIN_LINEAR)),
            EvidenceStatus.CALCULATED,
            "Datasheet capability is retained as an absolute limit; the lower project design ceiling governs acceptance.",
        ),
        MarginRecord(
            "MAR-005", "Audio PCB usable area above minimum architecture",
            190.0 * 125.0, 220.0 * 140.0, "mm^2",
            (220.0 * 140.0) / (190.0 * 125.0), None,
            EvidenceStatus.PROVISIONAL,
            "Preferred envelope provides strategic whitespace; final value awaits enclosure freeze.",
        ),
    ]

    criticality = [
        CriticalityRecord("CRIT-001", "SCH103 replay-EQ resistors and capacitors", Criticality.PERFORMANCE_DEFINING,
                          "No substitution without recalculation, tolerance review, and replay-curve regression.",
                          "Value, tolerance, dielectric, channel matching, and synthesis report."),
        CriticalityRecord("CRIT-002", "SCH101 gain-setting resistor networks", Criticality.PERFORMANCE_DEFINING,
                          "Substitute only as matched sets preserving calculated gain.",
                          "Gain report and channel-tracking audit."),
        CriticalityRecord("CRIT-003", "OPA1612/OPA1656/THAT1646 active devices", Criticality.PERFORMANCE_INFLUENCING,
                          "Approved-equivalent substitution requires noise, distortion, stability, supply, and pinout review.",
                          "Datasheet review plus bench stability and THD+N test."),
        CriticalityRecord("CRIT-004", "Local rail decouplers", Criticality.RELIABILITY_DEFINING,
                          "Equivalent reputable parts allowed if capacitance, voltage, ESR, package, and temperature ratings are met.",
                          "BOM inspection and placement-distance audit."),
        CriticalityRecord("CRIT-005", "Protection diodes, ferrites, XLRs and inter-box connector", Criticality.RELIABILITY_DEFINING,
                          "Approved equivalents allowed only with equal or better ratings and mechanical compatibility.",
                          "Rating and footprint review."),
        CriticalityRecord("CRIT-006", "General non-critical resistors, LEDs and fixings", Criticality.COMMODITY,
                          "Use lowest-cost reputable part meeting the frozen electrical/mechanical specification.",
                          "BOM and incoming inspection."),
        CriticalityRecord("CRIT-007", "Panel switches, enclosure, carrier plate and harness lengths", Criticality.MECHANICAL_DEPENDENT,
                          "Freeze only after enclosure and panel architecture close.",
                          "Mechanical model and assembly trial."),
    ]

    placement = [
        PlacementConstraint("PLC-001", "SCH101 cartridge input RF network", 8.0, 0,
                            "XLR harness connector, 100 ohm series resistors, CM and differential RF capacitors form one local cluster.",
                            "No control, output, or rail-spine route through the cluster.",
                            "Centroid-distance and region-crossing audit."),
        PlacementConstraint("PLC-002", "SCH101 gain and differential-converter feedback", 6.0, 0,
                            "Each gain/feedback resistor sits beside the associated amplifier pins.",
                            "No test-point branch or connector inside the feedback polygon.",
                            "Loop-area and via-count audit."),
        PlacementConstraint("PLC-003", "SCH103 active LF and recovery feedback loops", 6.0, 0,
                            "RF/RG and selected RC branches remain within their channel EQ island.",
                            "No left/right branch sharing; no unrelated trace under high-impedance nodes.",
                            "Channel-isolation, component-distance, and loop-area audit."),
        PlacementConstraint("PLC-004", "SCH107 rumble-filter frequency-setting network", 6.0, 0,
                            "Frequency-setting passives adjacent to OPA1656 pins.",
                            "No layer changes or control harness crossings.",
                            "Distance, via-count, and coupling audit."),
        PlacementConstraint("PLC-005", "SCH108 THAT1646 OUT/SNS loops", 5.0, 0,
                            "Each 10 uF common-mode capacitor directly adjacent to its OUT/SNS pin pair.",
                            "No via or branch in OUT-to-capacitor or SNS-to-capacitor conductors.",
                            "Direct-route and left/right symmetry audit."),
        PlacementConstraint("PLC-006", "Local IC decoupling", 4.0, 0,
                            "100 nF capacitor adjacent to each supply pin with shortest return to the reference plane.",
                            "No intervening connector, long neck, or shared signal segment.",
                            "Pin-to-capacitor distance and return-via audit."),
    ]

    return PerformanceBaseline(
        identifier="G3-PERF-002",
        revision="Rev A0",
        status="CALCULATED BASELINE — noise and distortion close after device/source models and bench correlation",
        nominal_cartridge_rms_v=nominal,
        gain_settings=gains,
        margins=margins,
        criticality=criticality,
        placement_constraints=placement,
        open_measurements=[
            "Grado 78C source resistance/inductance at representative audio frequencies.",
            "Integrated input-referred noise using final component values and bandwidth.",
            "Stage and end-to-end THD+N versus level and frequency.",
            "PSU ripple/noise at the PSU box and at the audio-board connector under load.",
            "Inter-box cable DC drop and chassis/0VA leakage behaviour.",
            "Channel tracking using fitted, measured EQ components.",
        ],
    )

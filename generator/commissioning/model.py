"""G3-004 staged commissioning and verification baseline.

This model deliberately separates calculated expectations from values that
must be established on Rev A hardware.  A stage may not proceed unless every
mandatory predecessor has passed and no stop condition remains active.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum

from generator.model.balanced_input import GAIN_SETTINGS
from generator.model.final_gain import GAIN_LINEAR as SCH104_GAIN
from generator.model.output_driver import DIFFERENTIAL_GAIN_LINEAR


class AcceptanceState(str, Enum):
    CALCULATED = "calculated"
    DESIGN_LIMIT = "design_limit"
    MEASUREMENT_REQUIRED = "measurement_required"
    VISUAL_INSPECTION = "visual_inspection"


@dataclass(frozen=True, slots=True)
class Measurement:
    identifier: str
    parameter: str
    injection_or_condition: str
    measurement_point: str
    expected: str
    tolerance_or_limit: str
    state: AcceptanceState
    instrument: str
    retain: str


@dataclass(frozen=True, slots=True)
class CommissioningStage:
    identifier: str
    title: str
    prerequisites: tuple[str, ...]
    safety_class: str
    configuration: tuple[str, ...]
    measurements: tuple[Measurement, ...]
    stop_conditions: tuple[str, ...]
    pass_evidence: tuple[str, ...]


@dataclass(slots=True)
class CommissioningBaseline:
    identifier: str
    revision: str
    status: str
    bench_assets: tuple[str, ...]
    global_rules: tuple[str, ...]
    stages: list[CommissioningStage] = field(default_factory=list)
    open_values: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _m(identifier, parameter, condition, point, expected, limit, state, instrument, retain):
    return Measurement(identifier, parameter, condition, point, expected, limit, state, instrument, retain)


def build_commissioning_baseline() -> CommissioningBaseline:
    default_gain = next(item for item in GAIN_SETTINGS if item.name == "DEFAULT")
    low_gain = next(item for item in GAIN_SETTINGS if item.name == "LOW")
    high_gain = next(item for item in GAIN_SETTINGS if item.name == "HIGH")
    stages = [
        CommissioningStage(
            "COM-00", "Document and configuration control", (), "administrative",
            ("Record PCB revision, BOM revision, fitted options and serial number.",
             "Confirm schematic Build ID and assembly drawing match the hardware."),
            (_m("M-0001", "Configuration identity", "Unpowered unit", "Build record", "All identifiers mutually consistent", "No mismatch permitted", AcceptanceState.VISUAL_INSPECTION, "Documentation review", "Signed configuration sheet"),),
            ("Any undocumented substitution in a performance-defining component.", "Any mismatch between fitted hardware and frozen baseline."),
            ("Signed configuration sheet", "High-resolution assembly photographs"),
        ),
        CommissioningStage(
            "COM-01", "Unpowered assembly inspection", ("COM-00",), "safe_unpowered",
            ("Disconnect PSU and all external cables.", "Remove active ICs from sockets where the assembly strategy permits."),
            (
                _m("M-0101", "0VA-to-CHASSIS relationship", "Unpowered", "Defined bond network", "Only the deliberate bond path is present", "No unintended low-resistance parallel bond", AcceptanceState.MEASUREMENT_REQUIRED, "DMM", "Resistance/diode-test record"),
                _m("M-0102", "+18V to 0VA resistance", "Unpowered", "Audio-box DC inlet", "No short circuit", "Investigate any unexpectedly low or unstable resistance", AcceptanceState.MEASUREMENT_REQUIRED, "DMM", "Resistance record"),
                _m("M-0103", "-18V to 0VA resistance", "Unpowered", "Audio-box DC inlet", "No short circuit", "Investigate any unexpectedly low or unstable resistance", AcceptanceState.MEASUREMENT_REQUIRED, "DMM", "Resistance record"),
                _m("M-0104", "Polarity and orientation", "Unpowered", "All polarised devices and IC pin-1 marks", "Matches assembly drawing", "No discrepancy permitted", AcceptanceState.VISUAL_INSPECTION, "Magnification and DMM", "Inspection checklist"),
            ),
            ("Short between either rail and 0VA or CHASSIS.", "Reversed diode, electrolytic or IC orientation.", "Unsoldered joint, bridge or damaged pad."),
            ("Completed inspection checklist", "Rail-resistance readings"),
        ),
        CommissioningStage(
            "COM-02", "External PSU standalone verification", ("COM-01",), "mains_hazard",
            ("Audio box disconnected.", "Use correct internal transformer primary configuration and fuse for local mains.", "Fit insulating covers to all exposed mains terminals."),
            (
                _m("M-0201", "Positive regulated rail", "PSU unloaded then representative dummy load", "PSU XLR +18V to 0VA", "+18.0 VDC nominal", "Initial acceptance target ±0.36 V; freeze after PSU characterisation", AcceptanceState.MEASUREMENT_REQUIRED, "DMM", "No-load and loaded readings"),
                _m("M-0202", "Negative regulated rail", "PSU unloaded then representative dummy load", "PSU XLR -18V to 0VA", "-18.0 VDC nominal", "Initial acceptance target ±0.36 V; freeze after PSU characterisation", AcceptanceState.MEASUREMENT_REQUIRED, "DMM", "No-load and loaded readings"),
                _m("M-0203", "Rail ripple/noise", "Representative load", "Each rail to 0VA", "Low and free of oscillation/spikes", "Numeric limit open pending PSU characterisation and measurement bandwidth definition", AcceptanceState.MEASUREMENT_REQUIRED, "Oscilloscope with short ground spring", "Bandwidth-limited captures"),
                _m("M-0204", "Protective-earth continuity", "Mains disconnected", "IEC earth pin to exposed PSU chassis", "Low-resistance permanent bond", "Final safety limit to follow applicable construction standard and test method", AcceptanceState.MEASUREMENT_REQUIRED, "Low-resistance meter/DMM", "Continuity record"),
            ),
            ("Incorrect rail polarity.", "Regulator oscillation, rising temperature or audible transformer distress.", "Protective-earth discontinuity.", "Fuse operation or abnormal inrush."),
            ("PSU voltage table", "Ripple captures", "Protective-earth test record"),
        ),
        CommissioningStage(
            "COM-03", "Audio-box current-limited first power", ("COM-02",), "energised_low_voltage",
            ("Mute engaged.", "No signal input.", "Use current-limited bench rails or series limiting arrangement for first energisation."),
            (
                _m("M-0301", "Audio-box +18V rail", "Current-limited power", "SCH106 rail test point", "+18 V nominal and stable", "Within PSU acceptance band", AcceptanceState.MEASUREMENT_REQUIRED, "DMM and oscilloscope", "Voltage and start-up capture"),
                _m("M-0302", "Audio-box -18V rail", "Current-limited power", "SCH106 rail test point", "-18 V nominal and stable", "Within PSU acceptance band", AcceptanceState.MEASUREMENT_REQUIRED, "DMM and oscilloscope", "Voltage and start-up capture"),
                _m("M-0303", "Quiescent current", "No input, mute engaged", "Both inter-box rail conductors", "Stable and repeatable", "Numeric acceptance limit to be frozen from calculated load inventory plus Rev A measurement", AcceptanceState.MEASUREMENT_REQUIRED, "Two DMMs or bench supply readback", "Per-rail current record"),
                _m("M-0304", "DC at balanced outputs", "No input, mute released only after rails stabilise", "Each output leg to 0VA and differential XLR output", "Near zero and stable", "Freeze numeric limit after first hardware data; investigate drift or rail-correlated offset", AcceptanceState.MEASUREMENT_REQUIRED, "DMM", "Four leg readings plus differential reading"),
            ),
            ("Current limit reached.", "Any IC or passive heating unexpectedly.", "Rail collapse, oscillation or excessive output DC."),
            ("First-power worksheet", "Thermal inspection record", "Start-up waveforms"),
        ),
        CommissioningStage(
            "COM-04", "SCH101 balanced-input gain and polarity", ("COM-03",), "energised_signal",
            ("Use low-level balanced generator injection through a protective series network.", "Select each internal gain option in turn."),
            tuple(_m(f"M-04{i+1:02d}", f"SCH101 {g.name} gain", "1 kHz balanced low-level input", "PRE_EQ channel test point", f"{g.total_gain:.4f} V/V ({g.realised_total_db:.3f} dB), non-inverting differential polarity", "Channel gain and tracking limits to be frozen after tolerance analysis", AcceptanceState.CALCULATED, "Signal generator and oscilloscope/DMM", "Left/right gain table") for i,g in enumerate((low_gain, default_gain, high_gain))),
            ("Unexpected phase reversal.", "Channel asymmetry inconsistent with fitted tolerances.", "Clipping, oscillation or common-mode instability."),
            ("Three-setting gain table", "Input/output waveform captures"),
        ),
        CommissioningStage(
            "COM-05", "SCH103 replay equalisation", ("COM-04",), "energised_signal",
            ("Use default SCH101 gain unless a lower level is required for headroom.", "Normalise each measured curve at 1 kHz.", "Verify both channels and every fitted selector position."),
            (
                _m("M-0501", "Replay curve tracking", "Log-spaced sweep for each bass/treble selection", "PRE_EQ and POST_EQ test points", "Matches generated replay-curve analysis", "Initial target ±0.20 dB from calculated curve, excluding generator/analyser uncertainty; final production limit to be reviewed", AcceptanceState.DESIGN_LIMIT, "Signal generator, oscilloscope or analyser", "CSV sweep and overlay plot"),
                _m("M-0502", "True-RIAA setting", "20 Hz to 20 kHz sweep", "POST_EQ", "Matches dedicated 3180/318 us plus 2121 Hz model", "Initial target ±0.20 dB from calculated curve", AcceptanceState.DESIGN_LIMIT, "Signal generator and analyser", "RIAA overlay plot"),
                _m("M-0503", "Channel tracking", "Identical sweep both channels", "POST_EQ_L versus POST_EQ_R", "Curves overlay", "Target ≤0.10 dB through 20 Hz–20 kHz, subject to fitted component matching", AcceptanceState.DESIGN_LIMIT, "Dual-channel oscilloscope/analyser", "Channel-difference plot"),
            ),
            ("Selector position produces discontinuity or unexpected gain jump.", "Sustained oscillation or clipping.", "Curve error indicates wrong component value or switch mapping."),
            ("All-curves CSV", "Model-versus-measurement plots", "Selector truth-table sign-off"),
        ),
        CommissioningStage(
            "COM-06", "SCH107/SCH104/SCH105 functional verification", ("COM-05",), "energised_signal",
            ("Verify rumble bypass and active positions.", "Verify SCH104 unity gain.", "Exercise stereo, dual-left, dual-right and L+R modes."),
            (
                _m("M-0601", "SCH104 gain", "1 kHz signal", "FILTERED to BUFFERED test points", f"{SCH104_GAIN:.3f} V/V", "Initial target ±0.05 dB", AcceptanceState.CALCULATED, "Oscilloscope/DMM", "Left/right gain readings"),
                _m("M-0602", "Mode truth table", "Independent L and R tones", "MODE_L and MODE_R", "Stereo, dual-L, dual-R and arithmetic-average L+R behave as frozen", "No incorrect crossfeed or gain state", AcceptanceState.MEASUREMENT_REQUIRED, "Two-channel generator or sequential injection and oscilloscope", "Mode matrix table"),
                _m("M-0603", "Rumble filter transfer", "Low-frequency sweep, bypass and active", "POST_EQ to FILTERED", "Matches frozen SCH107 model", "Initial target ±0.20 dB over verified sweep", AcceptanceState.DESIGN_LIMIT, "Signal generator and oscilloscope/analyser", "Transfer plot"),
            ),
            ("Incorrect mode routing.", "Non-unity SCH104 gain.", "Filter bypass does not restore the direct path."),
            ("Mode matrix worksheet", "Filter overlay", "Unity-buffer readings"),
        ),
        CommissioningStage(
            "COM-07", "SCH108 mute and balanced output", ("COM-06",), "energised_signal",
            ("Use representative line-level input.", "Test mute switching with downstream load disconnected first."),
            (
                _m("M-0701", "Differential output gain", "1 kHz at MODE input", "Balanced XLR output", f"{DIFFERENTIAL_GAIN_LINEAR:.3f} V/V differential (+6.021 dB)", "Initial target ±0.10 dB and left/right tracking review", AcceptanceState.CALCULATED, "Oscilloscope/DMM", "Gain table"),
                _m("M-0702", "Mute attenuation and transient", "Steady 1 kHz then operate mute", "Balanced output", "Signal suppressed without damaging transient", "Quantitative attenuation and transient limits to be frozen from Rev A data and downstream tolerance", AcceptanceState.MEASUREMENT_REQUIRED, "Oscilloscope", "Time-domain capture"),
                _m("M-0703", "Output symmetry", "Balanced output into representative load", "Each output leg to 0VA", "Equal and opposite legs", "Initial target ≤0.10 dB amplitude mismatch and visually opposite polarity", AcceptanceState.DESIGN_LIMIT, "Two-channel oscilloscope", "Dual-leg capture"),
            ),
            ("Large DC transient or oscillation.", "Output leg asymmetry outside tolerance.", "Protection component heating."),
            ("Balanced-output worksheet", "Mute transient capture", "Loaded-output capture"),
        ),
        CommissioningStage(
            "COM-08", "End-to-end performance characterisation", ("COM-07",), "energised_precision",
            ("Use final PSU and inter-box cable.", "Close unused inputs with representative cartridge source impedance.", "Define analyser bandwidth and weighting on every result."),
            (
                _m("M-0801", "End-to-end noise", "Inputs terminated with representative cartridge model", "Balanced outputs", "No hum spur or broadband anomaly; establish baseline", "Numeric limit remains open until cartridge impedance and measurement bandwidth are frozen", AcceptanceState.MEASUREMENT_REQUIRED, "HP distortion analyser and oscilloscope FFT as cross-check", "Spectrum and RMS noise record"),
                _m("M-0802", "THD+N", "Representative 1 kHz levels and selected curves", "Balanced outputs", "Monotonic, low and free of instability", "Freeze acceptance limit from Rev A characterisation below clipping", AcceptanceState.MEASUREMENT_REQUIRED, "HP distortion analyser", "THD+N versus level table"),
                _m("M-0803", "Overload behaviour", "Increase input until defined output or internal clipping", "Critical interstage test points and balanced output", "Consistent with validated headroom budget", "Worst-case input limit expected above 35 mV RMS in validated true-RIAA/20 Hz case", AcceptanceState.DESIGN_LIMIT, "Generator and oscilloscope", "Clipping map"),
                _m("M-0804", "Inter-box susceptibility", "Normal operation while moving/separating PSU within intended arrangement", "Balanced output noise", "No meaningful hum-field or cable-position sensitivity", "Qualitative first pass; quantify if any change is observable", AcceptanceState.MEASUREMENT_REQUIRED, "HP analyser/oscilloscope", "Placement sensitivity notes"),
            ),
            ("Unexpected hum, oscillation or clipping below budget.", "Performance changes materially with switch position beyond intended transfer function.", "Thermal drift or rail instability."),
            ("Noise spectra", "THD+N table", "Headroom map", "Final measured baseline JSON/CSV"),
        ),
        CommissioningStage(
            "COM-09", "Controlled listening and release", ("COM-08",), "operational",
            ("Complete objective acceptance first.", "Use known records and reference replay settings.", "Begin with downstream volume low and mute engaged."),
            (
                _m("M-0901", "Operational behaviour", "Normal user operation", "Complete instrument", "Controls intuitive, silent and repeatable", "No unexpected thump, intermittent contact or mechanical interference", AcceptanceState.MEASUREMENT_REQUIRED, "Listening system and observation", "Operational checklist"),
                _m("M-0902", "Subjective comparison", "Known shellac and optional RIAA record", "Listening position", "No unexplained channel imbalance, hum or tonal anomaly", "Subjective evidence cannot waive failed objective tests", AcceptanceState.MEASUREMENT_REQUIRED, "Reference playback system", "Listening notes"),
            ),
            ("Any objective acceptance test remains open or failed.", "Intermittent control, connector or harness behaviour."),
            ("Signed Rev A release record", "Issue list for Revision B"),
        ),
    ]
    return CommissioningBaseline(
        identifier="G3-COM-004", revision="Rev A0",
        status="PROVISIONAL — measurement-derived limits will be frozen during Rev A characterisation",
        bench_assets=(
            "Lavolta BPS305 current-limited bench supply",
            "Siglent 100 MHz four-channel oscilloscope",
            "Tektronix 500 MHz oscilloscope",
            "RS Pro signal generator",
            "HP distortion analyser",
            "True-RMS DMM(s)",
        ),
        global_rules=(
            "Never bypass a failed or incomplete mandatory stage.",
            "Record instrument, bandwidth, weighting, probe configuration and load for every quantitative result.",
            "Use current limiting for first energisation of each newly populated assembly state.",
            "Subjective listening cannot waive an objective failure.",
            "Any component substitution after acceptance requires affected stages to be repeated.",
            "Mains work is performed only with suitable competence, insulation and protective-earth verification.",
        ),
        stages=stages,
        open_values=[
            "Final PSU ripple/noise acceptance bandwidth and numeric limit.",
            "Calculated and measured per-rail quiescent-current limits.",
            "Representative Grado 78C source impedance model versus frequency.",
            "Final output-DC and mute-transient limits.",
            "Production noise, THD+N and channel-tracking acceptance limits after Rev A characterisation.",
        ],
    )


def validate_commissioning_baseline(model: CommissioningBaseline) -> None:
    ids = [stage.identifier for stage in model.stages]
    assert len(ids) == len(set(ids))
    known: set[str] = set()
    measurement_ids: set[str] = set()
    for stage in model.stages:
        assert all(parent in known for parent in stage.prerequisites)
        assert stage.measurements
        assert stage.stop_conditions
        assert stage.pass_evidence
        for measurement in stage.measurements:
            assert measurement.identifier not in measurement_ids
            measurement_ids.add(measurement.identifier)
            assert measurement.expected
            assert measurement.tolerance_or_limit
            assert measurement.instrument
        known.add(stage.identifier)
    assert ids[0] == "COM-00"
    assert ids[-1] == "COM-09"
    assert len(model.stages) == 10

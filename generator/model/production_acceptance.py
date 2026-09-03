"""AE-029 production commissioning acceptance model.

This module centralises Shellac's production acceptance criteria. It does not
replace the block models; it imports them and classifies each requirement by
evidence type.

Evidence states:
- ANALYTICALLY_CLOSED: deterministic model/regression demonstrates requirement.
- VERIFY_ON_PROTOTYPE: model defines acceptance target but physical measurement required.
- OPEN_DESIGN: design information still missing; production release blocked.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import log10

from .balanced_input import GAIN_SETTINGS
from .mode_matrix import mono_average_error_db
from .production_cmrr import production_cmrr_matrix
from .production_signal_chain_closure import production_closure
from .rumble_filter import magnitude_db as rumble_db
from .signal_chain_analysis import riaa_combination, signal_point
from .replay_curve_analysis import analyse_all_targets


class Evidence(str, Enum):
    ANALYTICALLY_CLOSED = "ANALYTICALLY_CLOSED"
    VERIFY_ON_PROTOTYPE = "VERIFY_ON_PROTOTYPE"
    OPEN_DESIGN = "OPEN_DESIGN"


@dataclass(frozen=True, slots=True)
class AcceptanceItem:
    identifier: str
    subsystem: str
    requirement: str
    acceptance: str
    evidence: Evidence
    method: str
    release_blocker: bool


NOMINAL_CARTRIDGE_RMS_V = 0.005
OUTPUT_DESIGN_CEILING_RMS_V = 10.0
OUTPUT_DC_PROVISIONAL_MAX_V = 0.025
STARTUP_SETTLING_MIN_S = 2.0

GAIN_ERROR_MAX_DB = 0.10
CHANNEL_GAIN_MATCH_PROVISIONAL_DB = 0.10
RIAA_PROVISIONAL_ERROR_DB = 0.20
HISTORICAL_CURVE_PROVISIONAL_ERROR_DB = 0.50
OUTPUT_BALANCE_PROVISIONAL_DB = 0.10

CMRR_LOW_MID_MIN_DB = 70.0
CMRR_20KHZ_MIN_DB = 60.0
NOISE_PROVISIONAL_MAX_RMS_V = 0.000150


def _gain_acceptance_items():
    items = []
    for setting in GAIN_SETTINGS:
        items.append(AcceptanceItem(
            f"GAIN-{setting.name}",
            "SCH101",
            f"{setting.name} total input-stage gain",
            f"{setting.target_total_db:.1f} dB nominal; model error <= {GAIN_ERROR_MAX_DB:.2f} dB",
            Evidence.ANALYTICALLY_CLOSED,
            "Calculate from implemented feedback values; verify channel-to-channel on prototype.",
            False,
        ))
    return items


def acceptance_items():
    x = production_closure()
    cmrr = production_cmrr_matrix()
    curves = analyse_all_targets()
    riaa = next(c for c in curves if c.target.identifier == "RIAA")

    items = list(_gain_acceptance_items())
    items += [
        AcceptanceItem(
            "LEVEL-RIAA-1K",
            "End-to-end",
            "Nominal balanced output at 1 kHz, DEFAULT, 5 mV RMS input, True RIAA",
            "0.62 to 0.67 V RMS differential",
            Evidence.ANALYTICALLY_CLOSED,
            "Inject balanced cartridge-equivalent signal; measure XLR differential RMS.",
            False,
        ),
        AcceptanceItem(
            "HEADROOM-DEFAULT",
            "End-to-end",
            "Worst-case wanted-band headroom at DEFAULT gain",
            f">=4.4 dB analytical margin to {OUTPUT_DESIGN_CEILING_RMS_V:.0f} V RMS differential ceiling",
            Evidence.ANALYTICALLY_CLOSED,
            "Dense model sweep; verify overload onset on prototype.",
            False,
        ),
        AcceptanceItem(
            "HEADROOM-HIGH",
            "End-to-end",
            "Worst-case wanted-band headroom at HIGH gain",
            ">=0.45 dB analytical margin at 5 mV reference; HIGH reserved for lower-output cartridges",
            Evidence.ANALYTICALLY_CLOSED,
            "Dense model sweep; verify overload onset on prototype.",
            False,
        ),
        AcceptanceItem(
            "RIAA-SHAPE",
            "SCH103",
            "True-RIAA normalised response",
            f"Prototype target <= +/-{RIAA_PROVISIONAL_ERROR_DB:.2f} dB, 20 Hz to 20 kHz",
            Evidence.VERIFY_ON_PROTOTYPE,
            f"Analytical nominal worst error {abs(riaa.worst_error_db):.4f} dB; sweep and normalise at 1 kHz.",
            True,
        ),
        AcceptanceItem(
            "HIST-EQ-SHAPE",
            "SCH103",
            "Historical 78 replay positions",
            f"Prototype target <= +/-{HISTORICAL_CURVE_PROVISIONAL_ERROR_DB:.2f} dB vs implemented nominal target",
            Evidence.VERIFY_ON_PROTOTYPE,
            "Sweep each Bass/Treble switch family position; normalise at 1 kHz.",
            True,
        ),
        AcceptanceItem(
            "RUMBLE-20",
            "SCH107",
            "Rumble FILTER wanted-band loss at 20 Hz",
            "> -0.50 dB",
            Evidence.ANALYTICALLY_CLOSED,
            f"Model = {rumble_db(20.0):.3f} dB; verify prototype.",
            False,
        ),
        AcceptanceItem(
            "RUMBLE-10",
            "SCH107",
            "Rumble FILTER attenuation at 10 Hz",
            "< -14 dB",
            Evidence.ANALYTICALLY_CLOSED,
            f"Model = {rumble_db(10.0):.2f} dB; verify prototype.",
            False,
        ),
        AcceptanceItem(
            "RUMBLE-5",
            "SCH107",
            "Rumble FILTER attenuation at 5 Hz",
            "< -38 dB",
            Evidence.ANALYTICALLY_CLOSED,
            f"Model = {rumble_db(5.0):.2f} dB; verify prototype.",
            False,
        ),
        AcceptanceItem(
            "MONO-AVERAGE",
            "SCH105",
            "Equal-input L+R mode gain",
            "Average (L+R)/2; magnitude error <0.03 dB",
            Evidence.ANALYTICALLY_CLOSED,
            f"Model error = {mono_average_error_db():.4f} dB.",
            False,
        ),
        AcceptanceItem(
            "CHANNEL-MODES",
            "SCH105",
            "Stereo / Dual-L / Dual-R / Mono routing truth table",
            "All four states must match controlled truth table; no permanent stereo cross-link",
            Evidence.VERIFY_ON_PROTOTYPE,
            "Inject L-only then R-only signal and record both outputs in every switch state.",
            True,
        ),
        AcceptanceItem(
            "CMRR-20-1K",
            "SCH101",
            "Input common-mode rejection from 20 Hz through 1 kHz",
            f">={CMRR_LOW_MID_MIN_DB:.0f} dB for LOW/DEFAULT/HIGH",
            Evidence.VERIFY_ON_PROTOTYPE,
            f"Analytical corner minimum = {min(p.worst_case_db for p in cmrr if p.frequency_hz <= 1000):.1f} dB.",
            True,
        ),
        AcceptanceItem(
            "CMRR-20K",
            "SCH101",
            "Input common-mode rejection at 20 kHz",
            f">={CMRR_20KHZ_MIN_DB:.0f} dB for LOW/DEFAULT/HIGH",
            Evidence.VERIFY_ON_PROTOTYPE,
            f"Analytical corner minimum = {min(p.worst_case_db for p in cmrr if p.frequency_hz >= 20000):.1f} dB.",
            True,
        ),
        AcceptanceItem(
            "NOISE-RIAA",
            "End-to-end",
            "Complete-RIAA electronics noise, DEFAULT, inputs terminated",
            f"Provisional <= {NOISE_PROVISIONAL_MAX_RMS_V*1e6:.0f} uV RMS differential, 20 Hz-20 kHz",
            Evidence.VERIFY_ON_PROTOTYPE,
            f"First-order model ~{x.electronics_noise_rms_v*1e6:.0f} uV RMS.",
            True,
        ),
        AcceptanceItem(
            "OUTPUT-DC",
            "SCH108/XLR",
            "Balanced differential output DC after >=2 s settling",
            f"Provisional <= {OUTPUT_DC_PROVISIONAL_MAX_V*1000:.0f} mV",
            Evidence.VERIFY_ON_PROTOTYPE,
            f"Conservative blocked analytical estimate ~{x.conservative_blocked_xlr_dc_v*1000:.0f} mV.",
            True,
        ),
        AcceptanceItem(
            "STARTUP",
            "Controls/DC",
            "Power-up settling with MUTE engaged",
            f"No release before {STARTUP_SETTLING_MIN_S:.1f} s; no damaging/transient overload",
            Evidence.VERIFY_ON_PROTOTYPE,
            "Oscilloscope balanced output during cold/warm starts; repeat both channels.",
            True,
        ),
        AcceptanceItem(
            "POWERDOWN",
            "Controls/DC",
            "Power-down transient with MUTE engaged",
            "No damaging output transient",
            Evidence.VERIFY_ON_PROTOTYPE,
            "Scope balanced output while removing power after engaging MUTE.",
            True,
        ),
        AcceptanceItem(
            "SWITCH-TRANSIENTS",
            "Controls",
            "Rumble / channel-mode / EQ switching",
            "No latch-up, sustained oscillation or unsafe output transient; quantify audible click/pop",
            Evidence.VERIFY_ON_PROTOTYPE,
            "Scope peak output transient during repeated switching under representative signal/no-signal cases.",
            True,
        ),
        AcceptanceItem(
            "CHANNEL-MATCH",
            "End-to-end",
            "L/R gain matching at 1 kHz",
            f"Provisional <= {CHANNEL_GAIN_MATCH_PROVISIONAL_DB:.2f} dB",
            Evidence.VERIFY_ON_PROTOTYPE,
            "Common generator source split to both inputs; compare differential outputs.",
            True,
        ),
        AcceptanceItem(
            "OUTPUT-BALANCE",
            "SCH108",
            "Balanced-output leg symmetry at 1 kHz",
            f"Provisional <= {OUTPUT_BALANCE_PROVISIONAL_DB:.2f} dB leg-amplitude mismatch",
            Evidence.VERIFY_ON_PROTOTYPE,
            "Measure XLR hot/cold leg amplitudes to 0VA and differential output.",
            True,
        ),
        AcceptanceItem(
            "OVERLOAD",
            "End-to-end",
            "Actual overload/clipping onset",
            "Prototype measured limit must not be below analytical design envelope",
            Evidence.VERIFY_ON_PROTOTYPE,
            "Increase sinusoidal input at representative LF/1k/HF points and each gain setting.",
            True,
        ),
        AcceptanceItem(
            "ROTARY-MECHANICS",
            "Controls",
            "Production rotary switch geometry/contact MPN",
            "AE-028 sample gate + Lorlin exact gold-contact MPN confirmation",
            Evidence.OPEN_DESIGN,
            "Close AE-027/AE-028 before BOM/PCB/panel freeze.",
            True,
        ),
    ]
    return tuple(items)


def counts_by_evidence():
    items = acceptance_items()
    return {state: sum(i.evidence is state for i in items) for state in Evidence}


def release_blockers():
    return tuple(i for i in acceptance_items() if i.release_blocker)


def validate_acceptance_matrix():
    items = acceptance_items()
    assert len({i.identifier for i in items}) == len(items)
    assert len(items) >= 20
    assert any(i.evidence is Evidence.ANALYTICALLY_CLOSED for i in items)
    assert any(i.evidence is Evidence.VERIFY_ON_PROTOTYPE for i in items)
    assert any(i.evidence is Evidence.OPEN_DESIGN for i in items)
    assert all(i.acceptance and i.method for i in items)

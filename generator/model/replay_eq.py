"""Controlled replay-equalisation data for SCH103.

This module separates three categories of engineering data:

1. ESP Project 91 source selections, retained unchanged for traceability.
2. Full P06/P91 active pole-zero networks, calculated with the complete
   feedback topology RF || (RS + 1/sC).
3. A dedicated true-RIAA active network, independently solved for the
   3180 us and 318 us time constants.

The superseded 14.3 kohm simple-RC bass model is intentionally absent.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

SOURCE_URL = "https://sound-au.com/project91.htm"
SOURCE_P06_URL = "https://sound-au.com/project06.htm"
SOURCE_RETRIEVED = "2026-07-14"


class EqValueStatus(str, Enum):
    SOURCE_REFERENCE = "source_reference"
    SYNTHESIS_PENDING = "synthesis_pending"
    TRANSFER_FUNCTION_VALIDATED = "transfer_function_validated"
    CURVE_NETWORKS_OPTIMISED = "curve_networks_optimised"
    ELECTRICALLY_CLOSED = "electrically_closed"
    FINALISED = "finalised"


# Complete active-network mathematics and the dedicated RIAA branch are now
# validated. Historical 78-position optimisation and whole-stage gain/overload
# closure remain pending, so SCH103 is not yet finalised.
DESIGN_STATUS = EqValueStatus.ELECTRICALLY_CLOSED

P06_RF_OHM = 100_000.0
P06_RS_OHM = 10_000.0
P06_RG_OHM = 2_700.0
TREBLE_FIXED_RESISTANCE_OHM = 750.0

# SCH103 fixed recovery stage following the active LF and passive HF networks.
RECOVERY_RG_OHM = 10_000.0
RECOVERY_RF_OHM = 11_000.0
RECOVERY_GAIN = 1.0 + RECOVERY_RF_OHM / RECOVERY_RG_OHM
OPA1612_DESIGN_OUTPUT_RMS_V = 10.0
from .balanced_input import default_setting

SCH101_DEFAULT_GAIN = default_setting().total_gain
NOMINAL_CARTRIDGE_RMS_V = 0.005



@dataclass(frozen=True, slots=True)
class BassNetwork:
    position: int
    name: str
    source_capacitance_nf: float | None
    switch_condition: str
    rf_ohm: float | None = None
    rs_ohm: float | None = None
    rg_ohm: float | None = None
    capacitor_parts_nf: tuple[float, ...] = ()
    target_pole_hz: float | None = None
    target_zero_hz: float | None = None
    notes: str = ""

    @property
    def capacitance_nf(self) -> float | None:
        return sum(self.capacitor_parts_nf) if self.capacitor_parts_nf else None


@dataclass(frozen=True, slots=True)
class TrebleNetwork:
    position: int
    name: str
    target_hz: float | None
    source_capacitance_nf: float | None
    switch_condition: str
    resistor_ohm: float | None = None
    capacitor_parts_nf: tuple[float, ...] = ()
    notes: str = ""

    @property
    def capacitance_nf(self) -> float | None:
        return sum(self.capacitor_parts_nf) if self.capacitor_parts_nf else None


# Original P91 networks are preserved as source evidence.
P91_SOURCE_BASS_NETWORKS: tuple[BassNetwork, ...] = (
    BassNetwork(1, "FLAT", None, "SHORT", notes="Active bass branch bypassed."),
    BassNetwork(2, "200 Hz SOURCE", 56.0, "NETWORK", P06_RF_OHM, P06_RS_OHM, P06_RG_OHM, (56.0,), notes="Published P91 source network."),
    BassNetwork(3, "400 Hz SOURCE", 27.0, "NETWORK", P06_RF_OHM, P06_RS_OHM, P06_RG_OHM, (27.0,), notes="Published P91 source network."),
    BassNetwork(4, "500 Hz SOURCE", 22.0, "NETWORK", P06_RF_OHM, P06_RS_OHM, P06_RG_OHM, (22.0,), notes="Published P91 source network; not true RIAA."),
)

# Final Shellac historical networks. Each switch position selects a complete
# RS+C branch, allowing the nominal 20 Hz lower break to remain fixed while
# selecting 200, 400 or 500 Hz upper turnover.
BASS_NETWORKS: tuple[BassNetwork, ...] = (
    BassNetwork(1, "FLAT", None, "SHORT", notes="Active bass branch bypassed."),
    BassNetwork(2, "200 Hz", 56.0, "NETWORK", P06_RF_OHM, 8_200.0, P06_RG_OHM, (68.0, 5.6), 20.0, 200.0, "Optimised complete branch: 8.20k, 68n+5.6n."),
    BassNetwork(3, "400 Hz", 27.0, "NETWORK", P06_RF_OHM, 2_490.0, P06_RG_OHM, (68.0, 9.1, 0.56), 20.0, 400.0, "Optimised complete branch: 2.49k, 68n+9.1n+560p."),
    BassNetwork(4, "500 Hz 78", 22.0, "NETWORK", P06_RF_OHM, 1_430.0, P06_RG_OHM, (68.0, 10.0, 0.47), 20.0, 500.0, "Optimised complete branch: 1.43k, 68n+10n+470p; historical 78, not RIAA."),
)

# Dedicated true-RIAA branch. 8.20 kohm and 27 nF + 2.4 nF are practical
# preferred values close to the exact 8.190 kohm / 29.392 nF solution.
RIAA_BASS_NETWORK = BassNetwork(
    position=5,
    name="TRUE RIAA 3180/318 us",
    source_capacitance_nf=None,
    switch_condition="NETWORK",
    rf_ohm=P06_RF_OHM,
    rs_ohm=8_200.0,
    rg_ohm=P06_RG_OHM,
    capacitor_parts_nf=(27.0, 2.4),
    target_pole_hz=50.05,
    target_zero_hz=500.5,
    notes="Dedicated resistor-and-capacitor branch; must be paired with 2121 Hz treble selection.",
)

TREBLE_NETWORKS: tuple[TrebleNetwork, ...] = (
    TrebleNetwork(1, "FLAT", None, None, "OPEN", notes="Treble capacitor disconnected."),
    TrebleNetwork(2, "1600 Hz", 1600.0, 120.0, "CAPACITOR", TREBLE_FIXED_RESISTANCE_OHM, (120.0, 12.0)),
    TrebleNetwork(3, "2121 Hz RIAA", 2121.0, 82.0, "CAPACITOR", TREBLE_FIXED_RESISTANCE_OHM, (100.0,), notes="Updated P06 recommendation."),
    TrebleNetwork(4, "3400 Hz", 3400.0, 56.0, "CAPACITOR", TREBLE_FIXED_RESISTANCE_OHM, (56.0, 6.2)),
    TrebleNetwork(5, "5800 Hz", 5800.0, 33.0, "CAPACITOR", TREBLE_FIXED_RESISTANCE_OHM, (33.0, 3.6)),
)

# Compatibility aliases for existing builder/model code.
BASS_SELECTIONS = BASS_NETWORKS
TREBLE_SELECTIONS = TREBLE_NETWORKS


def validate_replay_eq_data() -> None:
    assert DESIGN_STATUS is EqValueStatus.ELECTRICALLY_CLOSED
    assert len(BASS_NETWORKS) == 4
    assert len(TREBLE_NETWORKS) == 5
    assert BASS_NETWORKS[0].switch_condition == "SHORT"
    assert TREBLE_NETWORKS[0].switch_condition == "OPEN"
    assert all(item.capacitance_nf is not None for item in BASS_NETWORKS[1:])
    assert all(item.target_pole_hz == 20.0 for item in BASS_NETWORKS[1:])
    assert RIAA_BASS_NETWORK.rs_ohm == 8_200.0
    assert RIAA_BASS_NETWORK.capacitance_nf == 29.4
    assert all(item.capacitance_nf is not None for item in TREBLE_NETWORKS[1:])

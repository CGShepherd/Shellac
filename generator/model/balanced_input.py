"""AE-010 SCH101 selectable-gain closure.

SCH101 retains the existing architecture:
- matched OPA1656 non-inverting gain stage on each balanced leg;
- fixed 3.48x precision differential converter per channel.

The per-leg gains are selected so the complete SCH101 channel gain is
approximately 14, 18 or 22 dB.  The 18 dB setting is the default used by all
downstream headroom calculations.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from math import log10

DIFF_CONVERTER_GAIN = 3.48
GAIN_RG_OHM = 10_000.0
GAIN_BASE_RF_OHM = 4_420.0
GAIN_DEFAULT_ADD_OHM = 8_280.0
GAIN_HIGH_ADD_OHM = 21_680.0
DEFAULT_GAIN_DB = 18.0
SELECTOR = "8-way internal DIP; two setting bits repeated across four matched gain legs"


class BalancedInputStatus(str, Enum):
    ELECTRICALLY_CLOSED = "electrically_closed"


DESIGN_STATUS = BalancedInputStatus.ELECTRICALLY_CLOSED


@dataclass(frozen=True, slots=True)
class GainSetting:
    name: str
    target_total_db: float
    rf_ohm: float
    dip_pattern: str

    @property
    def per_leg_gain(self) -> float:
        return 1.0 + self.rf_ohm / GAIN_RG_OHM

    @property
    def total_gain(self) -> float:
        return self.per_leg_gain * DIFF_CONVERTER_GAIN

    @property
    def realised_total_db(self) -> float:
        return 20.0 * log10(self.total_gain)

    @property
    def error_db(self) -> float:
        return self.realised_total_db - self.target_total_db


GAIN_SETTINGS: tuple[GainSetting, ...] = (
    GainSetting("LOW", 14.0, 4_420.0, "00"),
    GainSetting("DEFAULT", 18.0, 12_700.0, "01"),
    GainSetting("HIGH", 22.0, 26_100.0, "10"),
)


def default_setting() -> GainSetting:
    return next(item for item in GAIN_SETTINGS if item.name == "DEFAULT")


def validate_balanced_input() -> None:
    assert DESIGN_STATUS is BalancedInputStatus.ELECTRICALLY_CLOSED
    assert len(GAIN_SETTINGS) == 3
    assert abs(default_setting().realised_total_db - DEFAULT_GAIN_DB) < 0.06
    assert all(abs(item.error_db) < 0.08 for item in GAIN_SETTINGS)
    assert len({item.dip_pattern for item in GAIN_SETTINGS}) == 3
    assert GAIN_BASE_RF_OHM + GAIN_DEFAULT_ADD_OHM == GAIN_SETTINGS[1].rf_ohm
    assert GAIN_BASE_RF_OHM + GAIN_HIGH_ADD_OHM == GAIN_SETTINGS[2].rf_ohm

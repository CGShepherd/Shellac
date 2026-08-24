"""G3-025 architecture contract for the optional 3180 us RIAA pole."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import pi

from .replay_eq_transfer import active_network_response

TAU_3180_S = 3180e-6
TAU_318_S = 318e-6
TAU_75_S = 75e-6

RIAA_3180_HZ = 1.0 / (2.0 * pi * TAU_3180_S)
RIAA_318_HZ = 1.0 / (2.0 * pi * TAU_318_S)
RIAA_75_HZ = 1.0 / (2.0 * pi * TAU_75_S)

CURRENT_RF_OHM = 100_000.0
CURRENT_RS_OHM = 8_200.0
CURRENT_RG_OHM = 2_700.0
CURRENT_C_F = 29.4e-9


class OptionalPoleStatus(str, Enum):
    CONTRADICTION_RECORDED = "contradiction_recorded"
    ARCHITECTURE_SELECTED = "architecture_selected"
    CIRCUIT_REALISATION_FROZEN = "circuit_realisation_frozen"


STATUS = OptionalPoleStatus.CIRCUIT_REALISATION_FROZEN


@dataclass(frozen=True, slots=True)
class OptionalPoleContract:
    identifier: str
    channels: int
    user_access: str
    on_state: str
    bypass_state: str
    invariant_terms: tuple[str, ...]
    minimum_linked_switch_paths: int
    exact_switch_mpn_frozen: bool
    exact_rc_realisation_frozen: bool


CONTRACT = OptionalPoleContract(
    identifier="RIAA-OPT-3180",
    channels=2,
    user_access="internal/service configuration",
    on_state="insert dedicated 3180 us first-order section in both channels",
    bypass_state="straight-through around dedicated 3180 us section in both channels",
    invariant_terms=("318 us zero", "75 us pole"),
    minimum_linked_switch_paths=2,
    exact_switch_mpn_frozen=True,
    exact_rc_realisation_frozen=True,
)


def riaa_core_transfer(s: complex) -> complex:
    return (1.0 + s * TAU_318_S) / (1.0 + s * TAU_75_S)


def optional_3180_transfer(s: complex) -> complex:
    return 1.0 / (1.0 + s * TAU_3180_S)


def architecture_transfer(s: complex, *, pole_enabled: bool) -> complex:
    core = riaa_core_transfer(s)
    return core * optional_3180_transfer(s) if pole_enabled else core


def canonical_riaa_transfer(s: complex) -> complex:
    return (1.0 + s * TAU_318_S) / (
        (1.0 + s * TAU_3180_S) * (1.0 + s * TAU_75_S)
    )


def current_single_rc_breaks_hz() -> tuple[float, float]:
    response = active_network_response(
        CURRENT_RF_OHM,
        CURRENT_RS_OHM,
        CURRENT_RG_OHM,
        CURRENT_C_F,
    )
    return response.pole_hz, response.zero_hz


def single_rc_break_ratio() -> float:
    pole, zero = current_single_rc_breaks_hz()
    return zero / pole


def scaled_single_rc_breaks_hz(capacitance_f: float) -> tuple[float, float]:
    response = active_network_response(
        CURRENT_RF_OHM,
        CURRENT_RS_OHM,
        CURRENT_RG_OHM,
        capacitance_f,
    )
    return response.pole_hz, response.zero_hz


def validate_optional_pole_contract() -> None:
    assert STATUS is OptionalPoleStatus.CIRCUIT_REALISATION_FROZEN
    assert CONTRACT.channels == 2
    assert CONTRACT.minimum_linked_switch_paths == 2
    assert CONTRACT.exact_switch_mpn_frozen
    assert CONTRACT.exact_rc_realisation_frozen
    pole, zero = current_single_rc_breaks_hz()
    assert abs(pole - 50.0) < 0.2
    assert abs(zero - 500.0) < 2.0

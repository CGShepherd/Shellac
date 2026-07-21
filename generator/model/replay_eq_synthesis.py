"""Controlled synthesis tables built on the AE-002 transfer-function engine."""

from __future__ import annotations

from dataclasses import dataclass
from math import pi

from .replay_eq import (
    BASS_NETWORKS,
    P06_RF_OHM,
    P06_RG_OHM,
    P91_SOURCE_BASS_NETWORKS,
    RIAA_BASS_NETWORK,
    TREBLE_NETWORKS,
)
from .replay_eq_transfer import active_network_response, solve_capacitance_for_pole, solve_series_resistor_for_break_ratio


@dataclass(frozen=True, slots=True)
class ActiveSynthesisRow:
    selection: str
    rf_ohm: float
    rs_ohm: float
    rg_ohm: float
    capacitance_nf: float
    pole_hz: float
    zero_hz: float
    shelf_db: float
    target_pole_hz: float | None = None
    target_zero_hz: float | None = None

    @property
    def pole_error_percent(self) -> float | None:
        if self.target_pole_hz is None:
            return None
        return (self.pole_hz / self.target_pole_hz - 1.0) * 100.0

    @property
    def zero_error_percent(self) -> float | None:
        if self.target_zero_hz is None:
            return None
        return (self.zero_hz / self.target_zero_hz - 1.0) * 100.0


def active_synthesis_rows(*, source: bool = False) -> tuple[ActiveSynthesisRow, ...]:
    rows: list[ActiveSynthesisRow] = []
    networks = P91_SOURCE_BASS_NETWORKS[1:] if source else BASS_NETWORKS[1:] + (RIAA_BASS_NETWORK,)
    for item in networks:
        response = active_network_response(item.rf_ohm, item.rs_ohm, item.rg_ohm, item.capacitance_nf * 1e-9)
        rows.append(ActiveSynthesisRow(
            item.name, item.rf_ohm, item.rs_ohm, item.rg_ohm, item.capacitance_nf,
            response.pole_hz, response.zero_hz, response.shelf_db,
            item.target_pole_hz, item.target_zero_hz,
        ))
    return tuple(rows)


def exact_riaa_solution() -> tuple[float, float]:
    ratio = 500.5 / 50.05
    rs = solve_series_resistor_for_break_ratio(P06_RF_OHM, P06_RG_OHM, ratio)
    capacitance_f = solve_capacitance_for_pole(P06_RF_OHM, rs, 50.05)
    return rs, capacitance_f * 1e9


def passive_treble_frequency_hz(resistance_ohm: float, capacitance_nf: float) -> float:
    if resistance_ohm <= 0 or capacitance_nf <= 0:
        raise ValueError("Resistance and capacitance must be positive.")
    return 1.0 / (2.0 * pi * resistance_ohm * capacitance_nf * 1e-9)

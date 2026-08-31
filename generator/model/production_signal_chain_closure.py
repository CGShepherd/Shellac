"""AE-023 production signal-chain closure helpers."""
from __future__ import annotations
from dataclasses import dataclass
from math import exp, log10, pi

from .balanced_input import default_setting
from .post_eq_dc_block import (
    BIAS_RESISTANCE_OHM,
    CAPACITANCE_F,
    cutoff_hz,
    magnitude_db,
)
from .signal_chain_analysis import (
    riaa_combination,
    signal_point,
    worst_xlr_margin_for_gain,
)
from .signal_chain_noise_dc import noise_budget, dc_budget_default_gain

NOMINAL_CARTRIDGE_RMS_V = 0.005
STARTUP_MUTE_RECOMMENDED_S = 2.0
DC_BLOCK_TAU_S = BIAS_RESISTANCE_OHM * CAPACITANCE_F


@dataclass(frozen=True, slots=True)
class ProductionClosure:
    nominal_riaa_output_rms_v: float
    default_worst_headroom_db: float
    high_worst_headroom_db: float
    electronics_noise_rms_v: float
    electronics_snr_db: float
    dc_block_cutoff_hz: float
    dc_block_loss_20hz_db: float
    conservative_blocked_xlr_dc_v: float
    residual_fraction_after_2s: float


def production_closure() -> ProductionClosure:
    default = default_setting()
    bass, treble = riaa_combination()
    nominal = signal_point(
        gain_setting=default,
        bass=bass,
        treble=treble,
        frequency_hz=1000.0,
        rumble_enabled=False,
        cartridge_rms_v=NOMINAL_CARTRIDGE_RMS_V,
    )
    default_headroom = worst_xlr_margin_for_gain("DEFAULT")
    high_headroom = worst_xlr_margin_for_gain("HIGH")

    # DR-039 is implemented; production noise always includes it.
    noise = noise_budget(rumble_enabled=False, include_dc_block=True)
    dc = dc_budget_default_gain()

    return ProductionClosure(
        nominal.xlr_output_rms_v,
        default_headroom.xlr_margin_db,
        high_headroom.xlr_margin_db,
        noise.output_noise_rms_v,
        20.0 * log10(nominal.xlr_output_rms_v / noise.output_noise_rms_v),
        cutoff_hz(),
        magnitude_db(20.0),
        dc.xlr_diff_offset_with_post_eq_block_estimate_v,
        exp(-STARTUP_MUTE_RECOMMENDED_S / DC_BLOCK_TAU_S),
    )


def validate_production_closure() -> None:
    x = production_closure()
    assert 0.62 < x.nominal_riaa_output_rms_v < 0.67
    assert x.default_worst_headroom_db > 4.4
    assert x.high_worst_headroom_db > 0.45
    assert 70.0 < x.electronics_snr_db < 80.0
    assert 0.4 < x.dc_block_cutoff_hz < 0.6
    assert x.dc_block_loss_20hz_db > -0.01
    assert x.conservative_blocked_xlr_dc_v < 0.025
    assert x.residual_fraction_after_2s < 0.003

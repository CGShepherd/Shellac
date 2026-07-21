from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.model.replay_eq import (
    OPA1612_DESIGN_OUTPUT_RMS_V,
    RECOVERY_GAIN,
    RECOVERY_RF_OHM,
    RECOVERY_RG_OHM,
)
from generator.model.replay_eq_electrical import (
    closure_points,
    db,
    johnson_noise_nv_per_rt_hz,
    worst_case_point,
)


def main() -> int:
    print("SCH103 electrical closure")
    print(
        f"Recovery stage: RG={RECOVERY_RG_OHM:g} ohm, "
        f"RF={RECOVERY_RF_OHM:g} ohm, gain={RECOVERY_GAIN:.4f} ({db(RECOVERY_GAIN):.3f} dB)"
    )
    print(f"Conservative OPA1612 internal design ceiling: {OPA1612_DESIGN_OUTPUT_RMS_V:.2f} V RMS")
    print()
    print(
        f"{'Curve':<12} {'Hz':>8} {'LF gain':>10} {'HF gain':>10} "
        f"{'SCH103':>10} {'Max cart/mV':>13} {'Nom LF/V':>10} {'Nom out/V':>10}"
    )
    print("-" * 92)
    for item in closure_points():
        print(
            f"{item.curve_name:<12} {item.frequency_hz:>8.1f} "
            f"{item.active_lf_gain:>10.3f} {item.passive_hf_gain:>10.3f} "
            f"{item.sch103_gain:>10.3f} {item.max_cartridge_input_rms_v*1000:>13.2f} "
            f"{item.nominal_active_output_rms_v:>10.3f} "
            f"{item.nominal_sch103_output_rms_v:>10.3f}"
        )

    worst = worst_case_point()
    print()
    print(
        f"Worst conservative cartridge-input limit: "
        f"{worst.max_cartridge_input_rms_v*1000:.2f} mV RMS "
        f"({worst.curve_name} at {worst.frequency_hz:g} Hz)"
    )
    print(
        "Nominal-input margin relative to 5 mV: "
        f"{db(worst.max_cartridge_input_rms_v / 0.005):.2f} dB"
    )
    print()
    print("Resistor thermal-noise densities at 300 K")
    for value in (750.0, 2700.0, 8200.0, 10_000.0, 11_000.0, 100_000.0):
        print(f"- {value:>8.0f} ohm: {johnson_noise_nv_per_rt_hz(value):.2f} nV/sqrt(Hz)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

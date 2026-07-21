from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.model.mode_matrix import (
    MODE_TABLE,
    INPUT_BIAS_RESISTOR_OHM,
    OPAMP,
    OUTPUT_ISOLATION_OHM,
    SUM_RESISTOR_OHM,
    SWITCH_TYPE,
    validate_mode_matrix,
)
from generator.model.mode_matrix_analysis import analyse_mode_matrix


def main() -> int:
    validate_mode_matrix()
    result = analyse_mode_matrix()

    print("SCH105 channel-mode matrix analysis")
    print(f"Switch: {SWITCH_TYPE}")
    print(f"Buffer: dual {OPAMP}, unity gain")
    print(f"Summing resistors: {SUM_RESISTOR_OHM:g} ohm each")
    print(f"Input-bias resistors: {INPUT_BIAS_RESISTOR_OHM:g} ohm")
    print(f"Output isolation: {OUTPUT_ISOLATION_OHM:g} ohm")
    print()
    print(f"{'Mode':<14} {'Left output':<16} {'Right output':<16} {'Sum connected'}")
    print("-" * 68)
    for row in MODE_TABLE:
        print(
            f"{row.mode.value:<14} {row.left_output_expression:<16} "
            f"{row.right_output_expression:<16} {str(row.summing_network_connected)}"
        )

    print()
    print(f"Mono equal-input gain: {result.mono_gain:.6f}")
    print(f"Mono equal-input level error: {result.mono_error_db:+.4f} dB")
    print(f"Mono source impedance: {result.mono_source_impedance_ohm:.1f} ohm")
    print(f"Severe-case output margin: {result.severe_output_margin_db:.2f} dB")
    print(
        "Mono-source resistor thermal-noise density: "
        f"{result.summing_resistor_noise_nv_per_rt_hz:.2f} nV/sqrt(Hz)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

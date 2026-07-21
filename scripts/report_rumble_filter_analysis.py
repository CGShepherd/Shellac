from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.model.rumble_filter import (
    BYPASS_SWITCH,
    CAPACITANCE_VALUE,
    OPAMP,
    SECTIONS,
    TARGET_CUTOFF_HZ,
    validate_rumble_filter,
)
from generator.model.rumble_filter_analysis import (
    approximate_group_delay_seconds,
    response_points,
)


def main() -> int:
    validate_rumble_filter()

    print("SCH107 rumble-filter analysis")
    print(f"Topology: 4th-order Butterworth high-pass")
    print(f"Nominal cutoff: {TARGET_CUTOFF_HZ:.1f} Hz")
    print(f"Op amp: {OPAMP}")
    print(f"Bypass: {BYPASS_SWITCH}")
    print(f"Capacitors: {CAPACITANCE_VALUE} film, four per channel")
    print()
    print(f"{'Section':<8} {'R1/ohm':>10} {'R2/ohm':>10} {'f0/Hz':>10} {'Q':>10}")
    print("-" * 52)
    for section in SECTIONS:
        print(
            f"{section.identifier:<8} {section.r1_ohm:>10.0f} "
            f"{section.r2_ohm:>10.0f} {section.realised_f0_hz:>10.3f} "
            f"{section.realised_q:>10.5f}"
        )

    print()
    print(f"{'Frequency/Hz':>12} {'Magnitude/dB':>14} {'Phase/deg':>12}")
    print("-" * 42)
    for point in response_points():
        print(
            f"{point.frequency_hz:>12.2f} "
            f"{point.magnitude_db:>14.3f} "
            f"{point.phase_degrees:>12.3f}"
        )

    print()
    print("Approximate group delay")
    for frequency in (15.0, 20.0, 30.0, 50.0, 100.0):
        delay_ms = approximate_group_delay_seconds(frequency) * 1000.0
        print(f"- {frequency:>6.1f} Hz: {delay_ms:.3f} ms")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

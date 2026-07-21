from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.model.controls import (
    CONTROLS,
    INDICATORS,
    LED_CURRENT_A,
    validate_controls,
)


def main() -> int:
    validate_controls()
    print("SCH109 controls and user-interface closure")
    print()
    print(f"{'ID':<7} {'Control':<22} {'Type':<12} Positions")
    print("-" * 88)
    for item in CONTROLS:
        print(f"{item.identifier:<7} {item.name:<22} {item.control_type:<12} {' / '.join(item.positions)}")

    print()
    print("Rail indicators")
    for item in INDICATORS:
        print(
            f"- {item.identifier}: {item.name}, {item.resistor_ohm:g} ohm, "
            f"{item.nominal_current_a*1000:.2f} mA nominal"
        )

    print()
    print("RIAA operating combination: BASS=TRUE RIAA; TREBLE=2121 Hz RIAA")
    print("Internal gain selection remains a SCH101 implementation requirement.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

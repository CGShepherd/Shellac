from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.model.balanced_input import (
    DEFAULT_GAIN_DB,
    DIFF_CONVERTER_GAIN,
    GAIN_RG_OHM,
    GAIN_SETTINGS,
    SELECTOR,
    validate_balanced_input,
)


def main() -> int:
    validate_balanced_input()
    print("SCH101 selectable-gain closure")
    print(f"Fixed differential converter gain: {DIFF_CONVERTER_GAIN:.4f}x")
    print(f"Per-leg Rg: {GAIN_RG_OHM:g} ohm")
    print(f"Selector: {SELECTOR}")
    print()
    print(f"{'Setting':<10} {'DIP':<5} {'Rf/ohm':>10} {'Leg gain':>10} {'Total gain':>12} {'dB':>9} {'Error/dB':>10}")
    print("-"*76)
    for item in GAIN_SETTINGS:
        print(f"{item.name:<10} {item.dip_pattern:<5} {item.rf_ohm:>10.0f} {item.per_leg_gain:>10.4f} "
              f"{item.total_gain:>12.4f} {item.realised_total_db:>9.3f} {item.error_db:>+10.3f}")
    print()
    print(f"Default target: {DEFAULT_GAIN_DB:.1f} dB")
    print("All four balanced gain legs must use the same two-bit pattern.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

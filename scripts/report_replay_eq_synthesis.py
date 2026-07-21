from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.model.replay_eq import DESIGN_STATUS, TREBLE_NETWORKS
from generator.model.replay_eq_synthesis import active_synthesis_rows, exact_riaa_solution, passive_treble_frequency_hz


def print_active(title: str, rows) -> None:
    print(title)
    print(f"{'Selection':<24} {'RF':>9} {'RS':>9} {'RG':>8} {'C/nF':>8} {'Pole/Hz':>10} {'Zero/Hz':>10} {'Shelf/dB':>10}")
    print("-" * 96)
    for row in rows:
        print(f"{row.selection:<24} {row.rf_ohm:>9.0f} {row.rs_ohm:>9.0f} {row.rg_ohm:>8.0f} {row.capacitance_nf:>8.3f} {row.pole_hz:>10.3f} {row.zero_hz:>10.3f} {row.shelf_db:>10.3f}")


def main() -> int:
    print(f"SCH103 design status: {DESIGN_STATUS.value}")
    print_active("Published P91 source networks", active_synthesis_rows(source=True))
    print()
    print_active("Optimised Shellac active networks", active_synthesis_rows())

    exact_rs, exact_c = exact_riaa_solution()
    print()
    print(f"Exact true-RIAA solution: RS={exact_rs:.3f} ohm, C={exact_c:.6f} nF")
    print("Selected true-RIAA branch: RS=8200 ohm, C=27 nF + 2.4 nF")
    print()
    print("Passive treble networks")
    for item in TREBLE_NETWORKS[1:]:
        actual = passive_treble_frequency_hz(item.resistor_ohm, item.capacitance_nf)
        error = (actual / item.target_hz - 1.0) * 100.0
        print(f"{item.name:<18} {item.resistor_ohm:>7.0f} ohm  {item.capacitance_nf:>7.2f} nF  {actual:>9.3f} Hz  {error:+.3f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

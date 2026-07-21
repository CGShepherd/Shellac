from pathlib import Path
import csv
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.model.replay_curve_analysis import (
    LABEL_RECOMMENDATIONS,
    analyse_all_targets,
)

OUT_CSV = Path("out/replay_curve_analysis.csv")


def main() -> int:
    summaries = analyse_all_targets()
    print("SCH103 full-band replay-curve analysis (normalised at 1 kHz)")
    print(f"{'Target':<25} {'Worst/dB':>10} {'At/Hz':>10} {'RMS/dB':>9} {'20Hz':>8} {'50Hz':>8} {'10kHz':>8} {'20kHz':>8}")
    print("-" * 103)
    for item in summaries:
        print(
            f"{item.target.name:<25} {item.worst_error_db:>+10.3f} "
            f"{item.worst_error_frequency_hz:>10.1f} {item.rms_error_db:>9.3f} "
            f"{item.error_20_hz_db:>+8.3f} {item.error_50_hz_db:>+8.3f} "
            f"{item.error_10_khz_db:>+8.3f} {item.error_20_khz_db:>+8.3f}"
        )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "identifier", "target", "bass_selection", "treble_selection",
            "worst_error_db", "worst_error_frequency_hz", "rms_error_db",
            "error_20_hz_db", "error_50_hz_db", "error_100_hz_db",
            "error_1_khz_db", "error_10_khz_db", "error_20_khz_db",
        ])
        for item in summaries:
            writer.writerow([
                item.target.identifier,
                item.target.name,
                item.target.bass_name,
                item.target.treble_name,
                item.worst_error_db,
                item.worst_error_frequency_hz,
                item.rms_error_db,
                item.error_20_hz_db,
                item.error_50_hz_db,
                item.error_100_hz_db,
                item.error_1_khz_db,
                item.error_10_khz_db,
                item.error_20_khz_db,
            ])

    print()
    print(f"Wrote {OUT_CSV}")
    print()
    print("Practical P91 label starting points")
    for item in LABEL_RECOMMENDATIONS:
        suffix = f" — {item.notes}" if item.notes else ""
        print(f"- {item.label}: bass={item.bass_selection}, treble={item.treble_selection}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

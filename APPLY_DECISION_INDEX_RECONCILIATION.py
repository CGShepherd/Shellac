from pathlib import Path

p = Path("config/decisions/current_decision_index.yaml")
t = p.read_text(encoding="utf-8")

t = t.replace(
    "  commit: 1ebb04d078aec05e370c0a899607d5e46ad25958",
    "  commit: dce5c0ec36e12f979338d8c46106c44a79c7a023",
)
t = t.replace(
    "    implemented_baseline_still:\n"
    "      converter_gain: 4.0\n"
    "      note: Active SCH101 remains the pre-DR038 implementation until atomic CAD migration.\n",
    "    implementation:\n"
    "      converter_gain: 4.0\n"
    "      precision_network: LT5400-7 A-grade, 1.25k/5k\n"
    "      gain_ladder: 1k Rg with 249R / 999R / 2.159k RF service configurations\n"
    "      selector: hard service links; default assembled state = DEFAULT\n",
)

p.write_text(t, encoding="utf-8")
print("Updated authoritative decision index to the validated DR-038/DR-039 baseline.")

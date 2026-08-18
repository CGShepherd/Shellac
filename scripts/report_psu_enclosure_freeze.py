import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.mechanical.psu_enclosure_freeze import build_psu_enclosure_freeze, validate_psu_enclosure_freeze

model = build_psu_enclosure_freeze()
issues = validate_psu_enclosure_freeze(model)
reserve = model.passive_thermal_reserve
print(f"{model.identifier} {model.revision}")
print(f"PSU enclosure: {model.enclosure.order_code} {model.decision.value}")
print(f"Mains entry: {model.mains_entry_order_code}")
print(f"Known geometry fits: {model.known_component_geometry_fits}")
print(f"Historical size gate satisfied: {model.historical_size_gate_satisfied}")
print(f"Residual width: {reserve.residual_width_after_known_components_mm:.1f} mm")
print(f"Residual depth: {reserve.residual_depth_after_known_components_and_mains_mm:.1f} mm")
print(f"Volume ratio vs M5501119: {reserve.internal_volume_ratio_vs_rejected:.2f}x")
print(f"Surface-area ratio vs M5501119: {reserve.external_surface_area_ratio_vs_rejected:.2f}x")
print(f"Temperature prediction claimed: {reserve.temperature_prediction_available}")
print(f"Validation issues: {len(issues)}")
for finding in model.findings:
    print(f"- {finding}")
if issues:
    for issue in issues:
        print(f"ISSUE: {issue}")
    raise SystemExit(1)
out = ROOT / "out/mechanical/psu_enclosure_freeze.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(model.to_dict(), indent=2) + "\n", encoding="utf-8")
print(f"Wrote {out}")

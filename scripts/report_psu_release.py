import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.mechanical.psu_release import build_psu_release_decision, validate_psu_release_decision

model = build_psu_release_decision()
issues = validate_psu_release_decision(model)
print(f"{model.identifier} {model.revision}")
print(f"Enclosure: {model.enclosure_order_code} {model.decision.value}")
print(f"Mains entry: {model.mains_entry.order_code}")
print(f"Mains geometry fits: {model.mains_geometry_fits}")
print(f"Residual nominal depth: {model.residual_depth_after_mains_mm:.2f} mm")
print(f"Thermal evidence complete: {model.thermal_evidence_complete}")
print(f"Validation issues: {len(issues)}")
for finding in model.findings:
    print(f"- {finding}")
if issues:
    for issue in issues:
        print(f"ISSUE: {issue}")
    raise SystemExit(1)
out = ROOT / "out/mechanical/psu_release.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(model.to_dict(), indent=2) + "\n", encoding="utf-8")
print(f"Wrote {out}")

from __future__ import annotations
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from generator.mechanical.unicase_fit import build_unicase_fit_decision, validate_unicase_fit_decision

def main() -> int:
    model = build_unicase_fit_decision()
    issues = validate_unicase_fit_decision(model)
    print(f"{model.identifier} {model.revision}")
    print(f"Audio: {model.audio.order_code} {model.audio_status.value}")
    print(f"PSU: {model.psu.order_code} {model.psu_status.value}")
    print(f"Architecture issues: {len(issues)}")
    print(f"Open items: {len(model.open_items)}")
    print(f"Audio base PCB envelope: {model.audio.base_pcb_width_mm:.0f} x {model.audio.base_pcb_depth_mm:.0f} mm")
    print(f"Transformer conservative envelope: {model.transformer.width_mm:.0f} x {model.transformer.depth_mm:.0f} x {model.transformer.height_mm:.0f} mm")
    for finding in model.findings:
        print(f"- {finding}")
    out = ROOT / "out/mechanical/unicase_fit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(model.to_dict(), indent=2) + "\n")
    print(f"Wrote {out}")
    return 1 if issues else 0

if __name__ == "__main__":
    raise SystemExit(main())

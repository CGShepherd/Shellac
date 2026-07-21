from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.commissioning import build_commissioning_baseline, validate_commissioning_baseline

OUT = ROOT / "out" / "commissioning"


def main() -> int:
    model = build_commissioning_baseline()
    validate_commissioning_baseline(model)
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "commissioning_baseline.json"
    target.write_text(json.dumps(model.to_dict(), indent=2) + "\n", encoding="utf-8")
    print(f"Project Shellac commissioning baseline: {model.identifier} {model.revision}")
    print(f"Stages: {len(model.stages)}")
    print(f"Measurements: {sum(len(stage.measurements) for stage in model.stages)}")
    print(f"Open values: {len(model.open_values)}")
    print(f"Wrote {target.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

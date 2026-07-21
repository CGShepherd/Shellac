"""Report the provisional Gate 3 PCB architecture baseline."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.layout import build_layout_baseline

OUT = ROOT / "out" / "layout"


def main() -> int:
    baseline = build_layout_baseline()
    OUT.mkdir(parents=True, exist_ok=True)
    json_path = OUT / "layout_baseline.json"
    json_path.write_text(json.dumps(baseline.to_dict(), indent=2) + "\n", encoding="utf-8")

    print(f"{baseline.identifier} — {baseline.revision}")
    print(baseline.status)
    print(f"Stack-up: {baseline.stackup.layer_count} layers")
    print(f"Functional regions: {len(baseline.regions)}")
    print(f"Critical-net classes: {len(baseline.critical_nets)}")
    print(f"Manual-only net classes: {sum(n.routing_policy.value == 'manual_only' for n in baseline.critical_nets)}")
    print(f"Wrote {json_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

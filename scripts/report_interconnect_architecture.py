from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from generator.layout.interconnect_architecture import (
    build_interconnect_architecture,
    validate_interconnect_architecture,
)


def main() -> int:
    model = build_interconnect_architecture()
    issues = validate_interconnect_architecture(model)
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        return 1
    out = PROJECT_ROOT / "out/layout/interconnect_architecture.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(model.to_dict(), indent=2), encoding="utf-8")
    print("Project Shellac interconnect architecture: PASS")
    print(f"Harnesses: {len(model.harnesses)}")
    print(f"Crimp tool: {model.crimp_tool.tool}")
    print(f"Status: {model.status}")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

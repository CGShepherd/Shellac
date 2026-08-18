from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.mechanical.interface_architecture import (
    build_interface_architecture,
    validate_interface_architecture,
)
from generator.mechanical import build_mechanical_baseline

OUT = ROOT / "out" / "mechanical"


def main() -> int:
    model = build_interface_architecture()
    issues = validate_interface_architecture(model)
    mechanical = build_mechanical_baseline()

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "interface_architecture.json").write_text(
        json.dumps(model.to_dict(), indent=2) + "\n", encoding="utf-8"
    )

    print(f"{model.identifier} {model.revision}")
    print(f"Status: {model.status}")
    print(
        "Enclosure family: "
        f"{model.enclosure_family.manufacturer} {model.enclosure_family.family}, "
        f"{model.enclosure_family.finish} {model.enclosure_family.colour_standard}"
    )
    print(f"Mechanical baseline: {mechanical.status}")
    print(f"Signal flow: {model.signal_flow_rule}")
    print(f"PSU flow: {model.psu_flow_rule}")
    print(f"Panel interfaces: {len(model.interfaces)}")
    print(f"Architecture issues: {len(issues)}")
    print(f"Open items: {len(model.open_items)}")

    print("\nInterfaces")
    for item in model.interfaces:
        print(
            f"{item.identifier}: {item.enclosure} {item.kind.value} -> "
            f"{item.face.value} [{item.mounting.value}]"
        )


    if model.drilling_template:
        print("\nDrilling-template contract")
        print(
            f"Formats: {model.drilling_template.primary_format} + "
            f"{model.drilling_template.machine_format}; scale {model.drilling_template.scale}"
        )
        print(f"Release gate: {model.drilling_template.release_gate}")

    if issues:
        print("\nISSUES")
        for issue in issues:
            print(f"- {issue}")
    print("\nWrote out/mechanical/interface_architecture.json")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())

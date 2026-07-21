from pathlib import Path
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.dispatch import build_project_from_model, shellac_builder_registry
from generator.model.shellac import build_shellac_model

OUT = Path("out/kicad")
PROJECT = "ProjectShellac"


def main() -> int:
    model = build_shellac_model()
    results = build_project_from_model(
        model,
        shellac_builder_registry(),
        out_dir=OUT,
        project_name=PROJECT,
    )

    implemented = sum(result.status == "implemented" for result in results)
    pending = sum(result.status == "pending" for result in results)
    print(f"Validated {model.name} — {model.revision}")
    print(f"Generated {implemented} implemented functional block(s).")
    print(f"Reported {pending} pending functional block(s).")
    print(f"Wrote {OUT / (PROJECT + '.kicad_pro')}")
    print(f"Wrote {OUT / (PROJECT + '.kicad_sch')}")
    manifest = json.loads((OUT / "build_manifest.json").read_text(encoding="utf-8"))
    print(f"Wrote {OUT / 'build_manifest.txt'}")
    print(f"Build ID: {manifest['build_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

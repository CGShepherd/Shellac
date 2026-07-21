from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.adapters.model_to_sheet import block_summary_sheet
from generator.model.shellac import build_shellac_model
from generator.model.validation import validate_project
from generator.writers.kicad9 import clean_output, write_project, write_schematic

OUT = Path("out/engineering_model")
PROJECT = "ProjectShellac_EngineeringModel"


def main() -> None:
    model = build_shellac_model()
    validate_project(model)

    clean_output(OUT)
    write_project(PROJECT, OUT)

    for block in model.blocks:
        filename = f"{block.identifier}_{block.name.replace(' ', '_')}.kicad_sch"
        sheet = block_summary_sheet(model, block, filename)
        write_schematic(sheet, OUT / filename)

    print(f"Validated {model.name} {model.revision}")
    print(f"Wrote {len(model.blocks)} architecture-summary schematics to {OUT}")


if __name__ == "__main__":
    main()

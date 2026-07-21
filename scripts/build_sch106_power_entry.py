from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.blocks.power_entry import add_power_entry
from generator.core.sheet import Sheet
from generator.writers.kicad9 import clean_output, write_project, write_schematic

OUT = Path("out/kicad_power_entry")
PROJECT = "ProjectShellac_PowerEntry"

def main():
    clean_output(OUT)
    write_project(PROJECT, OUT)
    sheet = Sheet(
        title="Project Shellac — SCH-106 Audio-box Power Entry",
        filename=f"{PROJECT}.kicad_sch",
    )
    add_power_entry(sheet)
    write_schematic(sheet, OUT / f"{PROJECT}.kicad_sch")
    print(f"Wrote {OUT / (PROJECT + '.kicad_pro')}")
    print(f"Wrote {OUT / (PROJECT + '.kicad_sch')}")

if __name__ == "__main__":
    main()

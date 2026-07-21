from pathlib import Path
import sys
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
from generator.blocks.balanced_input import add_input_connector_slice
from generator.core.sheet import Sheet
from generator.writers.kicad9 import write_project, write_schematic
OUT = Path("out/kicad")
PROJECT = "ProjectShellac"
def main():
    write_project(PROJECT, OUT)
    sheet = Sheet(title="Project Shellac — SCH-101 Balanced Input", filename=f"{PROJECT}.kicad_sch")
    add_input_connector_slice(sheet)
    write_schematic(sheet, OUT / f"{PROJECT}.kicad_sch")
    print(f"Wrote {OUT / (PROJECT + '.kicad_pro')}")
    print(f"Wrote {OUT / (PROJECT + '.kicad_sch')}")
if __name__ == "__main__":
    main()

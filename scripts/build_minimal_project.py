from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.core.components import capacitor, resistor, testpoint
from generator.core.geometry import Point
from generator.core.sheet import Sheet
from generator.writers.kicad9 import write_project, write_schematic

OUT = Path("out/kicad")
PROJECT = "ProjectShellac"

def main():
    write_project(PROJECT, OUT)

    sheet = Sheet(
        title="Project Shellac — Generator Sprint 0.1 Smoke Test",
        filename=f"{PROJECT}.kicad_sch",
    )
    sheet.add_note("Sprint 0.1: generator framework smoke test.")
    sheet.add_component(resistor("R001", "10k", Point(40, 60), tolerance="1%", function="Smoke-test resistor"))
    sheet.add_component(capacitor("C001", "100n", Point(70, 60), dielectric="X7R", voltage="50V", function="Smoke-test capacitor"))
    sheet.add_component(testpoint("TP001", "TEST_NODE", Point(100, 60)))

    write_schematic(sheet, OUT / f"{PROJECT}.kicad_sch")
    print(f"Wrote {OUT / (PROJECT + '.kicad_pro')}")
    print(f"Wrote {OUT / (PROJECT + '.kicad_sch')}")

if __name__ == "__main__":
    main()

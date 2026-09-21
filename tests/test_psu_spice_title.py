from pathlib import Path
import pytest
from simulation.psu.scripts import psu_run

ROOT=Path(__file__).resolve().parents[1]

def test_lf353_smoke_has_explicit_spice_title():
    p=ROOT/"simulation/psu/runs/run00_model_qualification/lf353_smoke.cir.in"
    first=p.read_text(encoding="utf-8").splitlines()[0].strip()
    assert first.startswith("*")

def test_deck_rejects_electrical_statement_as_first_line(tmp_path):
    template=tmp_path/"bad.cir.in"
    template.write_text("VP VP 0 15\n.end\n",encoding="utf-8")
    with pytest.raises(psu_run.ToolchainError,match="must begin"):
        psu_run.deck(None,"title_guard",template,{})

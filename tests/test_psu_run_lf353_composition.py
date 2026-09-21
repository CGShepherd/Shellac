from pathlib import Path
from simulation.psu.scripts.psu_run import embed_lf353_vendor, embed_lf353_wrapper

def test_lf353_self_contained_composition(tmp_path):
    vendor=tmp_path/"LF353.301"
    vendor.write_text(".SUBCKT LF353 1 2 3 4 5\n.ENDS LF353\n")
    wrapper=tmp_path/"lf353_shellac_psu.lib"
    wrapper.write_text(".SUBCKT SHELLAC_LF353 INP INM VPLUS VMINUS OUT\nXOP INP INM VPLUS VMINUS OUT LF353\n.ENDS SHELLAC_LF353\n")
    deck=f'.include "{vendor}"\n.include "{wrapper}"\nXU A B VP VN O SHELLAC_LF353\n.end\n'
    deck=embed_lf353_vendor(deck,vendor)
    deck=embed_lf353_wrapper(deck,wrapper)
    assert ".include" not in deck.lower()
    assert deck.lower().count(".subckt lf353 ")==1
    assert deck.lower().count(".subckt shellac_lf353 ")==1
    assert "xu a b vp vn o shellac_lf353" in deck.lower()

def test_runner_preserves_execution_failures():
    src=Path("simulation/psu/scripts/psu_run.py").read_text(encoding="utf-8")
    assert 'if q.returncode:' in src
    assert 'preserve_diagnostics(name,p,log,p.with_suffix(".raw"),txt)' in src

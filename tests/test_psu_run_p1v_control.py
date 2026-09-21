import pytest
from simulation.psu.scripts import psu_run
from simulation.scripts.shellac_spice import ToolchainError

def test_embedding_preserves_wrapper(tmp_path):
    v=tmp_path/"LF353.301"; v.write_text(".SUBCKT LF353 1 2 3 4 5\n.ENDS LF353\n")
    w=tmp_path/"lf353_shellac_psu.lib"
    d=f'.include "{v.as_posix()}"\n.include "{w.as_posix()}"\n.op\n.end\n'
    out=psu_run.embed_lf353_vendor(d,v)
    assert v.as_posix().lower() not in out.lower()
    assert w.as_posix().lower() in out.lower()

def test_required_measurements_reject_tnom_temp(monkeypatch):
    monkeypatch.setattr(psu_run,"qcfg",lambda:{"required_measurements":{"LM317":["VOUT_AVG","VOUT_MIN","VOUT_MAX"]}})
    with pytest.raises(ToolchainError):
        psu_run.require_measurements("LM317",{"TNOM":27.0,"TEMP":27.0})

def test_p1v_midpoint_and_220():
    import yaml
    d=yaml.safe_load((psu_run.PSU/"config"/"p1v.yaml").read_text())
    assert d["adjustment"]["nominal_effective_resistance_ohm"]==2500
    assert d["adjustment"]["qualification_effective_resistance_range_ohm"]==[0,5000]
    assert d["regulators"]["output_adjust_resistor_ohm_nominal"]==220
    assert d["servo"]["positive_rail_channel"]=="U1B"
    assert d["servo"]["negative_rail_channel"]=="U1A"
    policy=d["qualification_policy"]
    assert policy["run01_requires_run00_pass"] is True
    assert policy["run00_gate_status"]=="PASS"
    assert policy["run00_evidence"]=="simulation/psu/RUN00_QUALIFICATION.md"
    assert "run01_locked_until_run00_passes" not in policy

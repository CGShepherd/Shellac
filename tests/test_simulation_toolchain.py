from pathlib import Path

from simulation.scripts.shellac_spice import SIM, evaluate, load_yaml, parse_measurements, render_template, run_config, sha256_file

def test_run00_controlled_config_exists():
    cfg=run_config("RUN00")
    assert cfg["authority"]=={"architecture":"AE-053","execution":"AE-050","acceptance":"AE-049"}
    assert set(cfg["expected_measurements"])=={"RUN00_VPLUS18","RUN00_VMINUS18","RUN00_VMID"}

def test_run00_template_is_fully_parameterised_and_bipolar():
    cfg=run_config("RUN00"); template=Path(cfg["netlist_template"]).read_text(encoding="utf-8"); rendered=render_template(template,cfg["parameters"])
    assert "{{" not in rendered
    assert ".include ../runs/run00_sanity/run00_support.lib" in rendered
    assert "XDIV VPLUS18 VMID VMINUS18 SHELLAC_RUN00_DIV" in rendered
    assert ".meas DC RUN00_VPLUS18" in rendered

def test_run00_support_divider_has_explicit_return_node():
    support=(SIM/"runs"/"run00_sanity"/"run00_support.lib").read_text(encoding="utf-8")
    assert ".subckt SHELLAC_RUN00_DIV IN OUT RETURN" in support
    assert "R2 OUT RETURN {RLOAD}" in support

def test_measurement_parser_accepts_ltspice_style_colon_and_equals():
    text="""
RUN00_VPLUS18: 1.8000000e+01
RUN00_VMINUS18 = -1.8000000e+01
RUN00_VMID: 0.0e+00
"""
    parsed=parse_measurements(text)
    assert parsed["RUN00_VPLUS18"]==18.0 and parsed["RUN00_VMINUS18"]==-18.0 and parsed["RUN00_VMID"]==0.0

def test_acceptance_mapping_is_data_driven():
    criteria=load_yaml(SIM/"config"/"acceptance.yaml")["criteria"]
    assert evaluate(18.0,criteria["run00_positive_rail"])[0]
    assert evaluate(-18.0,criteria["run00_negative_rail"])[0]
    assert evaluate(0.0,criteria["run00_midpoint"])[0]
    assert not evaluate(0.01,criteria["run00_midpoint"])[0]

def test_project_run00_support_model_is_hashable():
    assert len(sha256_file(SIM/"runs"/"run00_sanity"/"run00_support.lib"))==64

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_manifest():
    return yaml.safe_load((ROOT / "simulation/config/model_sources.yaml").read_text(encoding="utf-8"))

def load_integrated():
    return yaml.safe_load((ROOT / "simulation/config/integrated_baseline.yaml").read_text(encoding="utf-8"))

def test_primary_grado_identity_is_78c():
    src = load_manifest()["sources"]
    assert "CARTRIDGE_GRADO_78C" in src
    assert "CARTRIDGE_GRADO_78E" not in src
    required = {x["id"] for x in load_integrated()["required_model_sources"]}
    assert "CARTRIDGE_GRADO_78C" in required
    assert "CARTRIDGE_GRADO_78E" not in required

def test_sch101_input_opamp_role_resolves_to_opa1656():
    src = load_manifest()["sources"]
    assert "SCH101_GAIN" in src["OPA1656"]["roles"]
    assert "SCH101_DIFF_CONVERTER" in src["OPA1656"]["roles"]
    required = {x["id"] for x in load_integrated()["required_model_sources"]}
    assert "SCH101_INPUT_OPAMP" not in required
    assert "OPA1656" in required

def test_vendor_sources_are_not_prematurely_resolved():
    src = load_manifest()["sources"]
    for key in ("OPA1656", "OPA1612", "LT5400", "THAT1646", "DIODE_S1G"):
        assert src[key]["status"] != "RESOLVED"
    assert "DIODE_1N4004" not in src

def test_at_vm95sp_official_electrical_values():
    e = load_manifest()["sources"]["CARTRIDGE_AT_VM95SP"]["electrical"]
    assert e["dc_resistance_ohm"] == 485
    assert e["inductance_h_at_1khz"] == 0.550
    assert e["recommended_load_ohm"] == 47000
    assert e["recommended_load_capacitance_pf_min"] == 100
    assert e["recommended_load_capacitance_pf_max"] == 200
    assert e["output_v_rms_at_1khz_5cms"] == 0.0027

def test_grado_78c_model_remains_bench_topology_open():
    g = load_manifest()["sources"]["CARTRIDGE_GRADO_78C"]
    assert g["identity_authority"] == "PROJECT_HARDWARE_BASELINE"
    assert g["status"] == "PARAMETERS_IDENTIFIED_BENCH_TOPOLOGY_OPEN"
    assert g["electrical"]["dc_resistance_ohm"] == 475
    assert g["electrical"]["inductance_h"] == 0.045
    assert g["electrical"]["recommended_load_ohm"] == 47000

def test_required_model_source_gate_remains_resolved_after_ae065_run00():
    integrated = load_integrated()
    required = integrated["required_model_sources"]
    assert required
    assert integrated["authority"]["model_source_closure"] == "AE-064"
    assert all(x["status"] == "RESOLVED" for x in required)
    run00 = integrated["integrated_run00"]
    assert run00["status"] == "PASSED_NOMINAL_SANITY"
    assert run00["authority"] == "AE-065"
    assert run00["shellac_top_implemented"] is True
    assert run00["shellac_top_run00_executed"] is True

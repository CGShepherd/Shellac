from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(path):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))

def test_ae064_cartridge_files_and_interfaces():
    expected = {
        "simulation/models/cartridges/grado_78c_shellac.lib":
            (".SUBCKT SHELLAC_GRADO_78C P N DRIVE", "RCOIL NGEN NRL 475", "LCOIL NRL P 45m"),
        "simulation/models/cartridges/at_vm95sp_shellac.lib":
            (".SUBCKT SHELLAC_AT_VM95SP P N DRIVE", "RCOIL NGEN NRL 485", "LCOIL NRL P 550m"),
        "simulation/models/cartridges/grado_gold_8mz_shellac.lib":
            (".SUBCKT SHELLAC_GRADO_GOLD_8MZ P N DRIVE", "RCOIL NGEN NRL 660", "LCOIL NRL P 50m"),
    }
    for rel, needles in expected.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            assert needle in text

def test_ae064_required_sources_remain_resolved_after_later_run00_progress():
    cfg = load_yaml("simulation/config/integrated_baseline.yaml")
    assert all(item["status"] == "RESOLVED" for item in cfg["required_model_sources"])
    assert cfg["authority"]["model_source_closure"] == "AE-064"
    run00 = cfg["integrated_run00"]
    assert run00["status"] in {
        "READY_FOR_SHELLAC_TOP_IMPLEMENTATION",
        "PASSED_NOMINAL_SANITY",
    }
    if run00["status"] == "READY_FOR_SHELLAC_TOP_IMPLEMENTATION":
        assert run00["shellac_top_implemented"] is False
        assert run00["shellac_top_run00_executed"] is False
    else:
        assert run00["authority"] == "AE-065"
        assert run00["shellac_top_implemented"] is True
        assert run00["shellac_top_run00_executed"] is True

def test_ae064_qualification_evidence_is_cross_referenced():
    qual = load_yaml("simulation/config/model_qualification.yaml")
    assert qual["authority"] == "AE-064"
    assert qual["sources"]["GRADO_78C"]["status"] == "QUALIFIED_BEHAVIOURAL_REFERENCE_MODEL"
    assert qual["sources"]["AT_VM95SP"]["status"] == "QUALIFIED_BEHAVIOURAL_REFERENCE_MODEL"
    assert qual["sources"]["GRADO_GOLD_8MZ"]["gating_for_integrated_run00"] is False

def test_ae064_grado_limit_does_not_close_bench_topology():
    cfg = load_yaml("simulation/config/cartridge_models.yaml")
    grado = cfg["models"]["GRADO_78C"]
    assert "body_return_isolation_modelled" not in grado
    assert "R-021" in grado["limitation"]
    assert cfg["interface"]["body_return_isolation_modelled"] is False

def test_ae064_preflight_checks_qualification_not_static_labels_only():
    text = (ROOT / "simulation/scripts/integrated_preflight.py").read_text(encoding="utf-8")
    assert "model_qualification.yaml" in text
    assert "CARTRIDGE_GRADO_78C" in text
    assert "CARTRIDGE_AT_VM95SP" in text
    assert "qualification status" in text

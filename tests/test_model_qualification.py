from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(rel):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))

def test_ae064_model_qualification_preserves_ae062_wrapped_sources():
    q = load_yaml("simulation/config/model_qualification.yaml")
    assert q["authority"] == "AE-064"
    assert q["qualification_semantics"]["vendor_model_smoke"] == "PASS"
    assert q["qualification_semantics"]["shellac_wrapper_smoke"] == "PASS"
    src = q["sources"]
    assert src["OPA1656"]["subckt"] == "OPA1656"
    assert src["OPA1612"]["subckt"] == "OPA161x"
    assert src["LT5400"]["subckt"] == "LT5400-7"
    assert src["THAT1646"]["subckt"] == "THAT1646"
    for key in ("OPA1656", "OPA1612", "LT5400", "THAT1646"):
        item = src[key]
        assert item["vendor_smoke_test"] == "PASS"
        assert item["wrapper_smoke_test"] == "PASS"
        assert item["redistribution_status"] == "NOT_YET_APPROVED"

def test_ae062_yaml_paths_parse_as_literal_windows_paths():
    q = load_yaml("simulation/config/model_qualification.yaml")
    assert q["ltspice"]["executable"].endswith(r"ADI\LTspice\LTspice.exe")
    assert q["sources"]["LT5400"]["source_library"].endswith(r"LTspice\lib\sub\LT5400.lib")

def test_ae063_model_source_manifest_is_self_consistent():
    m = load_yaml("simulation/config/model_sources.yaml")
    assert m["authority"] == "AE-063"
    s = m["sources"]
    expected = {
        "OPA1656": "QUALIFIED_LOCAL_SOURCE",
        "OPA1612": "QUALIFIED_LOCAL_SOURCE",
        "LT5400": "QUALIFIED_LOCAL_LIBRARY_SOURCE",
        "THAT1646": "QUALIFIED_LOCAL_SOURCE",
    }
    for key, status in expected.items():
        item = s[key]
        assert item["status"] == status
        assert item["sha256"]
        assert item["pin_mapping_verified"] is True
        assert item["wrapper_path"]
        assert item["qualification_record"] == "simulation/config/model_qualification.yaml"

def test_ae063_s1g_reference_model_is_qualified_without_wrapper():
    q = load_yaml("simulation/config/model_qualification.yaml")
    d = q["sources"]["S1G"]
    assert d["vendor"] == "Vishay General Semiconductor"
    assert d["model_name"] == "s1g"
    assert d["direct_use"] is True
    assert d["vendor_smoke_test"] == "PASS"
    assert d["status"] == "QUALIFIED_LOCAL_REFERENCE_SOURCE"
    assert d["redistribution_status"] == "NOT_YET_APPROVED"
    assert "wrapper_smoke_test" not in d

def test_ae062_wrapper_smoke_harness_present():
    assert (ROOT / "simulation/scripts/ae062_wrapper_smoke.py").is_file()

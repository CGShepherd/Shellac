from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(rel):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))

def test_live_output_driver_uses_s1g():
    text = (ROOT / "generator/model/output_driver.py").read_text(encoding="utf-8")
    assert 'SURGE_DIODE = "S1G"' in text
    assert 'SURGE_DIODE = "1N4004"' not in text

def test_bom_clamp_matches_sma_geometry():
    bom = load_yaml("config/bom/shellac_bom.yaml")
    rows = [x for x in bom["items"] if x.get("id") == "BOM-SCH108-CLAMP"]
    assert len(rows) == 1
    row = rows[0]
    assert row["manufacturer"] == "Vishay General Semiconductor"
    assert row["mpn"] == "S1G"
    assert row["quantity"] == 8
    assert row["footprint"] == "Diode_SMD:D_SMA"

def test_integrated_contract_requires_s1g_not_1n4004():
    cfg = load_yaml("simulation/config/integrated_baseline.yaml")
    ids = [x["id"] for x in cfg["required_model_sources"]]
    assert "DIODE_S1G" in ids
    assert "DIODE_1N4004" not in ids

def test_s1g_model_provenance_is_controlled_but_not_resolved():
    src = load_yaml("simulation/config/model_sources.yaml")
    assert src["authority"] == "AE-063"
    s1g = src["sources"]["DIODE_S1G"]
    assert s1g["manufacturer"] == "Vishay General Semiconductor"
    assert s1g["sha256"] == "ffd79ea06d6ab712987b44e577c8787dbe54d25a90de58e3f6901a1b89642ed4"
    assert s1g["model_name"] == "s1g"
    assert s1g["direct_use"] is True
    assert s1g["status"] != "RESOLVED"

def test_s1g_qualification_smoke_is_preserved_after_ae064():
    q = load_yaml("simulation/config/model_qualification.yaml")
    assert q["authority"] == "AE-064"
    s1g = q["sources"]["S1G"]
    assert s1g["vendor_smoke_test"] == "PASS"
    assert s1g["status"] == "QUALIFIED_LOCAL_REFERENCE_SOURCE"
    assert s1g["model_file_sha256"] == "ffd79ea06d6ab712987b44e577c8787dbe54d25a90de58e3f6901a1b89642ed4"

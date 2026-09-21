from pathlib import Path
import yaml,re
ROOT=Path(__file__).resolve().parents[1]; PSU=ROOT/"simulation/psu"
def test_frozen_sources():
    c=yaml.safe_load((PSU/"config/model_sources.yaml").read_text())
    for s in c["sources"].values():
        assert len(s["archive_sha256"])==64 and len(s["model_sha256"])==64 and s["pins"]
def test_lm317_nc_is_not_artificially_loaded():
    t=(PSU/"models/wrappers/lm317_shellac_psu.lib").read_text()
    assert re.search(r"XREG\s+IN\s+ADJ\s+OUT\s+NC_OUT1\s+LM317_TRANS",t,re.I)
    assert "RNC" not in t.upper()
def test_lm337_program_network_is_canonical():
    t=(PSU/"runs/run00_model_qualification/lm337_smoke.cir.in").read_text()
    assert "R1 OUT ADJ 240" in t and "R2 ADJ 0 720" in t
def test_vendor_payloads_absent():
    names={p.name.upper() for p in PSU.rglob("*") if p.is_file()}
    assert not {"LM317_TRANS.LIB","LM337_N_TRANS.LIB","LF353.301"} & names

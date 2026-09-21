from simulation.psu.scripts import psu_run


def test_lf353_literal_vendor_interface():
    assert psu_run.cfg()["sources"]["LF353"]["pins"] == ["1", "2", "3", "4", "5"]


def test_readlog_ascii_and_utf16(tmp_path):
    a = tmp_path / "a.log"
    a.write_bytes(b"LTspice 26.0.2\nvout_avg: 5.0\n")
    assert "vout_avg" in psu_run.readlog(a)

    u = tmp_path / "u.log"
    u.write_text(
        "LTspice legacy\nvout_avg: 5.0\n",
        encoding="utf-16",
    )
    assert "vout_avg" in psu_run.readlog(u)


def test_lf353_embedding(tmp_path):
    v = tmp_path / "LF353.301"
    payload = (
        ".SUBCKT LF353 1 2 3 4 5\n"
        "R1 1 2 1k\n"
        ".ENDS LF353\n"
    )
    v.write_text(payload, encoding="utf-8")

    d = (
        '.include "C:/vendor/LF353.301"\n'
        "XU 1 2 3 4 5 LF353\n"
        ".op\n"
        ".end\n"
    )

    out = psu_run.embed_lf353_vendor(d, v)

    assert ".include" not in out.lower()
    assert payload.rstrip() in out
    assert out.lower().rfind(".subckt lf353") < out.lower().rfind(".end")
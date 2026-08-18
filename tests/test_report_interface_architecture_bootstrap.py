from scripts import report_interface_architecture


def test_interface_architecture_report_bootstraps_from_repo_root(tmp_path, monkeypatch):
    monkeypatch.setattr(report_interface_architecture, "OUT", tmp_path)
    assert report_interface_architecture.main() == 0
    assert (tmp_path / "interface_architecture.json").exists()

from pathlib import Path
import importlib.metadata


def _requirements():
    return {
        line.strip()
        for line in Path("requirements.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def test_pyyaml_is_declared_and_pinned():
    assert "PyYAML==6.0.3" in _requirements()


def test_pyyaml_runtime_matches_controlled_baseline():
    assert importlib.metadata.version("PyYAML") == "6.0.3"


def test_pytest_remains_declared():
    assert any(line.lower().startswith("pytest") for line in _requirements())

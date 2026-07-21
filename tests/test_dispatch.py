from pathlib import Path

import pytest

from generator.dispatch import (
    BuilderRegistry,
    build_project_from_model,
    shellac_builder_registry,
)
from generator.model.shellac import build_shellac_model


def test_shellac_registry_contains_existing_detailed_builders():
    registry = shellac_builder_registry()
    assert registry.registered_ids() == {"SCH101", "SCH103", "SCH104", "SCH105", "SCH106", "SCH107", "SCH108", "SCH109"}


def test_duplicate_builder_registration_is_rejected():
    registry = BuilderRegistry()
    registry.register("SCH999", "Test", lambda sheet: None)
    with pytest.raises(ValueError):
        registry.register("SCH999", "Test Again", lambda sheet: None)


def test_model_driven_build_generates_registered_blocks_and_manifest(tmp_path: Path):
    model = build_shellac_model()
    results = build_project_from_model(
        model,
        shellac_builder_registry(),
        out_dir=tmp_path,
        project_name="ProjectShellac",
    )

    by_id = {result.block_id: result for result in results}
    assert by_id["SCH101"].status == "implemented"
    assert by_id["SCH106"].status == "implemented"
    assert by_id["SCH103"].status == "implemented"
    assert (tmp_path / "ProjectShellac.kicad_pro").exists()
    assert (tmp_path / "ProjectShellac.kicad_sch").exists()
    assert (tmp_path / "ProjectShellac_SCH101.kicad_sch").exists()
    assert (tmp_path / "ProjectShellac_SCH106.kicad_sch").exists()
    assert (tmp_path / "build_manifest.json").exists()
    assert (tmp_path / "build_manifest.txt").exists()

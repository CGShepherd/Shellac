from pathlib import Path

import pytest

from generator.build_provenance import (
    GeneratedProjectMismatchError,
    KiCadSessionOpenError,
    require_closed_kicad_session,
    verify_generated_project,
    write_provenance,
)


def _cad_file(directory: Path, name: str, content: str) -> Path:
    path = directory / name
    path.write_text(content, encoding="utf-8")
    return path


def test_build_guard_rejects_open_kicad_session(tmp_path: Path):
    _cad_file(tmp_path, "~ProjectShellac.kicad_sch.lck", "lock")
    with pytest.raises(KiCadSessionOpenError, match="Close KiCad completely"):
        require_closed_kicad_session(tmp_path)


def test_build_guard_accepts_closed_project(tmp_path: Path):
    require_closed_kicad_session(tmp_path)


def test_generated_project_provenance_round_trip(tmp_path: Path):
    _cad_file(tmp_path, "ProjectShellac.kicad_pro", "{}")
    _cad_file(tmp_path, "ProjectShellac.kicad_sch", "(kicad_sch)")
    _cad_file(tmp_path, "ProjectShellac.kicad_sym", "(kicad_symbol_lib)")
    _cad_file(tmp_path, "sym-lib-table", "(sym_lib_table)")
    provenance = write_provenance(tmp_path)
    verified = verify_generated_project(tmp_path)
    assert verified["build_id"] == provenance["build_id"]
    assert verified["files"] == provenance["files"]
    assert verified["mutable_files"] == provenance["mutable_files"]
    assert verified["mutable_changes"] == []
    assert len(provenance["build_id"]) == 16
    assert "ProjectShellac.kicad_pro" in provenance["mutable_files"]


def test_provenance_detects_modified_generated_file(tmp_path: Path):
    schematic = _cad_file(
        tmp_path, "ProjectShellac.kicad_sch", "(kicad_sch original)"
    )
    write_provenance(tmp_path)
    schematic.write_text("(kicad_sch modified)", encoding="utf-8")
    with pytest.raises(GeneratedProjectMismatchError, match="changed="):
        verify_generated_project(tmp_path)


def test_kicad_project_file_change_is_reported_but_not_fatal(tmp_path: Path):
    project = _cad_file(tmp_path, "ProjectShellac.kicad_pro", "{}")
    _cad_file(tmp_path, "ProjectShellac.kicad_sch", "(kicad_sch)")
    write_provenance(tmp_path)
    project.write_text('{"erc": {"meta": {"version": 0}}}', encoding="utf-8")
    verified = verify_generated_project(tmp_path)
    assert verified["mutable_changes"] == ["ProjectShellac.kicad_pro"]


def test_mutable_project_file_does_not_change_build_id(tmp_path: Path):
    project = _cad_file(tmp_path, "ProjectShellac.kicad_pro", "{}")
    _cad_file(tmp_path, "ProjectShellac.kicad_sch", "(kicad_sch)")
    first = write_provenance(tmp_path)["build_id"]
    project.write_text('{"editor": "modified"}', encoding="utf-8")
    assert verify_generated_project(tmp_path)["build_id"] == first



def test_legacy_provenance_with_project_file_in_immutable_map_is_migrated(
    tmp_path: Path,
):
    project = _cad_file(tmp_path, "ProjectShellac.kicad_pro", "{}")
    schematic = _cad_file(
        tmp_path, "ProjectShellac.kicad_sch", "(kicad_sch)"
    )

    # Recreate the provenance format written before SR-021G.
    from generator.build_provenance import (
        build_id_from_hashes,
        file_sha256,
    )
    legacy_files = {
        project.name: file_sha256(project),
        schematic.name: file_sha256(schematic),
    }
    (tmp_path / "build_provenance.json").write_text(
        __import__("json").dumps(
            {
                "build_id": build_id_from_hashes(legacy_files),
                "files": legacy_files,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    verified = verify_generated_project(tmp_path)

    assert verified["provenance_migrated"] == [
        "ProjectShellac.kicad_pro"
    ]
    assert "ProjectShellac.kicad_pro" not in verified["files"]
    assert "ProjectShellac.kicad_pro" in verified["mutable_files"]
    assert verified["legacy_build_id"] != verified["build_id"]


def test_legacy_provenance_tolerates_kicad_rewriting_project_file(
    tmp_path: Path,
):
    project = _cad_file(tmp_path, "ProjectShellac.kicad_pro", "{}")
    schematic = _cad_file(
        tmp_path, "ProjectShellac.kicad_sch", "(kicad_sch)"
    )

    from generator.build_provenance import (
        build_id_from_hashes,
        file_sha256,
    )
    legacy_files = {
        project.name: file_sha256(project),
        schematic.name: file_sha256(schematic),
    }
    (tmp_path / "build_provenance.json").write_text(
        __import__("json").dumps(
            {
                "build_id": build_id_from_hashes(legacy_files),
                "files": legacy_files,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    project.write_text('{"erc": {"meta": {"version": 0}}}', encoding="utf-8")
    verified = verify_generated_project(tmp_path)

    assert verified["mutable_changes"] == [
        "ProjectShellac.kicad_pro"
    ]
    assert verified["provenance_migrated"] == [
        "ProjectShellac.kicad_pro"
    ]

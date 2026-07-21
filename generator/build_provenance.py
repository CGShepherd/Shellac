"""Generated-project session safety and deterministic provenance."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import json


IMMUTABLE_HASH_SUFFIXES = {
    ".kicad_sch",
    ".kicad_sym",
}
MUTABLE_PROJECT_SUFFIXES = {".kicad_pro"}
GENERATED_TABLE_NAMES = {"sym-lib-table", "fp-lib-table"}


class KiCadSessionOpenError(RuntimeError):
    """Raised when a generated KiCad project appears to be open."""


class GeneratedProjectMismatchError(RuntimeError):
    """Raised when generated CAD files do not match their build manifest."""


def lock_files(out_dir: Path) -> tuple[Path, ...]:
    out_dir = Path(out_dir)
    if not out_dir.exists():
        return ()
    return tuple(sorted(
        path
        for path in out_dir.iterdir()
        if path.is_file() and path.name.startswith("~") and path.name.endswith(".lck")
    ))


def require_closed_kicad_session(out_dir: Path) -> None:
    locks = lock_files(out_dir)
    if not locks:
        return
    names = ", ".join(path.name for path in locks)
    raise KiCadSessionOpenError(
        "Refusing to rebuild generated KiCad output while a KiCad lock file "
        f"is present: {names}. Close KiCad completely, confirm the lock file "
        "has disappeared, then rerun the build."
    )


def immutable_generated_files(out_dir: Path) -> tuple[Path, ...]:
    out_dir = Path(out_dir)
    files = []
    if not out_dir.exists():
        return ()
    for path in out_dir.iterdir():
        if not path.is_file():
            continue
        if path.suffix in IMMUTABLE_HASH_SUFFIXES or path.name in GENERATED_TABLE_NAMES:
            files.append(path)
    return tuple(sorted(files, key=lambda item: item.name))


def mutable_project_files(out_dir: Path) -> tuple[Path, ...]:
    out_dir = Path(out_dir)
    if not out_dir.exists():
        return ()
    files = [
        path for path in out_dir.iterdir()
        if path.is_file() and path.suffix in MUTABLE_PROJECT_SUFFIXES
    ]
    return tuple(sorted(files, key=lambda item: item.name))


def generated_cad_files(out_dir: Path) -> tuple[Path, ...]:
    return tuple(sorted(
        (*immutable_generated_files(out_dir), *mutable_project_files(out_dir)),
        key=lambda item: item.name,
    ))


def file_sha256(path: Path) -> str:
    digest = sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def immutable_hashes(out_dir: Path) -> dict[str, str]:
    return {path.name: file_sha256(path) for path in immutable_generated_files(out_dir)}


def mutable_hashes(out_dir: Path) -> dict[str, str]:
    return {path.name: file_sha256(path) for path in mutable_project_files(out_dir)}


def cad_hashes(out_dir: Path) -> dict[str, str]:
    return {**immutable_hashes(out_dir), **mutable_hashes(out_dir)}


def build_id_from_hashes(hashes: dict[str, str]) -> str:
    payload = "\n".join(
        f"{name}:{digest}" for name, digest in sorted(hashes.items())
    ).encode("utf-8")
    return sha256(payload).hexdigest()[:16]


def write_provenance(out_dir: Path) -> dict:
    out_dir = Path(out_dir)
    immutable = immutable_hashes(out_dir)
    mutable = mutable_hashes(out_dir)
    provenance = {
        "build_id": build_id_from_hashes(immutable),
        "files": immutable,
        "mutable_files": mutable,
    }
    (out_dir / "build_provenance.json").write_text(
        json.dumps(provenance, indent=2) + "\n",
        encoding="utf-8",
    )
    return provenance


def load_provenance(out_dir: Path) -> dict:
    path = Path(out_dir) / "build_provenance.json"
    if not path.exists():
        raise GeneratedProjectMismatchError(
            f"Missing generated-project provenance file: {path}"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def _normalise_legacy_provenance(provenance: dict) -> dict:
    """Return a verification view compatible with pre-SR-021G manifests.

    SR-021C through SR-021F recorded ``.kicad_pro`` inside the immutable
    ``files`` map and included it in the Build ID.  SR-021G correctly
    reclassified the editor-owned project file as mutable, but accepted
    repositories can still contain an older provenance document.

    Verification migrates that document in memory: mutable project entries
    move out of the immutable set and the expected immutable Build ID is
    recalculated.  The provenance file on disk is not rewritten.
    """
    normalised = dict(provenance)
    immutable = dict(normalised.get("files", {}))
    mutable = dict(normalised.get("mutable_files", {}))
    migrated = []

    for name in list(immutable):
        if Path(name).suffix in MUTABLE_PROJECT_SUFFIXES:
            mutable.setdefault(name, immutable.pop(name))
            migrated.append(name)

    if migrated:
        normalised["legacy_build_id"] = normalised.get("build_id")
        normalised["files"] = immutable
        normalised["mutable_files"] = mutable
        normalised["build_id"] = build_id_from_hashes(immutable)
        normalised["provenance_migrated"] = sorted(migrated)
    else:
        normalised["provenance_migrated"] = []

    return normalised


def verify_generated_project(out_dir: Path) -> dict:
    require_closed_kicad_session(out_dir)
    expected = _normalise_legacy_provenance(load_provenance(out_dir))
    actual_hashes = immutable_hashes(out_dir)
    expected_hashes = expected.get("files", {})
    actual_mutable = mutable_hashes(out_dir)
    expected_mutable = expected.get("mutable_files", {})

    missing = sorted(set(expected_hashes) - set(actual_hashes))
    unexpected = sorted(set(actual_hashes) - set(expected_hashes))
    changed = sorted(
        name for name in set(expected_hashes) & set(actual_hashes)
        if expected_hashes[name] != actual_hashes[name]
    )
    actual_build_id = build_id_from_hashes(actual_hashes)

    mutable_changed = sorted(
        name for name in set(expected_mutable) & set(actual_mutable)
        if expected_mutable[name] != actual_mutable[name]
    )
    expected["mutable_changes"] = mutable_changed

    if missing or unexpected or changed or actual_build_id != expected.get("build_id"):
        details = []
        if missing:
            details.append("missing=" + ",".join(missing))
        if unexpected:
            details.append("unexpected=" + ",".join(unexpected))
        if changed:
            details.append("changed=" + ",".join(changed))
        if actual_build_id != expected.get("build_id"):
            details.append(
                f"build_id={actual_build_id} expected={expected.get('build_id')}"
            )
        raise GeneratedProjectMismatchError(
            "Generated KiCad project does not match its build provenance: "
            + "; ".join(details)
        )
    return expected

"""Engineering-model-driven build orchestration for Foundry.

The dispatcher owns orchestration only. Detailed circuit knowledge remains in
existing block builders, which are registered explicitly by functional-block ID.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable
import json

from generator.build_provenance import (
    require_closed_kicad_session,
    write_provenance,
)

from generator.blocks.balanced_input import add_sch101_diff_converter_slice
from generator.blocks.power_entry import add_power_entry
from generator.blocks.replay_eq import add_replay_equalisation
from generator.blocks.rumble_filter import add_rumble_filter
from generator.blocks.final_gain import add_final_gain
from generator.blocks.mode_matrix import add_mode_matrix
from generator.blocks.balanced_output import add_balanced_output
from generator.blocks.controls import add_controls
from generator.core.sheet import Sheet
from generator.model.core import FunctionalBlock, ProjectModel
from generator.model.validation import validate_project
from generator.annotation import validate_unique_references
from generator.hierarchy import child_hierarchical_ports, sheet_instance_path
from generator.writers.kicad9 import (
    clean_output,
    write_project,
    write_root_schematic,
    write_schematic,
)


SheetBuilder = Callable[[Sheet], None]


@dataclass(frozen=True, slots=True)
class BuilderRegistration:
    block_id: str
    title: str
    builder: SheetBuilder


@dataclass(frozen=True, slots=True)
class BlockBuildResult:
    block_id: str
    name: str
    status: str
    output_file: str | None = None
    detail: str = ""


class BuilderRegistry:
    """Explicit, deterministic map from engineering blocks to proven builders."""

    def __init__(self) -> None:
        self._registrations: dict[str, BuilderRegistration] = {}

    def register(self, block_id: str, title: str, builder: SheetBuilder) -> None:
        if block_id in self._registrations:
            raise ValueError(f"Builder already registered for {block_id}.")
        self._registrations[block_id] = BuilderRegistration(block_id, title, builder)

    def resolve(self, block_id: str) -> BuilderRegistration | None:
        return self._registrations.get(block_id)

    def registered_ids(self) -> set[str]:
        return set(self._registrations)


def shellac_builder_registry() -> BuilderRegistry:
    registry = BuilderRegistry()
    registry.register(
        "SCH101",
        "Project Shellac — SCH-101 Balanced Input",
        add_sch101_diff_converter_slice,
    )
    registry.register(
        "SCH103",
        "Project Shellac — SCH-103 Replay Equalisation",
        add_replay_equalisation,
    )
    registry.register(
        "SCH104",
        "Project Shellac — SCH-104 Final Gain and Buffer",
        add_final_gain,
    )
    registry.register(
        "SCH105",
        "Project Shellac — SCH-105 Channel Mode Matrix",
        add_mode_matrix,
    )
    registry.register(
        "SCH108",
        "Project Shellac — SCH-108 Balanced Output and Mute",
        add_balanced_output,
    )
    registry.register(
        "SCH107",
        "Project Shellac — SCH-107 Rumble Filter",
        add_rumble_filter,
    )
    registry.register(
        "SCH106",
        "Project Shellac — SCH-106 Audio-box Power Entry",
        add_power_entry,
    )
    registry.register(
        "SCH109",
        "Project Shellac — SCH-109 Controls and User Interface",
        add_controls,
    )
    return registry


def _sheet_filename(project_name: str, block: FunctionalBlock) -> str:
    return f"{project_name}_{block.identifier}.kicad_sch"


def write_build_manifest(
    project: ProjectModel,
    results: list[BlockBuildResult],
    out_dir: Path,
    *,
    provenance: dict | None = None,
) -> None:
    manifest = {
        "project": project.name,
        "model_revision": project.revision,
        "functional_blocks": len(list(project.all_blocks())),
        "implemented": sum(result.status == "implemented" for result in results),
        "pending": sum(result.status == "pending" for result in results),
        "root_schematic": "ProjectShellac.kicad_sch",
        "blocks": [asdict(result) for result in results],
        "build_id": provenance["build_id"] if provenance else None,
        "generated_file_hashes": provenance["files"] if provenance else {},
    }
    (out_dir / "build_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        project.name,
        project.revision,
        "",
        "Functional blocks",
        "-----------------",
    ]
    for result in results:
        marker = "[OK]" if result.status == "implemented" else "[--]"
        suffix = f" -> {result.output_file}" if result.output_file else ""
        lines.append(f"{marker} {result.block_id} {result.name}: {result.status}{suffix}")
    lines.extend(
        [
            "",
            f"Implemented: {manifest['implemented']}",
            f"Pending: {manifest['pending']}",
            f"Build ID: {manifest['build_id'] or 'not recorded'}",
        ]
    )
    (out_dir / "build_manifest.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_project_from_model(
    project: ProjectModel,
    registry: BuilderRegistry,
    *,
    out_dir: Path,
    project_name: str,
    clean: bool = True,
) -> list[BlockBuildResult]:
    """Validate and render every currently implemented functional block."""

    validate_project(project)

    # Rebuilding underneath an open KiCad session leaves KiCad's in-memory
    # hierarchy stale while the files on disk change. Native ERC would then
    # describe a different design from the repository. Refuse that state.
    require_closed_kicad_session(out_dir)
    if clean:
        clean_output(out_dir)
    write_project(project_name, out_dir)

    results: list[BlockBuildResult] = []
    generated_sheets: list[tuple[str, Sheet, FunctionalBlock, str, tuple]] = []
    for block in project.blocks:
        registration = registry.resolve(block.identifier)
        if registration is None:
            results.append(
                BlockBuildResult(
                    block_id=block.identifier,
                    name=block.name,
                    status="pending",
                    detail="No builder registered.",
                )
            )
            continue

        filename = _sheet_filename(project_name, block)
        sheet = Sheet(title=registration.title, filename=filename)
        registration.builder(sheet)
        ports = child_hierarchical_ports(sheet, block)
        generated_sheets.append((block.identifier, sheet, block, filename, ports))

    validate_unique_references(
        (block_id, sheet)
        for block_id, sheet, _block, _filename, _ports in generated_sheets
    )

    for block_id, sheet, block, filename, ports in generated_sheets:
        write_schematic(
            sheet,
            out_dir / filename,
            hierarchical_ports=ports,
            instance_path=sheet_instance_path(project_name, block.identifier),
        )
        results.append(
            BlockBuildResult(
                block_id=block.identifier,
                name=block.name,
                status="implemented",
                output_file=filename,
                detail=block.implementation_ref or "Registered builder.",
            )
        )

    block_files = {
        result.block_id: result.output_file
        for result in results
        if result.output_file is not None
    }
    if len(block_files) == len(project.blocks):
        write_root_schematic(
            project,
            block_files,
            out_dir / f"{project_name}.kicad_sch",
            project_name,
        )

    provenance = write_provenance(out_dir)
    write_build_manifest(project, results, out_dir, provenance=provenance)
    return results

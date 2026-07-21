from generator.dispatch import shellac_builder_registry
from generator.model.shellac import build_shellac_model
from generator.readiness import audit_project


def test_all_eight_model_blocks_have_registered_builders():
    project = build_shellac_model()
    registry = shellac_builder_registry()
    assert registry.registered_ids() == {block.identifier for block in project.blocks}


def test_readiness_audit_does_not_mistake_functional_sheets_for_connected_schematics():
    audit = audit_project(build_shellac_model(), shellac_builder_registry())
    assert audit.cad_ready is False
    assert len(audit.blocks) == 8
    assert not any("root hierarchical schematic" in item for item in audit.project_blockers)
    assert not any("symbol-cache/library resolution" in item for item in audit.project_blockers)
    assert not any("reference annotation" in item for item in audit.project_blockers)
    assert any("electrical-rules checking" in item for item in audit.project_blockers)
    assert audit.hierarchical_sheets == 8
    assert audit.hierarchical_pins == 66
    assert audit.cross_sheet_signals == 19


def test_only_existing_wired_slices_have_nonzero_wire_counts():
    audit = audit_project(build_shellac_model(), shellac_builder_registry())
    wire_counts = {block.block_id: block.wires for block in audit.blocks}
    assert wire_counts["SCH101"] > 0
    assert wire_counts["SCH106"] > 0
    assert wire_counts["SCH104"] > 0
    assert wire_counts["SCH103"] > 0


def test_unresolved_custom_symbols_are_reported():
    audit = audit_project(build_shellac_model(), shellac_builder_registry())
    unresolved = {
        symbol
        for block in audit.blocks
        for symbol in block.unresolved_custom_symbols
    }
    assert unresolved == set()


def test_sch104_and_sch105_are_pin_aware_proof_blocks():
    audit = audit_project(build_shellac_model(), shellac_builder_registry())
    by_id = {block.block_id: block for block in audit.blocks}
    assert by_id["SCH104"].cad_ready is True
    assert by_id["SCH104"].wires > 0
    assert by_id["SCH104"].unresolved_custom_symbols == ()
    assert by_id["SCH105"].cad_ready is True
    assert by_id["SCH105"].wires > 0
    assert by_id["SCH105"].unresolved_custom_symbols == ()



def test_sch107_is_pin_aware():
    audit = audit_project(build_shellac_model(), shellac_builder_registry())
    by_id = {block.block_id: block for block in audit.blocks}
    assert by_id["SCH107"].cad_ready is True
    assert by_id["SCH107"].wires > 0
    assert by_id["SCH107"].unresolved_custom_symbols == ()



def test_sch108_is_pin_aware():
    audit = audit_project(build_shellac_model(), shellac_builder_registry())
    by_id = {block.block_id: block for block in audit.blocks}
    assert by_id["SCH108"].cad_ready is True
    assert by_id["SCH108"].wires > 0
    assert by_id["SCH108"].unresolved_custom_symbols == ()



def test_sch101_is_cad_ready_after_dip_symbol_embedding():
    audit = audit_project(build_shellac_model(), shellac_builder_registry())
    by_id = {block.block_id: block for block in audit.blocks}
    assert by_id["SCH101"].cad_ready is True
    assert by_id["SCH101"].wires > 0
    assert by_id["SCH101"].unresolved_custom_symbols == ()


def test_sch109_is_pin_aware():
    audit=audit_project(build_shellac_model(),shellac_builder_registry()); b={x.block_id:x for x in audit.blocks}["SCH109"]
    assert b.cad_ready is True and b.wires>0 and b.unresolved_custom_symbols==()


def test_sch103_is_pin_aware():
    audit = audit_project(build_shellac_model(), shellac_builder_registry())
    block = {item.block_id: item for item in audit.blocks}["SCH103"]
    assert block.cad_ready is True
    assert block.wires > 0
    assert block.unresolved_custom_symbols == ()


def test_zero_native_erc_findings_closes_schematic_readiness_gate():
    audit = audit_project(
        build_shellac_model(), shellac_builder_registry(), erc_violations=0
    )
    assert audit.cad_ready is True
    assert audit.project_blockers == ()


def test_native_erc_findings_remain_a_project_blocker():
    audit = audit_project(
        build_shellac_model(), shellac_builder_registry(), erc_violations=2
    )
    assert audit.cad_ready is False
    assert "2 violation(s)" in audit.project_blockers[0]


def test_machine_readiness_does_not_imply_human_reviewability():
    audit = audit_project(
        build_shellac_model(),
        shellac_builder_registry(),
        erc_violations=0,
        human_reviewable_block_ids={"SCH104"},
    )
    by_id = {block.block_id: block for block in audit.blocks}

    assert audit.cad_ready is True
    assert audit.human_review_ready is False
    assert audit.human_reviewable_blocks == 1
    assert by_id["SCH104"].human_reviewable is True
    assert by_id["SCH101"].human_reviewable is False


def test_human_review_gate_closes_only_when_every_block_is_reviewable():
    project = build_shellac_model()
    audit = audit_project(
        project,
        shellac_builder_registry(),
        erc_violations=0,
        human_reviewable_block_ids={block.identifier for block in project.blocks},
    )

    assert audit.human_review_ready is True
    assert audit.human_reviewable_blocks == 8


def test_sr020_human_reviewable_set_includes_power_entry():
    audit = audit_project(
        build_shellac_model(),
        shellac_builder_registry(),
        erc_violations=0,
        human_reviewable_block_ids={"SCH101", "SCH104", "SCH106"},
    )
    by_id = {block.block_id: block for block in audit.blocks}

    assert audit.human_reviewable_blocks == 3
    assert by_id["SCH106"].human_reviewable is True
    assert audit.human_review_ready is False


def test_sr021_human_reviewable_set_includes_rumble_filter():
    audit = audit_project(
        build_shellac_model(),
        shellac_builder_registry(),
        erc_violations=0,
        human_reviewable_block_ids={"SCH101", "SCH104", "SCH106", "SCH107"},
    )
    by_id = {block.block_id: block for block in audit.blocks}

    assert audit.human_reviewable_blocks == 4
    assert by_id["SCH107"].human_reviewable is True
    assert audit.human_review_ready is False


def test_sr022_human_reviewable_set_includes_mode_matrix():
    audit = audit_project(
        build_shellac_model(),
        shellac_builder_registry(),
        erc_violations=0,
        human_reviewable_block_ids={
            "SCH101", "SCH104", "SCH105", "SCH106", "SCH107"
        },
    )
    by_id = {block.block_id: block for block in audit.blocks}

    assert audit.human_reviewable_blocks == 5
    assert by_id["SCH105"].human_reviewable is True
    assert audit.human_review_ready is False


def test_sr023_human_reviewable_set_includes_balanced_output():
    audit = audit_project(
        build_shellac_model(),
        shellac_builder_registry(),
        erc_violations=0,
        human_reviewable_block_ids={
            "SCH101", "SCH104", "SCH105", "SCH106", "SCH107", "SCH108"
        },
    )
    by_id = {block.block_id: block for block in audit.blocks}

    assert audit.human_reviewable_blocks == 6
    assert by_id["SCH108"].human_reviewable is True
    assert audit.human_review_ready is False


def test_sr025_human_reviewable_set_closes_gate_2b():
    project = build_shellac_model()
    audit = audit_project(
        project,
        shellac_builder_registry(),
        erc_violations=0,
        human_reviewable_block_ids={block.identifier for block in project.blocks},
    )
    by_id = {block.block_id: block for block in audit.blocks}
    assert audit.human_reviewable_blocks == 8
    assert by_id["SCH109"].human_reviewable is True
    assert audit.human_review_ready is True

from pathlib import Path

from generator.mechanical.board_outline import (
    OutlineStatus,
    build_provisional_outline_contract,
)
from generator.mechanical.board_skeleton import (
    render_board_skeleton,
    validate_board_skeleton_text,
    write_board_skeleton,
)


def test_provisional_board_skeleton_is_four_layer_and_has_no_holes():
    contract = build_provisional_outline_contract()
    text = render_board_skeleton(contract)
    assert '(0 "F.Cu" signal)' in text
    assert '(2 "In1.Cu" signal)' in text
    assert '(4 "In2.Cu" signal)' in text
    assert '(31 "B.Cu" signal)' in text
    assert text.count('(footprint "ProjectShellac:MountingHole"') == 0
    assert "PROVISIONAL — NOT FOR MANUFACTURE" in text
    assert validate_board_skeleton_text(text, contract) == []


def test_board_skeleton_contains_closed_outline_and_all_regions():
    text = render_board_skeleton()
    assert text.count('(layer "Edge.Cuts")') == 4
    for region_id in ("REG-01", "REG-02", "REG-03", "REG-04", "REG-05", "REG-06", "REG-07"):
        assert region_id in text


def test_write_board_skeleton_reports_provisional_contract(tmp_path: Path):
    out = tmp_path / "ProjectShellac_Provisional.kicad_pcb"
    result = write_board_skeleton(out)
    assert out.exists()
    assert result.state == OutlineStatus.PROVISIONAL.value
    assert result.outline_width_mm == 220.0
    assert result.outline_depth_mm == 140.0
    assert result.mounting_hole_count == 0
    assert result.region_count >= 7


def test_provisional_skeleton_keeps_orientation_contract():
    text = render_board_skeleton()
    assert "Right edge = cartridge inputs" in text
    assert "Left edge = balanced outputs and DC entry" in text


def test_board_skeleton_uses_numeric_ids_for_user_layers():
    text = render_board_skeleton()
    assert '(40 "Dwgs.User" user "user.drawings")' in text
    assert '(41 "Cmts.User" user "user.comments")' in text
    assert '\n    (Dwgs.User ' not in text
    assert '\n    (Cmts.User ' not in text


def test_board_skeleton_validator_rejects_non_numeric_layer_entry():
    contract = build_provisional_outline_contract()
    text = render_board_skeleton(contract).replace(
        '(40 "Dwgs.User" user "user.drawings")',
        '(Dwgs.User user "user.drawings")',
    )
    issues = validate_board_skeleton_text(text, contract)
    assert any("numeric index" in issue for issue in issues)

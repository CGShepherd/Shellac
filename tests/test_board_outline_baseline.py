from dataclasses import replace

import pytest

from generator.mechanical import build_mechanical_baseline
from generator.mechanical.board_outline import (
    OutlineStatus,
    build_provisional_outline_contract,
    derive_frozen_outline_contract,
    validate_outline_contract,
)
from generator.mechanical.freeze import DrawingEvidence, derive_carrier_freeze


def _verified_carrier():
    candidate = next(
        item for item in build_mechanical_baseline().candidates
        if item.identifier == "ENC-A03"
    )
    verified = replace(candidate, internal_width_mm=250.0, internal_depth_mm=160.0)
    evidence = DrawingEvidence(True, True, True, True, True, "manufacturer-drawing-rev-1")
    return derive_carrier_freeze(verified, evidence)


def test_provisional_contract_never_invents_mounting_holes():
    contract = build_provisional_outline_contract()
    assert contract.status is OutlineStatus.PROVISIONAL
    assert contract.mounting_holes == []
    assert contract.unresolved_inputs
    assert validate_outline_contract(contract) == []


def test_frozen_contract_derives_four_symmetric_nonplated_holes():
    contract = derive_frozen_outline_contract(_verified_carrier())
    assert contract.status is OutlineStatus.FROZEN
    assert len(contract.mounting_holes) == 4
    assert all(not hole.plated for hole in contract.mounting_holes)
    assert [(h.centre.x_mm, h.centre.y_mm) for h in contract.mounting_holes] == [
        (8.0, 8.0),
        (212.0, 8.0),
        (212.0, 132.0),
        (8.0, 132.0),
    ]
    assert validate_outline_contract(contract) == []


def test_outline_rejects_unfrozen_carrier():
    carrier = replace(_verified_carrier(), status="PROVISIONAL")
    with pytest.raises(ValueError):
        derive_frozen_outline_contract(carrier)


def test_outline_rejects_hole_keepout_outside_board():
    with pytest.raises(ValueError):
        derive_frozen_outline_contract(_verified_carrier(), hole_inset_x_mm=2.0)

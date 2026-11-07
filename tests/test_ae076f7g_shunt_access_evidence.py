"""Fast, offline CI checks. Native FreeCAD qualification is a separate required gate."""
from copy import deepcopy
import json
from pathlib import Path

import pytest
import yaml

from generator.mechanical.qualification_register import (
    EvidenceContractError, RECORD, STUDIES, file_hash, validate_register,
)

ROOT = Path(__file__).resolve().parents[1]


def register():
    return yaml.safe_load((ROOT / RECORD).read_text(encoding='utf-8'))


def test_u1_u5_provenance_and_current_authority_are_fail_closed():
    result = validate_register(ROOT)
    assert result == {'classification': 'NONBINDING_HISTORICAL_SHADOW',
                      'studies_indexed': len(STUDIES), 'reports_byte_verified': False,
                      'release_authorised': False}


@pytest.mark.parametrize('field,value', [
    ('classification', 'PROMOTED'),
    ('current_mechanical_authority', 'AE-076F7G'),
    ('historical_F6H_study_board_outline_mm', [220, 148]),
])
def test_never_promote_historical_shadows_without_authority(field, value):
    r = deepcopy(register())
    r[field] = value
    with pytest.raises(EvidenceContractError):
        validate_register(ROOT, r)


def test_current_board_change_invalidates_snapshot():
    r = deepcopy(register())
    r['current_board']['sha256'] = '0' * 64
    with pytest.raises(EvidenceContractError, match='PCB differs'):
        validate_register(ROOT, r)


def test_open_native_service_and_structural_qualifications_cannot_be_self_closed():
    r = deepcopy(register())
    r['remaining_qualifications']['real_hand_grip_and_shunt_service'] = 'PASS'
    with pytest.raises(EvidenceContractError, match='marked closed'):
        validate_register(ROOT, r)


def test_optional_report_byte_check_and_tamper_fail_closed(tmp_path):
    with pytest.raises(EvidenceContractError, match='cannot hash'):
        validate_register(ROOT, reports_dir=tmp_path)
    r = deepcopy(register())
    # Synthetic reports validate the verifier, not the historical FreeCAD results.
    for item in r['study_results'].values():
        path = tmp_path / item['filename']
        path.write_text(json.dumps({'status': item['status']}), encoding='utf-8')
        item['sha256'] = file_hash(path)
    assert validate_register(ROOT, r, reports_dir=tmp_path)['reports_byte_verified'] is True
    (tmp_path / r['study_results']['U5']['filename']).write_text('{}', encoding='utf-8')
    with pytest.raises(EvidenceContractError, match='report bytes mismatch'):
        validate_register(ROOT, r, reports_dir=tmp_path)


def test_live_release_holds_cannot_be_inferred_from_geometry():
    r = deepcopy(register())
    r['release_claims']['manufacturing_release'] = True
    with pytest.raises(EvidenceContractError, match='release hold'):
        validate_register(ROOT, r)


def test_historical_geometry_not_current_manufacturing_authority():
    r = deepcopy(register())
    assert r['U5_historical_candidate']['R3_new_cut_xy_mm'] == [145, 12, 211, 60]
    assert r['U5_historical_candidate']['projected_26mm_gauges']['PARK_O10_CENTRED'] == 'BLOCKED'
    assert r['selected_next_board_outline_mm'] != r['historical_F6H_study_board_outline_mm']
    r['U5_historical_candidate']['status'] = 'RELEASED_FOR_FAB'
    with pytest.raises(EvidenceContractError, match='candidate promoted'):
        validate_register(ROOT, r)

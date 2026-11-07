"""Fail-closed index of *nonbinding* mechanical evidence (NOT native MCAD qualification).

Fast CI validates source provenance and authority boundaries. Actual BREP and service
checks must run separately, against the then-current assembly, before promotion.
"""
from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
from typing import Mapping

import yaml

RECORD = Path('config/mechanical/ae076f7g_shunt_access_evidence.yaml')
HOLDS = ('final_routing', 'layout_freeze', 'bom_freeze', 'manufacturing_release')
STUDIES = ('U1', 'U2', 'U3', 'U4R', 'U5')
_SHA256 = re.compile(r'[0-9a-f]{64}\Z')


class EvidenceContractError(ValueError):
    """Missing, inconsistent or overstated evidence; never authorises release."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceContractError(message)


def load_yaml(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding='utf-8'))
    except (OSError, yaml.YAMLError) as exc:
        raise EvidenceContractError(f'unreadable YAML {path}: {exc}') from exc
    require(isinstance(data, dict), f'YAML not a mapping: {path}')
    return data


def file_hash(path: Path) -> str:
    try:
        with path.open('rb') as stream:
            digest = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
            return digest.hexdigest()
    except OSError as exc:
        raise EvidenceContractError(f'cannot hash {path}: {exc}') from exc


def valid_hash(value: object) -> bool:
    return isinstance(value, str) and _SHA256.fullmatch(value) is not None


def validate_register(root: Path, record: Mapping | None = None,
                      reports_dir: Path | None = None) -> dict:
    """Verify provenance and release holds; optional reports must match exact bytes.

    This deliberately does NOT claim that a historical STEP applies to today's PCB.
    """
    root = Path(root)
    r = dict(record) if record is not None else load_yaml(root / RECORD)
    require(r.get('schema_version') == 1 and r.get('project') == 'Shellac', 'invalid evidence schema')
    require(r.get('classification') == 'NONBINDING_HISTORICAL_SHADOW', 'evidence illegally promoted')
    require(r.get('current_mechanical_authority') == 'AE-076B', 'mechanical authority changed: review needed')
    b = r.get('current_board', {})
    require(b.get('path') == 'out/kicad/ProjectShellac.kicad_pcb', 'PCB path changed')
    require(valid_hash(b.get('sha256')), 'invalid PCB hash')
    require(file_hash(root / b['path']) == b['sha256'], 'PCB differs from evidence baseline; regenerate and review')
    require(b.get('outline_mm') == [220, 140], 'historical governed outline mislabelled')
    require(r.get('selected_next_board_outline_mm') == [220, 148], 'selected-next outline changed; review contract')
    require(r.get('historical_F6H_study_board_outline_mm') == [228, 156], 'historical F6H outline changed')
    for key in ('historical_F6H_step_sha256', 'metcase_step_sha256', 'handover_rev_A20_sha256'):
        require(valid_hash(r.get(key)), f'invalid {key}')
    old = load_yaml(root / 'config/mechanical/ae076b_control_service_module.yaml')
    require(old.get('authority') == 'AE-076B', 'governed current mechanical authority has changed')
    require(old.get('selected_architecture', {}).get('aluminium_carrier') == 'NOT_SELECTED',
            'current authority no longer matches nonbinding evidence')
    require(old.get('permissions', {}).get('native_pcb_mechanical_migration') is False,
            'governed mechanical migration permission changed')
    m = load_yaml(root / 'config/mechanical/ae076b2c_mcad_sources.yaml')
    require(m.get('metcase_enclosure', {}).get('step_sha256') == r['metcase_step_sha256'],
            'Metcase provenance disagrees with controlled source')
    release = load_yaml(root / 'config/release/ae071_prerouting_hold.yaml')
    claims = r.get('release_claims', {})
    require(claims.get('native_pcb_mechanical_migration') is False,
            'register claims native PCB migration release')
    require(all(claims.get(k) is False and release.get('permissions', {}).get(k) is False
                for k in HOLDS), 'live release hold or register claim changed')
    require(all(old.get('permissions', {}).get(k) is False for k in HOLDS),
            'mechanical authority holds changed')
    q = r.get('remaining_qualifications')
    require(isinstance(q, dict) and len(q) >= 8 and all(v == 'OPEN' for v in q.values()),
            'unqualified mechanical evidence marked closed')
    result = r.get('study_results', {})
    require(isinstance(result, dict) and set(result) == set(STUDIES), 'study chain incomplete or unexpected')
    for name in STUDIES:
        item = result[name]
        require(isinstance(item, dict) and set(item) == {'filename', 'sha256', 'status'},
                f'{name} bad report contract')
        require(item['filename'].startswith('SHELLAC_F7G_I7C_' + name + '_')
                and item['filename'].endswith('_READONLY.json') and '/' not in item['filename']
                and '\\' not in item['filename'], f'{name} unsafe report name')
        require(valid_hash(item['sha256']), f'{name} invalid SHA256')
        require(isinstance(item['status'], str) and item['status'].startswith('PASS_')
                and ('HELD' in item['status'] or 'SHADOW' in item['status']),
                f'{name} invalid nonbinding status')
    candidate = r.get('U5_historical_candidate', {})
    require(candidate.get('status') == 'PROPOSED_NOT_AUTHORISED_FOR_CAD_OR_FAB', 'candidate promoted')
    require(candidate.get('R3_new_cut_xy_mm') == [145, 12, 211, 60], 'U5 evidence geometry changed')
    require(candidate.get('joined_existing_windows') == ['W8', 'W2'], 'U5 aperture identity changed')
    require(abs(candidate.get('additional_removed_area_per_leaf_mm2', -1) - 1648.362833) < 0.001,
            'U5 area evidence changed')
    require(candidate.get('projected_26mm_gauges') == {
        'LOW_P01_CENTRED': 'CLEAR', 'HIGH_H111_CENTRED': 'CLEAR',
        'PARK_O10_NORTH_APPROACH': 'CLEAR', 'PARK_O10_CENTRED': 'BLOCKED'},
            'U5 projection or negative control changed')
    if reports_dir is not None:
        from json import loads
        for name in STUDIES:
            item = result[name]
            path = Path(reports_dir) / item['filename']
            require(file_hash(path) == item['sha256'], f'{name} report bytes mismatch')
            try:
                report = loads(path.read_text(encoding='utf-8'))
            except (OSError, ValueError) as exc:
                raise EvidenceContractError(f'{name} invalid JSON: {exc}') from exc
            require(report.get('status') == item['status'], f'{name} report result mismatch')
    return {'classification': r['classification'], 'studies_indexed': len(STUDIES),
            'reports_byte_verified': reports_dir is not None, 'release_authorised': False}


def main() -> int:
    parser = argparse.ArgumentParser(description='Audit Shellac nonbinding native mechanical evidence')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--reports-dir', type=Path,
                        help='optional Dropbox staging reports folder: all five exact JSON files required')
    args = parser.parse_args()
    try:
        state = validate_register(args.root, reports_dir=args.reports_dir)
    except EvidenceContractError as exc:
        print(f'HOLD mechanical evidence: {exc}')
        return 1
    print(f'PASS nonbinding evidence register: {state}; no design or release permission granted')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

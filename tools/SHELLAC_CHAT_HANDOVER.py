#!/usr/bin/env python3
"""Dynamic, non-authoritative Shellac chat handover; reads controlled status.

Replaces the previous stale AE-076B2B static snapshot. This tool is deliberately
read-only and must NEVER represent its output as electrical/mechanical release.
"""
from pathlib import Path
import argparse
import json
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / 'config/decisions/current_spec_manifest.yaml'


def _git(*args):
    p = subprocess.run(['git', *args], cwd=ROOT, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.returncode, p.stdout.strip()


def current_status():
    r, branch = _git('branch', '--show-current')
    h, head = _git('rev-parse', 'HEAD')
    o, origin = _git('rev-parse', 'origin/develop')
    s, dirty = _git('status', '--porcelain=v1', '--untracked-files=all')
    if any(c != 0 for c in (r,h,o,s)):
        raise RuntimeError('Git status unavailable; fail closed')
    return {
        'branch': branch, 'head': head, 'origin_develop': origin,
        'head_equals_origin_develop': head == origin,
        'working_tree_clean': dirty == '',
        'working_tree_status': dirty.splitlines(),
        'governed_develop_ready': branch == 'develop' and head == origin and dirty == '',
    }


def payload():
    if not SPEC.is_file():
        raise RuntimeError('Current specification manifest missing')
    manifest = yaml.safe_load(SPEC.read_text(encoding='utf-8'))
    hold = yaml.safe_load((ROOT/'config/release/ae071_prerouting_hold.yaml').read_text(encoding='utf-8'))
    index = yaml.safe_load((ROOT/'config/decisions/current_decision_index.yaml').read_text(encoding='utf-8'))
    key = manifest['record'].replace('S35B-S14', 'AE-076F7H-S14')
    if index['decisions'][key]['primary_record'] != manifest['specification']:
        raise RuntimeError('Spec/index authority mismatch')
    if any(hold['permissions'].get(x) is not False for x in (
        'final_routing','layout_freeze','bom_freeze','manufacturing_release')):
        raise RuntimeError('Unexpected manufacturing permission; STOP')
    return {
        'project': 'Shellac',
        'classification': 'PROCESS_CONTINUITY_ONLY_NOT_DESIGN_AUTHORITY',
        'repository': current_status(),
        'current_specification': manifest['specification'],
        'current_spec_record': manifest['record'],
        'current_implementation': manifest['baseline'],
        'selected_next': manifest['mechanical_selected_next'],
        'matrix': manifest['channel_matrix'],
        'release_holds': {k: hold['permissions'][k] for k in (
            'final_routing','layout_freeze','bom_freeze','manufacturing_release')},
        'next_engineering_transaction': manifest['next_engineering_transaction'],
        'read_first': ['PROJECT_GUIDANCE.md','PROJECT_SHELLAC_WORKING_STATE.md',
            'config/decisions/current_decision_index.yaml',manifest['specification'],
            'config/release/ae071_prerouting_hold.yaml'],
        'interaction_mode': 'NORMAL_CHAT_ONLY_NO_WORK_OR_CODEX',
        'required_response_tail': ['Confidence: NN%', 'Chat runway: ...'],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    data = payload()
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print('=== PROJECT SHELLAC CONTROLLED CHAT HANDOVER ===')
        print('NOT engineering release or fabrication approval')
        print('Git branch:', data['repository']['branch'])
        print('HEAD:', data['repository']['head'])
        print('origin/develop:', data['repository']['origin_develop'])
        print('Governed develop ready:', data['repository']['governed_develop_ready'])
        print('Current spec:', data['current_specification'])
        print('Matrix:', data['matrix']['selected_mpn'],
              f"{data['matrix']['poles']}P{data['matrix']['positions']}T")
        print('Selected-next Rumble/Mute:', data['selected_next']['mute_rumble_mpn'])
        print('Release holds:', data['release_holds'])
        print('Next:', data['next_engineering_transaction'])
        print('READ FIRST:', ', '.join(data['read_first']))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

"""Validate GH-001 design examples; never call Git, gh, GitHub or credentials."""

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(name):
    return json.loads((ROOT / 'contracts' / name).read_text(encoding='utf-8'))


def design_authority(policy, request):
    return (
        request['actor'] == 'controller' and request['authorized']
        and request['same_principal'] and request['same_repository']
        and not request['cancelled'] and request['action'] in policy['allowed_actions']
        and request['head_ref'].startswith(policy['branch_prefix'])
        and request['head_ref'] == request['authorized_head_ref']
        and request['head_ref'] not in {request['base_ref'], request['default_ref']}
    )


def design_reconciliation(intent, case):
    """Model PR-create lookup results; booleans/rows are synthetic, not observations."""
    if not case['scan_complete']:
        return 'blocked_incomplete'
    rows = case['candidates']
    if not rows:
        return 'create' if case['dispatch_state'] == 'not_dispatched' else 'blocked_unknown'
    if len(rows) != 1:
        return 'blocked_ambiguous'
    observed = rows[0]
    if (type(observed.get('number')) is not int or observed['number'] < 1
            or not isinstance(observed.get('node_id'), str) or not observed['node_id']):
        return 'blocked_conflict'
    matches = all(observed[field] == intent[field] for field in
                  ['repository_id', 'base_ref', 'base_sha', 'head_ref', 'head_sha', 'marker'])
    if (not matches or observed['head_repository_id'] != intent['repository_id']
            or observed['author_id'] != intent['principal_id']):
        return 'blocked_conflict'
    if observed['state'] in {'closed', 'merged'}:
        return 'blocked_terminal'
    return 'reuse' if observed['state'] == 'open' else 'blocked_unknown'


def design_delivery_gate(observation):
    flags = ['local_checks', 'qa', 'security', 'lead', 'native_manifest',
             'inputs_current', 'human_accepted', 'pr_observed_ready']
    checks = observation['native_checks']
    return (all(observation[key] for key in flags) and bool(checks)
            and all(check['conclusion'] == 'success' and check['identity_matches']
                    and check['revision_matches'] and check['unique_current_attempt']
                    for check in checks))


def main():
    policy = load('github-delivery.json')
    schema = load('github-delivery.schema.json')
    protocol = load('protocol.schema.json')
    limits = load('execution-limits.json')
    examples = load('github-delivery.examples.json')
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(policy)
    for name in ['Id', 'Digest', 'Revision', 'ArtifactRef']:
        require(schema['$defs'][name] == protocol['$defs'][name], 'Canonical type drift')
    require(policy['binding'] is None and policy['required_checks'] is None,
            'Design must not invent mission authorization or configured checks')
    require(set(policy['allowed_actions']).isdisjoint(policy['denied_actions']), 'Ambiguous authority')
    require(len(set(policy['allowed_actions'])) == len(policy['allowed_actions']) == 5,
            'Unexpected publication capability')
    require(set(policy['allowed_actions']) == {'create_branch', 'push_fast_forward',
            'create_draft_pr', 'convert_to_draft', 'mark_ready'}, 'Added write authority')
    require(policy['github_deadline_ref'] == 'time.github_seconds'
            and limits['time']['github_seconds'] == 30, 'GitHub deadline drift')
    require(policy['lookup'] == {'page_size': 100, 'max_pages': 2,
                                'max_observations_per_wait': 6}, 'Unbounded lookup')
    intent_validator = Draft202012Validator({**schema, '$ref': '#/$defs/PublicationIntent'})
    intent = examples['intent']
    intent_validator.validate(intent)
    require(intent['head_ref'] == policy['branch_prefix'] + intent['mission_id'],
            'Mission branch identity mismatch')
    require(intent['marker'] == '<!-- multifullstackmade:publication:' + intent['operation_key'] + ' -->',
            'Correlation marker mismatch')
    names = [case['name'] for group in ['shape', 'authority', 'reconciliation', 'gates']
             for case in examples[group]]
    require(len(names) == len(set(names)), 'Duplicate delivery example names')
    for case in examples['shape']:
        value = {**copy.deepcopy(intent), **case['changes']}
        require(intent_validator.is_valid(value) == case['valid'], f'Intent shape: {case["name"]}')
    for case in examples['authority']:
        require(design_authority(policy, case['input']) == case['allow'], f'Authority: {case["name"]}')
    for case in examples['reconciliation']:
        require(design_reconciliation(intent, case) == case['result'],
                f'Reconciliation: {case["name"]}')
    for case in examples['gates']:
        require(design_delivery_gate(case['input']) == case['deliver'], f'Gate: {case["name"]}')
    print(f'PASS: frozen GH-001 policy, private intent schema and {len(names)} synthetic '
          'shape/authority/reconciliation/gate cases; PROTO-001 types unchanged.')
    print('NOT VERIFIED: effective identity/scopes, remote races/replay, draft CI, native '
          'check provenance, real authorization or any GH integration scenario.')


if __name__ == '__main__':
    main()

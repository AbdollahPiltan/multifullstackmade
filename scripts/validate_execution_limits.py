"""Validate LIM-001 fixtures and synthetic calculations, without dispatching work."""

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


def lookup(document, path):
    value = document
    for field in path:
        value = value[field]
    return value


def profile_consistent(profile):
    time = profile['time']
    hierarchy = [time[k] for k in ['model_seconds', 'invocation_seconds',
                                  'task_active_seconds', 'mission_active_seconds',
                                  'mission_lifetime_seconds']]
    return (
        hierarchy == sorted(hierarchy)
        and time['stop_grace_seconds'] <= time['cleanup_seconds']
        and max(profile['checks'].values()) <= time['invocation_seconds']
        and max(time['ordinary_tool_seconds'], time['github_seconds']) <= time['invocation_seconds']
        and profile['invocation']['model_calls'] <= profile['task']['model_calls_per_attempt']
        <= profile['mission']['model_calls']
        and profile['invocation']['tool_calls'] <= profile['task']['tool_calls_per_attempt']
        <= profile['mission']['tool_calls']
        and profile['task']['repair_attempts'] <= profile['mission']['repair_attempts']
        and profile['task']['messages'] <= profile['mission']['messages']
        and profile['tokens']['input_per_call'] + profile['tokens']['output_per_call']
        <= profile['tokens']['mission_total']
        and profile['container']['memory_plus_swap_mib'] == profile['container']['memory_mib']
        and profile['container']['tmpfs_mib'] <= profile['container']['memory_mib']
        and profile['bytes']['control_reserve'] < profile['bytes']['private_project']
        and profile['bytes']['check_logs'] <= profile['bytes']['mission_logs']
    )


def design_admission(profile, charges):
    """Check a synthetic multi-budget vector; not a persistent admission engine."""
    if not charges:
        return False
    seen = set()
    for charge in charges:
        key = tuple(charge['limit'])
        if key in seen:
            return False
        seen.add(key)
        values = [charge[k] for k in ['spent', 'reserved', 'request']]
        if not all(type(value) is int and value >= 0 for value in values):
            return False
        limit = lookup(profile, key)
        if key == ('bytes', 'private_project'):
            limit -= profile['bytes']['control_reserve']
        if sum(values) > limit:
            return False
    return True


def design_retry(profile, observation):
    """Compute example retry waits; no timer, provider or retry loop is started."""
    policy = profile['retry']
    used = observation['dispatches_used']
    if (observation['cancelled'] or not observation['safe'] or not observation['transient']
            or not 1 <= used < policy['max_dispatches']):
        return None
    fraction = observation['jitter_fraction']
    require(0 <= fraction <= 1, 'Invalid synthetic jitter fraction')
    jitter = fraction * min(policy['jitter_cap_seconds'], policy['base_seconds'] * 2 ** (used - 1))
    retry_after = observation['retry_after_seconds']
    delay = max(jitter, max(0, retry_after) if retry_after is not None else 0)
    if delay > policy['max_wait_seconds'] or delay >= observation['seconds_remaining']:
        return None
    return delay


def design_control(profile, observation):
    return (
        not observation['cancelled'] and not observation['unknown_effect']
        and not observation['quiescent_wait']
        and 0 <= observation['lifetime_elapsed_seconds'] < profile['time']['mission_lifetime_seconds']
        and observation['remaining_active_seconds'] > 0
    )


def main():
    profile = load('execution-limits.json')
    schema = load('execution-limits.schema.json')
    examples = load('execution-limits.examples.json')
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    validator.validate(profile)
    require(profile_consistent(profile), 'Inconsistent baseline limits')
    names = [case['name'] for group in ['configuration', 'admission', 'retry', 'control']
             for case in examples[group]]
    require(len(names) == len(set(names)), 'Duplicate example names')
    for case in examples['configuration']:
        candidate = copy.deepcopy(profile)
        if case['path']:
            parent = lookup(candidate, case['path'][:-1])
            parent[case['path'][-1]] = case['value']
        valid = validator.is_valid(candidate) and profile_consistent(candidate)
        require(valid == case['valid'], f'Configuration mismatch: {case["name"]}')
    for case in examples['admission']:
        original = copy.deepcopy(case['charges'])
        require(design_admission(profile, case['charges']) == case['admit'],
                f'Admission mismatch: {case["name"]}')
        require(case['charges'] == original, 'Static check mutated budget observations')
    for case in examples['retry']:
        require(design_retry(profile, case['input']) == case['delay_seconds'],
                f'Retry mismatch: {case["name"]}')
    for case in examples['control']:
        require(design_control(profile, case['input']) == case['admit'],
                f'Control mismatch: {case["name"]}')

    protocol = load('protocol.schema.json')
    branches = protocol['$defs']['ToolRequest']['properties']['call']['oneOf']
    tools = {b['properties']['tool']['const']: b['properties']['arguments'] for b in branches}
    # Cross-check operational defaults against the existing closed transport limits.
    changes = protocol['$defs']['FileChange']['oneOf']
    write = next(c for c in changes if c['properties']['operation']['const'] == 'write')
    require(profile['bytes']['source_file'] <= 4 * write['properties']['content']['maxLength'],
            'File bytes exceed transport character bound')
    require('request_check' in tools, 'Missing check tool')
    api = load('notes.openapi.json')
    require(api['paths']['/api/v1/notes']['get']['parameters'][0]['schema']['maximum'] == 100,
            'Notes page contract drift')
    role_contract = (ROOT / 'docs/PROTOCOL-CONTRACTS.md').read_text(encoding='utf-8')
    require(all(check in role_contract for check in profile['checks']), 'Unknown check profile')
    remaining = protocol['$defs']['Invocation']['properties']['remaining_budget']
    require(set(remaining['properties']) == {'model_calls', 'tool_calls', 'repair_attempts',
                                            'max_output_tokens', 'deadline'}, 'Wire budget changed')
    print(f'PASS: closed LIM-001 profile, cross-limit consistency and {len(names)} synthetic '
          'configuration/admission/retry/control examples; existing wire budget unchanged.')
    print('NOT VERIFIED: durable accounting, actual retries, clocks, cancellation, '
          'tokenizer, container limits, API overload or real runtime enforcement.')


if __name__ == '__main__':
    main()

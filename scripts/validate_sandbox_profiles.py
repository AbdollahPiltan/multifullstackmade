"""Validate SBX-001 design fixtures, not real container or filesystem enforcement."""

import copy
import fnmatch
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(name):
    return json.loads((ROOT / 'contracts' / name).read_text(encoding='utf-8'))


def lookup(document, path):
    result = document
    for field in path:
        result = result[field]
    return result


def design_path_allowed(policy, request):
    """Evaluate synthetic attributes only; no resolve/open or runtime authorization."""
    path = request['path']
    if request['role'] not in set(policy['owners']) | {'lead'}:
        return False
    if (not 1 <= len(path) <= policy['max_characters']
            or not re.fullmatch(r'[A-Za-z0-9_./-]+', path)):
        return False
    components = path.split('/')
    if any(not part or part.startswith('.') for part in components):
        return False
    if (not request['regular'] or request['symlink'] or request['nlink'] != 1
            or request['case_collision']):
        return False
    basename = components[-1].casefold()
    if any(fnmatch.fnmatchcase(part.casefold(), pattern.casefold())
           for part in components for pattern in policy['private_basename_patterns']):
        return False
    if not any(path == grant or path.startswith(grant + '/') for grant in request['grants']):
        return False
    operation = request['operation']
    if operation == 'read':
        roots = [root for values in policy['owners'].values() for root in values]
    elif operation in {'write', 'delete'}:
        roots = policy['owners'].get(request['role'], [])
        if any(fnmatch.fnmatchcase(basename, p.casefold()) for p in policy['shared_basename_patterns']):
            return False
    else:
        return False
    return any(path.startswith(root + '/') for root in roots)


def design_check_allowed(policy, request):
    profile = policy['profiles'].get(request['profile_id'])
    return bool(profile and request['actor'] == request['declared_role']
                and request['actor'] in profile['roles']
                and request['profile_id'] in request['available_check_ids'])


def main():
    policy = load('sandbox-profiles.json')
    schema = load('sandbox-profiles.schema.json')
    limits = load('execution-limits.json')
    protocol = load('protocol.schema.json')
    cases = load('sandbox-profiles.examples.json')
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    validator.validate(policy)
    common = policy['common']
    require(sum(t['size_mib'] for t in common['writable_tmpfs']) == limits['container']['tmpfs_mib'],
            'Tmpfs partitions disagree with LIM-001')
    require(common['driver_uid'] > 0 and common['service_uid'] > 0
            and common['driver_uid'] != common['service_uid'], 'Invalid isolation identities')
    expected_roles = {
        'frontend_unit': {'frontend', 'qa', 'lead'},
        'backend_unit': {'backend', 'qa', 'lead'},
        'api_contract': {'backend', 'qa', 'lead'},
        'qa_integration': {'qa', 'lead'},
        'security_static': {'security', 'lead'},
        'security_negative': {'security', 'lead'},
    }
    require(set(policy['profiles']) == set(limits['checks']) == set(expected_roles), 'Profile ID drift')
    check_tool_roles = set(protocol['x-tool-role-allowlist']['request_check'])
    browsers = set()
    for name, profile in policy['profiles'].items():
        require(set(profile['roles']) == expected_roles[name] <= check_tool_roles, 'Profile authority drift')
        require(profile['deadline_ref'] == 'checks.' + name and limits['checks'][name] > 0,
                'Missing profile deadline')
        require(profile['release'] is None, 'Design fixture must not claim a real release')
        require(profile['harness_id'] == name + '_v1', 'Harness ID drift')
        if profile['browser']:
            browsers.add(name)
            require(profile['seccomp'] == 'browser_userns_reviewed', 'Browser sandbox missing')
        else:
            require(profile['seccomp'] == 'engine_default', 'Default syscall envelope changed')
    require(browsers == {'frontend_unit', 'qa_integration'}, 'Unexpected browser scope')
    require(policy['path_policy']['max_characters'] == protocol['$defs']['RelativePath']['maxLength'],
            'Path-length contract drift')
    require(set(policy['path_policy']['owners']) == set(protocol['x-tool-role-allowlist']['submit_patch']),
            'Path ownership grants a role without patch authority')

    names = [case['name'] for group in ['envelope', 'paths', 'requests'] for case in cases[group]]
    require(len(names) == len(set(names)), 'Duplicate sandbox example names')
    for case in cases['envelope']:
        candidate = copy.deepcopy(policy)
        if case['path']:
            parent = lookup(candidate, case['path'][:-1])
            parent[case['path'][-1]] = case['value']
        require(validator.is_valid(candidate) == case['valid'], f'Envelope mismatch: {case["name"]}')
    for case in cases['paths']:
        require(design_path_allowed(policy['path_policy'], case['input']) == case['allow'],
                f'Path mismatch: {case["name"]}')
    for case in cases['requests']:
        require(design_check_allowed(policy, case) == case['allow'], f'Check mismatch: {case["name"]}')
    print(f'PASS: six frozen design profiles, role/limit/path consistency and {len(names)} '
          'synthetic envelope/path/request examples. All image releases remain unresolved.')
    print('NOT VERIFIED: filesystem races, Docker/Chromium isolation, image/scanner qualification, '
          'effective resources, live permissions or any SB runtime scenario.')


if __name__ == '__main__':
    main()

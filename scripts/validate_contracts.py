"""Validate design contracts and examples; does not execute agents or the API."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from openapi_spec_validator import validate_spec


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / 'contracts' / name).read_text(encoding='utf-8'))


def assert_local_refs(value, document):
    if isinstance(value, dict):
        if '$ref' in value:
            reference = value['$ref']
            assert reference.startswith('#/'), f'Nonlocal reference: {reference}'
            target = document
            for part in reference[2:].split('/'):
                target = target[part.replace('~1', '/').replace('~0', '~')]
        for item in value.values():
            assert_local_refs(item, document)
    elif isinstance(value, list):
        for item in value:
            assert_local_refs(item, document)


def validate_examples(document, definitions, cases):
    for case in cases:
        schema = {
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            **document,
            '$ref': f'{definitions}/{case["definition"]}',
        }
        schema.pop('oneOf', None)
        schema.pop('$id', None)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = list(validator.iter_errors(case['value']))
        assert bool(errors) != case['valid'], (
            case['name'], [error.message for error in errors]
        )


def main():
    protocol = load('protocol.schema.json')
    api = load('notes.openapi.json')
    Draft202012Validator.check_schema(protocol)
    validate_spec(api)
    assert_local_refs(protocol, protocol)
    assert_local_refs(api, api)

    role_cases = load('protocol.examples.json')['cases']
    note_cases = load('notes.examples.json')['cases']
    assert len({c['name'] for c in role_cases + note_cases}) == len(role_cases + note_cases)
    validate_examples(protocol, '#/$defs', role_cases)
    validate_examples({'components': api['components']}, '#/components/schemas', note_cases)
    canonical = {'Invocation', 'Message', 'RoleResult', 'ToolRequest', 'ToolResponse',
                 'Evidence', 'TaskSnapshot', 'HumanDecision', 'Event'}
    root_validator = Draft202012Validator(protocol, format_checker=FormatChecker())
    assert {c['definition'] for c in role_cases if c['valid']} >= canonical
    for case in role_cases:
        if case['valid'] and case['definition'] in canonical:
            root_validator.validate(case['value'])

    roles = {'lead', 'frontend', 'backend', 'qa', 'security'}
    allowed = protocol['x-tool-role-allowlist']
    branches = protocol['$defs']['ToolRequest']['properties']['call']['oneOf']
    tools = {b['properties']['tool']['const'] for b in branches}
    assert len(tools) == 11 and tools == set(allowed)
    assert all(values and len(values) == len(set(values)) and set(values) <= roles
               for values in allowed.values())
    assert allowed['submit_patch'] == ['frontend', 'backend', 'qa', 'security']
    assert allowed['submit_assessment'] == ['qa', 'security']
    for name in ['propose_plan', 'ask_human', 'submit_delivery']:
        assert allowed[name] == ['lead']
    for name in tools:
        assert any(c['name'] == name + '_request' for c in role_cases)
        assert any(c['name'] == name + '_ok_response' for c in role_cases)
        assert any(c['name'] == name + '_response' for c in role_cases)

    operations = [op['operationId'] for path in api['paths'].values()
                  for method, op in path.items() if method in {'get', 'post', 'put', 'delete'}]
    assert len(operations) == len(set(operations)) == 5
    assert 'content' not in api['paths']['/api/v1/notes/{note_id}']['delete']['responses']['204']
    for name, definition in api['components']['schemas'].items():
        Draft202012Validator.check_schema(definition)
    # Check boundary shapes beyond the compact stored examples.
    for title, body, valid in [('x' * 120, 'x' * 5000, True),
                               ('x' * 121, '', False), ('x', 'x' * 5001, False)]:
        validate_examples({'components': api['components']}, '#/components/schemas', [{
            'name': 'note_length_boundary', 'definition': 'NoteInput',
            'value': {'title': title, 'body': body}, 'valid': valid,
        }])
    print(f'PASS: schema/OpenAPI validation, local refs, {len(role_cases)} protocol + '
          f'{len(note_cases)} API shape examples, 3 length boundaries, '
          '11 tool allowlists and 5 API operations.')
    print('NOT VERIFIED: actor identity, permissions, real checks, runtime API or replay semantics.')


if __name__ == '__main__':
    main()

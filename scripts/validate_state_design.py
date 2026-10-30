"""Check STATE-001 graph and SQL fixtures; never run an agent or project database."""

import hashlib
import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_graph():
    graph = json.loads((ROOT / 'contracts/workflow.graph.json').read_text())
    protocol = json.loads((ROOT / 'contracts/protocol.schema.json').read_text())
    nodes = {node['id']: node for node in graph['nodes']}
    terminal = set(graph['terminal'])
    require(graph['design_version'] == 1, 'Unsupported graph design version')
    require(len(nodes) == len(graph['nodes']) == 13, 'Duplicate/missing stages')
    require(terminal == {'delivered', 'cancelled'}, 'Unexpected terminal stages')
    require(graph['initial'] in nodes and terminal <= nodes.keys(), 'Unknown stage')
    states = set(protocol['$defs']['TaskSnapshot']['properties']['status']['enum'])
    require({n['task_status'] for n in nodes.values()} <= states, 'Unknown task status')
    require(len(graph['edges']) == 18, 'Expected 18 logical transitions')
    require(len({e['guard'] for e in graph['edges']}) == 18, 'Duplicate guards')
    overview = (ROOT / 'docs/GRAPH-MEMORY.md').read_text()
    edge_table = overview.split('| From | To | Condition / owner |', 1)[1].split('\n\n', 1)[0]
    aliases = {'Any active stage': '@active', 'Any nonterminal stage': '@nonterminal',
               'Last safe stage': '@resume'}
    overview_edges = []
    for line in edge_table.splitlines():
        if line.startswith('|') and '---' not in line:
            labels = [part.strip() for part in line.split('|')[1:3]]
            overview_edges.append(tuple(aliases.get(v, v.lower().replace(' ', '_')) for v in labels))
    require(len(overview_edges) == 18 and set(overview_edges) ==
            {(e['from'], e['to']) for e in graph['edges']}, 'Graph overview disagrees with fixture')

    adjacency = {node: set() for node in nodes}
    for edge in graph['edges']:
        source, target = edge['from'], edge['to']
        require(source in nodes or source in {'@active', '@nonterminal'}, 'Bad source')
        require(target in nodes or target == '@resume', 'Bad target')
        require(bool(edge['guard']), 'Unguarded transition')
        sources = set(nodes) - terminal if source.startswith('@') else {source}
        if source == '@active':
            sources.remove('blocked')
        targets = set(nodes) - terminal - {'blocked'} if target == '@resume' else {target}
        for node in sources:
            adjacency[node].update(targets)
    require(all(not adjacency[n] for n in terminal), 'Terminal stage has an exit')
    reached, pending = set(), [graph['initial']]
    while pending:
        node = pending.pop()
        if node not in reached:
            reached.add(node)
            pending.extend(adjacency[node] - reached)
    require(reached == set(nodes), 'Unreachable stages')
    for final, guard in [('delivered', 'human_accepted_and_delivery_observed'),
                         ('implement', 'plan_approved_and_contract_acknowledged')]:
        require(any(e['to'] == final and e['guard'] == guard for e in graph['edges']),
                'Missing human gate')
    return set(nodes)


def expect_rejected(db, statement, parameters=()):
    db.execute('SAVEPOINT rejected_case')
    try:
        db.execute(statement, parameters)
    except sqlite3.IntegrityError:
        pass
    else:
        raise ValueError(f'SQL fixture accepted invalid case: {statement}')
    finally:
        db.execute('ROLLBACK TO rejected_case')
        db.execute('RELEASE rejected_case')


def validate_storage(nodes):
    sql = (ROOT / 'contracts/domain-storage.sql').read_text()
    with sqlite3.connect(':memory:') as db:
        db.executescript(sql)
        require(db.execute('PRAGMA foreign_keys').fetchone() == (1,), 'Foreign keys disabled')
        db.execute('INSERT INTO schema_meta VALUES (1, 1, ?, ?)',
                   ('synthetic-project', hashlib.sha256(sql.encode()).hexdigest()))
        db.executemany('INSERT INTO missions (mission_id, stage, input_digest) VALUES (?, ?, ?)',
                       [('m1', 'request', 'a' * 64), ('m2', 'cancelled', 'b' * 64)])
        db.executemany('INSERT INTO tasks (mission_id, task_id, owner, status, plan_position) '
                       'VALUES (?, ?, ?, ?, ?)',
                       [('m1', 't1', 'frontend', 'planned', 0),
                        ('m1', 't2', 'backend', 'planned', 1),
                        ('m2', 'foreign-task', 'lead', 'cancelled', 0)])
        db.execute('INSERT INTO task_dependencies VALUES (?, ?, ?)', ('m1', 't2', 't1'))
        db.executemany('INSERT INTO artifacts VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [
            (mission, name, 'c' * 64, 2, 'application/json', 'private', 'present',
             '2026-10-30T00:00:00Z') for mission, name in [('m1', 'object1'), ('m2', 'object2')]]
        )
        db.execute('INSERT INTO attempts (mission_id, task_id, attempt_id, ordinal, '
                   'actor_role, input_digest, started_at, outcome) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   ('m1', 't1', 'attempt1', 1, 'frontend', 'd' * 64,
                    '2026-10-30T00:00:00Z', 'running'))
        db.execute('INSERT INTO records VALUES (?, ?, ?, ?, ?, ?)',
                   ('m1', 'record1', 't1', 'attempt1', 'invocation', 'object1'))
        db.execute('INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   ('m1', 'event1', 1, '2026-10-30T00:00:00Z', 'controller', 'controller1',
                    'record1', None))
        db.execute('INSERT INTO memory_entries VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   ('m1', 'entry1', 'summary', 't1', 'd' * 64, 'object1', 'record1', None))
        operation = ('m1', 't1', 'attempt1', 'key1', 'e' * 64, 'prepared', None)
        db.execute('INSERT INTO operations VALUES (?, ?, ?, ?, ?, ?, ?)', operation)
        db.execute('INSERT INTO node_runs VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   ('m1', 't1', 'attempt1', 'implement', 'd' * 64, 'prepared', None, None))
        db.commit()

        rejected = [
            ('UPDATE missions SET stage = ? WHERE mission_id = ?', ('invented-stage', 'm1')),
            ('INSERT INTO missions (mission_id, stage, input_digest) VALUES (?, ?, ?)',
             ('m3', 'request', 'a' * 64)),
            ('INSERT INTO task_dependencies VALUES (?, ?, ?)', ('m1', 't1', 'foreign-task')),
            ('INSERT INTO task_dependencies VALUES (?, ?, ?)', ('m1', 't1', 't1')),
            ('INSERT INTO operations VALUES (?, ?, ?, ?, ?, ?, ?)', operation),
            ('UPDATE operations SET state = ?, response_artifact = ?', ('observed', 'object2')),
            ('UPDATE operations SET state = ?', ('observed',)),
            ('UPDATE tasks SET owner = ?', ('human',)),
            ('UPDATE tasks SET status = ?', ('approved_by_agent',)),
            ('INSERT INTO attempts SELECT mission_id, task_id, ?, ordinal, actor_role, '
             'input_digest, started_at, finished_at, outcome, result_artifact, usage_artifact '
             'FROM attempts', ('attempt2',)),
            ('UPDATE records SET task_id = ?', ('t2',)),
            ('UPDATE events SET record_id = ?', ('unknown-record',)),
            ('UPDATE artifacts SET byte_count = ?', (-1,)),
            ('UPDATE node_runs SET state = ?', ('checkpoint_observed',)),
            ('UPDATE missions SET stage = ? WHERE mission_id = ?', ('blocked', 'm1')),
            ('UPDATE missions SET resume_stage = ? WHERE mission_id = ?', ('checks', 'm2')),
            ('DELETE FROM artifacts WHERE mission_id = ? AND artifact_id = ?', ('m1', 'object1')),
        ]
        for statement, parameters in rejected:
            expect_rejected(db, statement, parameters)

        # A conflict during a multi-record result transaction must undo its earlier update.
        version = db.execute('SELECT state_version FROM tasks WHERE mission_id=? AND task_id=?',
                             ('m1', 't1')).fetchone()[0]
        db.commit()
        try:
            with db:
                db.execute('UPDATE tasks SET state_version=state_version+1 WHERE mission_id=? '
                           'AND task_id=?', ('m1', 't1'))
                db.execute('UPDATE operations SET state=?, response_artifact=?', ('observed', 'missing'))
        except sqlite3.IntegrityError:
            pass
        else:
            raise ValueError('Expected transaction failure')
        require(db.execute('SELECT state_version FROM tasks WHERE mission_id=? AND task_id=?',
                           ('m1', 't1')).fetchone() == (version,), 'Partial result transaction')
        update = 'UPDATE tasks SET state_version=state_version+1 WHERE mission_id=? AND task_id=? AND state_version=?'
        require(db.execute(update, ('m1', 't1', version)).rowcount == 1, 'First update failed')
        require(db.execute(update, ('m1', 't1', version)).rowcount == 0, 'Stale update accepted')
        db.execute('UPDATE operations SET state=?, response_artifact=?', ('observed', 'object1'))
        db.execute('UPDATE node_runs SET state=?, result_artifact=?', ('result_recorded', 'object1'))
        db.execute('UPDATE node_runs SET state=?, checkpoint_id=?', ('checkpoint_observed', 'opaque-1'))
        for stage in nodes:
            if stage not in {'delivered', 'cancelled'}:
                db.execute('UPDATE missions SET stage=?, resume_stage=? WHERE mission_id=?',
                           (stage, 'checks' if stage == 'blocked' else None, 'm1'))
        db.commit()
        require(db.execute('PRAGMA foreign_key_check').fetchall() == [], 'Foreign key failure')
        tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")]
        require(len(tables) == 11, 'Unexpected table count')
        with sqlite3.connect(':memory:') as restored:
            restored.execute('PRAGMA foreign_keys = ON')
            db.backup(restored)
            require(restored.execute('PRAGMA integrity_check').fetchone() == ('ok',), 'Backup corrupt')
            require(restored.execute('PRAGMA foreign_key_check').fetchall() == [], 'Backup references invalid')
            for table in tables:
                # Identifiers come exclusively from this reviewed schema, not caller input.
                require(db.execute(f'SELECT * FROM "{table}"').fetchall() ==
                        restored.execute(f'SELECT * FROM "{table}"').fetchall(), 'Backup differs')
        return len(rejected)


def main():
    nodes = validate_graph()
    count = validate_storage(nodes)
    print(f'PASS: 13 stages, 18 guarded edges, 11 SQL tables, {count} rejected SQL cases, '
          'transaction rollback, version conflict and synthetic SQLite backup.')
    print(f'Environment: SQLite {sqlite3.sqlite_version}. '
          'NOT VERIFIED: LangGraph restart, live locks, external replay, artifact restore or runtime gates.')


if __name__ == '__main__':
    main()

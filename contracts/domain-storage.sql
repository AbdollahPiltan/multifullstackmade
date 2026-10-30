-- STATE-001 version 1 design fixture, not an application migration command.
-- Runtime must validate canonical protocol payloads and domain transitions too.
PRAGMA foreign_keys = ON;

CREATE TABLE schema_meta (
    singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
    version INTEGER NOT NULL CHECK (version = 1),
    project_id TEXT NOT NULL UNIQUE,
    schema_digest TEXT NOT NULL CHECK (length(schema_digest) = 64)
);

CREATE TABLE missions (
    mission_id TEXT PRIMARY KEY,
    stage TEXT NOT NULL CHECK (stage IN (
        'request', 'clarify', 'plan', 'await_human', 'implement', 'checks',
        'independent_review', 'repair', 'lead_review', 'await_delivery_decision',
        'delivered', 'blocked', 'cancelled')),
    resume_stage TEXT CHECK (resume_stage IN (
        'request', 'clarify', 'plan', 'await_human', 'implement', 'checks',
        'independent_review', 'repair', 'lead_review', 'await_delivery_decision')),
    state_version INTEGER NOT NULL DEFAULT 0 CHECK (state_version >= 0),
    input_digest TEXT NOT NULL CHECK (length(input_digest) = 64),
    plan_artifact TEXT,
    budget_artifact TEXT,
    CHECK ((stage = 'blocked' AND resume_stage IS NOT NULL)
        OR (stage <> 'blocked' AND resume_stage IS NULL)),
    FOREIGN KEY (mission_id, plan_artifact) REFERENCES artifacts(mission_id, artifact_id),
    FOREIGN KEY (mission_id, budget_artifact) REFERENCES artifacts(mission_id, artifact_id)
);

CREATE UNIQUE INDEX one_active_mission ON missions ((1))
    WHERE stage NOT IN ('delivered', 'cancelled');

CREATE TABLE tasks (
    mission_id TEXT NOT NULL REFERENCES missions(mission_id),
    task_id TEXT NOT NULL,
    owner TEXT NOT NULL CHECK (owner IN ('lead', 'frontend', 'backend', 'qa', 'security')),
    status TEXT NOT NULL CHECK (status IN (
        'planned', 'ready', 'in_progress', 'awaiting_checks', 'changes_requested',
        'awaiting_lead', 'awaiting_human', 'done', 'blocked', 'cancelled')),
    plan_position INTEGER NOT NULL CHECK (plan_position >= 0),
    current_attempt_ordinal INTEGER NOT NULL DEFAULT 0 CHECK (current_attempt_ordinal >= 0),
    state_version INTEGER NOT NULL DEFAULT 0 CHECK (state_version >= 0),
    PRIMARY KEY (mission_id, task_id),
    UNIQUE (mission_id, plan_position)
);

CREATE TABLE task_dependencies (
    mission_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    predecessor_id TEXT NOT NULL,
    PRIMARY KEY (mission_id, task_id, predecessor_id),
    CHECK (task_id <> predecessor_id),
    FOREIGN KEY (mission_id, task_id) REFERENCES tasks(mission_id, task_id),
    FOREIGN KEY (mission_id, predecessor_id) REFERENCES tasks(mission_id, task_id)
);
CREATE INDEX dependency_consumers ON task_dependencies (mission_id, predecessor_id);

CREATE TABLE artifacts (
    mission_id TEXT NOT NULL REFERENCES missions(mission_id),
    artifact_id TEXT NOT NULL,
    digest TEXT NOT NULL CHECK (length(digest) = 64),
    byte_count INTEGER NOT NULL CHECK (byte_count >= 0),
    media_type TEXT NOT NULL,
    sensitivity TEXT NOT NULL CHECK (sensitivity IN ('public_sanitized', 'private')),
    availability TEXT NOT NULL CHECK (availability IN ('present', 'missing', 'redacted', 'deleted')),
    created_at TEXT NOT NULL,
    PRIMARY KEY (mission_id, artifact_id)
);

CREATE TABLE attempts (
    mission_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    attempt_id TEXT NOT NULL,
    ordinal INTEGER NOT NULL CHECK (ordinal > 0),
    actor_role TEXT NOT NULL CHECK (actor_role IN ('lead', 'frontend', 'backend', 'qa', 'security')),
    input_digest TEXT NOT NULL CHECK (length(input_digest) = 64),
    started_at TEXT NOT NULL,
    finished_at TEXT,
    outcome TEXT NOT NULL CHECK (outcome IN (
        'running', 'ready_for_review', 'needs_input', 'blocked', 'failed', 'cancelled')),
    result_artifact TEXT,
    usage_artifact TEXT,
    PRIMARY KEY (mission_id, task_id, attempt_id),
    UNIQUE (mission_id, task_id, ordinal),
    CHECK ((outcome = 'running' AND finished_at IS NULL)
        OR (outcome <> 'running' AND finished_at IS NOT NULL)),
    FOREIGN KEY (mission_id, task_id) REFERENCES tasks(mission_id, task_id),
    FOREIGN KEY (mission_id, result_artifact) REFERENCES artifacts(mission_id, artifact_id),
    FOREIGN KEY (mission_id, usage_artifact) REFERENCES artifacts(mission_id, artifact_id)
);

CREATE TABLE records (
    mission_id TEXT NOT NULL,
    record_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    attempt_id TEXT NOT NULL,
    kind TEXT NOT NULL CHECK (kind IN (
        'invocation', 'message', 'role_result', 'tool_request', 'tool_response',
        'evidence', 'human_decision', 'task_snapshot')),
    artifact_id TEXT NOT NULL,
    PRIMARY KEY (mission_id, record_id),
    FOREIGN KEY (mission_id, task_id, attempt_id) REFERENCES attempts(mission_id, task_id, attempt_id),
    FOREIGN KEY (mission_id, artifact_id) REFERENCES artifacts(mission_id, artifact_id)
);
CREATE INDEX task_records ON records (mission_id, task_id, attempt_id);

CREATE TABLE events (
    mission_id TEXT NOT NULL,
    event_id TEXT NOT NULL,
    sequence INTEGER NOT NULL CHECK (sequence > 0),
    recorded_at TEXT NOT NULL,
    actor_kind TEXT NOT NULL CHECK (actor_kind IN ('controller', 'operator', 'agent')),
    actor_ref TEXT NOT NULL,
    record_id TEXT NOT NULL,
    supersedes_event TEXT,
    PRIMARY KEY (mission_id, event_id),
    UNIQUE (mission_id, sequence),
    CHECK (supersedes_event IS NULL OR supersedes_event <> event_id),
    FOREIGN KEY (mission_id, record_id) REFERENCES records(mission_id, record_id),
    FOREIGN KEY (mission_id, supersedes_event) REFERENCES events(mission_id, event_id)
);

CREATE TABLE operations (
    mission_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    attempt_id TEXT NOT NULL,
    operation_key TEXT NOT NULL,
    request_digest TEXT NOT NULL CHECK (length(request_digest) = 64),
    state TEXT NOT NULL CHECK (state IN ('prepared', 'running', 'unknown', 'observed')),
    response_artifact TEXT,
    PRIMARY KEY (mission_id, task_id, attempt_id, operation_key),
    CHECK ((state = 'observed' AND response_artifact IS NOT NULL)
        OR (state <> 'observed' AND response_artifact IS NULL)),
    FOREIGN KEY (mission_id, task_id, attempt_id) REFERENCES attempts(mission_id, task_id, attempt_id),
    FOREIGN KEY (mission_id, response_artifact) REFERENCES artifacts(mission_id, artifact_id)
);
CREATE INDEX pending_operations ON operations (mission_id, state);

CREATE TABLE node_runs (
    mission_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    attempt_id TEXT NOT NULL,
    node_id TEXT NOT NULL,
    input_digest TEXT NOT NULL CHECK (length(input_digest) = 64),
    state TEXT NOT NULL CHECK (state IN ('prepared', 'result_recorded', 'checkpoint_observed')),
    result_artifact TEXT,
    checkpoint_id TEXT,
    PRIMARY KEY (mission_id, task_id, attempt_id, node_id, input_digest),
    CHECK ((state = 'prepared' AND result_artifact IS NULL AND checkpoint_id IS NULL)
        OR (state = 'result_recorded' AND result_artifact IS NOT NULL AND checkpoint_id IS NULL)
        OR (state = 'checkpoint_observed' AND result_artifact IS NOT NULL AND checkpoint_id IS NOT NULL)),
    FOREIGN KEY (mission_id, task_id, attempt_id) REFERENCES attempts(mission_id, task_id, attempt_id),
    FOREIGN KEY (mission_id, result_artifact) REFERENCES artifacts(mission_id, artifact_id)
);

CREATE TABLE memory_entries (
    mission_id TEXT NOT NULL,
    entry_id TEXT NOT NULL,
    kind TEXT NOT NULL CHECK (kind IN ('decision', 'summary', 'file_index')),
    scope_key TEXT NOT NULL,
    input_digest TEXT NOT NULL CHECK (length(input_digest) = 64),
    artifact_id TEXT NOT NULL,
    source_record_id TEXT NOT NULL,
    supersedes_entry TEXT,
    PRIMARY KEY (mission_id, entry_id),
    CHECK (supersedes_entry IS NULL OR supersedes_entry <> entry_id),
    FOREIGN KEY (mission_id, artifact_id) REFERENCES artifacts(mission_id, artifact_id),
    FOREIGN KEY (mission_id, source_record_id) REFERENCES records(mission_id, record_id),
    FOREIGN KEY (mission_id, supersedes_entry) REFERENCES memory_entries(mission_id, entry_id)
);
CREATE INDEX memory_lookup ON memory_entries (mission_id, scope_key, input_digest);

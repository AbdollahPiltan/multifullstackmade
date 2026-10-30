# Stage-five graph and durable memory design

Record STATE-001, 2026-10-30; implements the design deliverable T-014 against
[ARCH-001](ARCHITECTURE.md), [ROLE-001](AGENT-CONTRACTS.md) and
[PROTO-001](PROTOCOL-CONTRACTS.md). This specifies future implementation. The SQL
and graph files below are reviewable design fixtures, not an installed database,
LangGraph runner, migration command or working memory service.

## 1. Sources of truth and storage boundary

| Concern | Authority / location in the future private project directory |
| --- | --- |
| Mission, tasks, attempts, ownership, gates and operation intents | Controller-owned `domain.sqlite3`; authoritative domain results |
| Graph scheduling checkpoint | Adapter-owned `checkpoints.sqlite3`; mission ID is the LangGraph thread ID; opaque checkpoint IDs |
| Exact records, source manifests, logs and summaries | `objects/sha256/<digest>`; immutable content, referenced by domain metadata |
| Working source | Separate Git worktrees; source commit plus clean-tree manifest pins content; never the only copy of evidence |
| Notes fixture data | Separate container/preview storage; cannot access controller databases or objects |
| Public continuation | Repository MEMORY.md/TASKS.md; sanitized manual navigation, never runtime authority |

One private directory belongs to one project identity, checked against the canonical
repository path and approved remote. Refuse a mismatch rather than automatically
sharing context. Keep directories owner-only (0700), files owner-only (0600), outside
the checkout and containers. This is local access control, not encryption at rest.
Credentials stay in operator configuration; no secret-bearing transcript is stored.

The baseline files are [workflow.graph.json](../contracts/workflow.graph.json) and
[domain-storage.sql](../contracts/domain-storage.sql). The latter describes domain
schema version 1; it must never be applied to LangGraph's database. Full protocol
records stay canonical JSON artifacts validated against PROTO-001. SQL stores query
keys, references and mutable projections; it does not reimplement JSON Schema.
No wire field, role, tool or protocol version changes in STATE-001.

## 2. Executable stages and deterministic gates

The 18 logical edges in [GRAPH-MEMORY.md](GRAPH-MEMORY.md) remain the workflow
overview. The JSON file pins machine IDs, task-state mapping and guard names.
`@active` excludes blocked and terminal stages; `@nonterminal` includes blocked;
`@resume` means the saved safe nonterminal stage, never an arbitrary target.
Guards are controller predicates, not booleans accepted from agent output.

| Stage | Durable work / exit gate |
| --- | --- |
| request / clarify | Capture scoped requirement artifact; material questions answered by the actual operator through the lead |
| plan | Lead proposal, DAG, path grants, acceptance/check IDs and versioned contract recorded |
| await_human | Exact plan digest accepted; connected developers acknowledge the same contract; no implicit approval on timeout |
| implement | Select one ready task at a time; persist invocation and attempt before dispatch; required owners submit concrete revisions |
| checks | Integrate accepted patches; execute required registered checks on the combined immutable source snapshot |
| independent_review | Sequential QA and Security results tracked separately; both current and passing, no blocking findings |
| repair | Preserve failed evidence; assign the responsible owner; reserve remaining repair budget before the next attempt |
| lead_review | Lead evaluates criteria; controller rechecks all required gates and reconciles the PR authorized by mission setup; missing publication authority blocks that effect |
| await_delivery_decision | Present the exact delivery artifact, observed PR reference and limitations to the human; record accept/change/cancel |
| delivered | Human acceptance plus observed completion of the authorized delivery PR; acceptance alone does not prove a PR exists |
| blocked | Persist reason, safe return stage, affected tasks and unresolved effects; stop dependent scheduling |
| cancelled | Persist cancellation and stop/observe running effects; late results remain historical and cannot reopen the mission |

Task status is a projection, distinct from mission stage. `planned -> ready` needs
accepted plan and dependencies; `ready -> in_progress` needs a reserved attempt.
`in_progress -> awaiting_checks` needs an applied revision; check/review failure
sets `changes_requested`, and a budgeted repair returns it to `in_progress`.
Passing required checks and both reviews sets `awaiting_lead`; lead acceptance
sets `awaiting_human`; observed authorized delivery sets `done`. Before assignment,
clarification tasks may have no implementation attempt. Block/cancel applies to any
unfinished task; resume re-evaluates prerequisites instead of copying an old status.
Completed dependency tasks do not rerun just because the mission changes stages.

Replanning creates a new approved plan artifact; unchanged valid results may be
reused after explicit compatibility checks. Requirement/contract/policy changes
invalidate affected work. No task dependency cycles or overlapping grants are
permitted; the controller checks these inside the plan update transaction.
Node IDs, role IDs, task IDs and attempt IDs are different identities.

Before the implementation DAG exists, the controller creates a lead coordination
task and attempt for clarification/plan records. This satisfies PROTO-001 context
without pretending implementation started. Its accepted outputs become references
in the subsequent plan; it does not consume a developer assignment.

## 3. Domain schema and attribution

The reference SQL uses ordinary SQLite types, explicit foreign keys and CHECK
constraints; no ORM or new service. IDs are scoped by mission. A database has one
project metadata row and at most one nonterminal mission. Cross-mission references
are rejected by composite foreign keys, not trusted because an ID looks valid.

| Table | Purpose / important invariant |
| --- | --- |
| schema_meta | Project identity, version and reference schema digest; exactly the supported version before writes |
| missions | Stage, safe return stage, state version, pinned plan/input artifacts and remaining-budget ledger artifact |
| tasks | Owner, status, ordered plan position and current attempt ordinal; compare-and-swap version for updates |
| task_dependencies | Same-mission predecessor links; unique, no self-edge; longer cycles require domain validation |
| attempts | Task, ordinal, authenticated role, input digest, start/end, outcome, result/usage artifacts; history preserved |
| artifacts | Content digest, bytes, media type, sensitivity, creation time and availability; no caller-supplied host path |
| records | Canonical protocol artifact plus task/attempt identity and record kind; source validation remains mandatory |
| events | Mission-ordered sequence, authenticated actor, UTC creation time, artifact reference and linked corrections |
| operations | Scoped operation key, immutable request digest, state and observed response; one intent before any effect |
| node_runs | Task/attempt/node/input identity, result reference and checkpoint observation; completed output can survive checkpoint lag |
| memory_entries | Decision/summary/file-index references, provenance, input digest and supersession; navigation aids only |

Every patch/result/message/check is associated with its invocation through the
canonical record context. Events provide the actual actor and recording time;
an agent's declared role is insufficient. A handoff is a PROTO-001 Message of kind
handoff, followed by its receiver's recorded acknowledgement where required.
Original failed checks and assessments remain immutable artifacts. Current task
state and memory availability are mutable projections of recorded observations.
No private reasoning trace is required or retained.

SQL constraints cover relational shape only. The trusted writer must additionally
validate digest syntax, timestamps, attempt ownership/current ordinal, node IDs,
acyclic dependencies, canonical record context and permitted transitions. Normal
history writes append records; corrections append linked records. Only the explicit
redaction/deletion procedure may remove historical payloads. No model gets SQL access.

Query by `(mission, task, attempt)`, dependency predecessor, pending operations,
event sequence or memory scope/input digest. Page events and messages with a stable
sequence cursor; retrieve task context by IDs, not a full event replay on every turn.
The reference indexes support these accesses; query plans and workload budgets
still need measurement at implementation. One SQL transaction updates a result,
event and projection with an expected state version; zero updated rows means conflict.
Foreign keys must be enabled on every connection before a transaction. This is
required by [SQLite's connection-level foreign-key behavior](https://www.sqlite.org/foreignkeys.html).

## 4. Commit protocol and restart algorithm

Use a nonblocking OS advisory project lock held by the controller for its entire
write lifetime. Do not use a PID file as proof of ownership, unlink an active lock,
or automatically steal it after a timer. The selected Linux/macOS implementation
must be tested; unavailable locking fails closed. Read-only inspection must not
start a runner. Cancellation and recovery also respect the writer lock.

For each node, hash a canonical sorted-key UTF-8 JSON input manifest containing
project/mission/task/attempt, source tree, requirements, plan, contract, policy,
role configuration, check profile/image and graph/schema versions. Array order is
significant; file manifests are sorted by normalized path. Snapshot file bytes
are hashed exactly, with no newline normalization. Reject unsupported values.
Pin a digest of the complete manifest, not just a branch name or summary text.

1. Acquire lock; verify project identity, supported versions, artifact availability,
   Git snapshot and remaining persisted limits. Refuse unexplained worktree changes.
2. In a short domain transaction reserve usage/attempt budget, record invocation,
   `prepared` node run and effect intent keyed by task/attempt/operation_key.
3. Outside SQL transactions, perform the permitted operation. Never hold a database
   transaction across a model call, Docker check, Git or GitHub request.
4. Write each bounded artifact to a private temporary file, hash, flush/fsync,
   atomically rename on the same filesystem and sync its parent directory. Verify
   an already-existing object against the digest; mismatches are corruption.
5. Commit observed operation response, result record/event, usage and task/mission
   projection together in domain SQLite. The node run becomes `result_recorded`.
6. Advance LangGraph/checkpoint using that committed result. Record the opaque
   checkpoint reference as `checkpoint_observed` in a separate domain transaction.

These commits are not one distributed transaction. Set and verify appropriate
SQLite durability settings at scaffold (foreign_keys=ON, synchronous=FULL; journal
mode chosen and verified for the local filesystem). Network filesystems are outside
the initial storage profile. Never edit adapter-owned checkpoint tables directly.
LangGraph documents checkpoints separately from long-term stores, and resumes
interrupted nodes by restarting their bodies:
[persistence](https://docs.langchain.com/oss/python/langgraph/persistence),
[interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts).
Place human interrupts before effects and make resumed bodies consult the journal.

| Observed restart boundary | Required recovery |
| --- | --- |
| Prepared intent, no confirmed result | Determine whether effect began; mark unknown when uncertain; never assume failure |
| Object exists, domain reference absent | Quarantine as orphan; retain until reference reconciliation; no automatic success |
| Domain result committed, checkpoint behind | Reuse verified result for identical input, advance through adapter; no repeated paid/tool effect |
| Checkpoint claims completion, domain result missing | Block; inspect backup/domain integrity; no fabricated result or direct checkpoint SQL repair |
| PR may exist, response absent | Controller reconciles approved repository/base/head and intent; ambiguity blocks; GH-001 defines identity details |
| Paid model call may have completed | Keep usage reservation and unknown outcome; use supported provider observations where available; otherwise require an explicit retry decision under budget |
| Source/contract/policy/profile changed | Mark affected result unusable, recompute context and rerun applicable gates |
| Running container at cancellation/crash | Controller finds owned execution identity, stops or observes it; late outputs are recorded without accepting delivery |

An identical operation key/request returns the recorded observation; reuse with a
different request digest conflicts. State progresses through prepared, running,
unknown or observed; only authoritative reconciliation resolves unknown. A failed
observed result is still observed, not a reason to repeat it automatically. New
authorized role actions use new keys and remaining budget. Safe transport dispatch
retries inside a still-pending intent follow LIM-001 and retain their own durable
dispatch IDs; they are distinct from a new work/repair attempt. Preserve
budget consumption and uncertain reservations across restart. Numeric limits and
timeout/retry eligibility are now specified by [LIM-001](EXECUTION-LIMITS.md);
no execution before those limits are implemented and verified.

For typed tools, the request digest covers the immutable context, tool and canonical
arguments. The operation key is already in the primary key; request_id is transport
correlation and is excluded from the digest. A replay response uses the current
request_id while referencing the original observation. Provider intents similarly
pin sanitized effective input/configuration, never a credential value.

## 5. Retrieval, invalidation and memory correctness

Assemble a manifest for each invocation: accepted requirements/policy/contract,
task ownership and dependencies, unresolved messages/findings, last failed attempt,
current evidence, relevant source excerpts and reasons for including each reference.
File-index entries use project, path, blob digest and indexer version; stale entries
are excluded and the relevant paths re-indexed. Start with path/import/symbol and
literal search; a graph/vector database or embeddings is unnecessary for this MVP.

Read approved decisions first, then current task dependencies and referenced files.
When a summary contradicts source/evidence, expand inspection and add a correction
linked to the original entry. A missing dependency, truncated required contract or
unknown impact blocks the handoff until inspected. Tokens/bytes/record counts must
fit LIM-001; provide pagination or ask for a smaller task, never silently drop a
required input. Do not automatically load other roles' full transcripts.

Gate validity is recomputed from exact source revision/tree, requirement, plan,
contract, policy, check-profile and environment digests. For MVP, conservatively
invalidate all delivery checks/reviews after any candidate snapshot change; retain
the original outcomes and append a stale observation. A test with zero executed
tests, a missing artifact or an agent summary cannot satisfy a required check.
No reuse across projects. Compare token/latency/correctness on representative tasks
before claiming selective retrieval improves cost.

For a later mission in the same project, the controller may inspect approved
decisions from named prior missions using scope and compatibility filters. Create
a current-mission context artifact with explicit origin mission/record/digest and
supersession references; do not rewrite the original canonical record's context or
create a cross-mission SQL foreign key. Such imported knowledge remains provenance,
not a current plan approval, permission grant or reusable passing review.

## 6. Retention, deletion and recovery policy

Default: keep the active mission's required records and referenced artifacts until
explicit operator cleanup. Terminal missions remain private until the operator
chooses archive or deletion; there is no silent age-based purge. Orphans may be
removed only by explicit cleanup after scanning both databases, pending intents and
backup manifests. Preview cleanup lists scope, bytes and broken/restricted resume
paths. Limits must stop writes before unbounded storage growth (LIM-001).

Store concise structured exchanges, decisions and bounded sanitized diagnostics;
do not persist full provider conversations by default. Exclude secrets before any
artifact/model/log write. If sensitive content is discovered, stop exposing it,
restrict access, remove its object and affected backup copies where controlled,
and append a content-free deletion/correction marker. Reconcile every reference to
a shared object so another mission cannot continue exposing the deleted content.
`availability=redacted` or
`deleted` keeps the ID/digest but no recoverable payload. Hashes may themselves be
sensitive: full mission deletion may remove metadata too. Resume and gates requiring
removed content are blocked. Audit history is not an undeletable secret archive.

Backups are an explicit operator action, outside the source tree, with the same
access restrictions. Stop scheduling, settle or record in-flight effects, acquire
the writer lock, and quiesce both stores. Use the SQLite backup API for each database
and copy referenced immutable objects plus source snapshot/bundle needed to resume.
Do not copy a live SQLite main file while ignoring its WAL. The
[SQLite backup API](https://www.sqlite.org/backup.html) supports consistent database
copies; cross-store consistency still requires the quiescent protocol here.

Write the backup manifest last: project identity, domain/checkpoint/schema versions,
file digests, object references, source snapshot, unresolved intents and creation
time. Credentials are excluded. A backup is verified only after restoring into a
new private directory, running integrity_check/foreign_key_check on both databases,
checking referenced object hashes and reconstructing the pending stage read-only.
Adapter schema compatibility is checked through its supported API, not rewritten.
Missing referenced files fail restore verification. External GitHub/provider state
is not restored; reconcile it before any resumed effect. Backup-frequency and
recovery-time/data-loss targets remain operator decisions, not measured guarantees.

Migration policy: reject a newer unsupported domain/schema/graph version; no
automatic downgrade. Future migrations are numbered, checksum-pinned, reviewed
and tested against a verified backup. Under the exclusive lock and with scheduling
stopped, migrate domain data transactionally, then run integrity/reference/version
checks. Upgrade the checkpoint adapter only with a tested compatibility path and
consistent backup of both stores. On failure stop and restore to a separate
directory; never overwrite the only recoverable copy or silently resume old code.
The reference v1 DDL is a fresh-schema fixture, not an upgrade implementation.

## 7. Validation and implementation acceptance

Run `python3 scripts/validate_state_design.py` with the standard library. It checks
graph references/reachability/task-state vocabulary and exercises the SQL fixture
in memory: same-mission references, one active mission, operation uniqueness,
attempt identity, optimistic version conflicts and transactional rollback. It also
checks the SQLite backup API on that synthetic database. It never starts LangGraph,
creates a real project database, calls a model or creates a delivery PR.

At this design checkpoint the fixture checks ran with Python 3.10.6 and SQLite
3.37.2. This is a tooling observation; it does not validate the selected Python
3.12/LangGraph application stack, filesystem crash safety or complete project restore.

Future integration scenarios (not claimed passing here):

| ID | Required observable result / existing acceptance |
| --- | --- |
| ST-01 | Kill/restart at each commit boundary; completed node reused only with matching inputs (AC-07) |
| ST-02 | Unknown paid/PR effects block blind replay; reconcile once, preserve usage reservation (AC-09) |
| ST-03 | Changed snapshot or policy invalidates checks/reviews without erasing history (AC-08) |
| ST-04 | Failed test -> owner repair -> real retest retains all attempts; exhausted budget blocks (AC-05/06) |
| ST-05 | Two processes contend for one lock; second cannot write or dispatch effects |
| ST-06 | Cross-project artifact, forged actor/approval and corrupt object cannot unlock gates (AC-02/11) |
| ST-07 | Oversized/missing/stale context triggers bounded expansion or blocked state (AC-10/13) |
| ST-08 | Restore both databases, objects and source; continue read-only then reconcile external effects |
| ST-09 | Redact/delete required object and backup copies; mark unavailable and block dependent resume |
| ST-10 | Cancel during check/model operation; late result cannot turn cancelled mission into delivered (AC-12) |
| ST-11 | Unsupported migration/adapter version blocks; tested restore preserves the prior recoverable copy |

LIM-001 now selects numeric budgets and accounting/cancellation design.
SBX-001 now specifies sandbox/access design and its required runtime qualification;
[GH-001](GITHUB-DELIVERY.md) now specifies external identities/reconciliation.
T-018 starts implementation when instructed.
T-019/T-020 implement this design. Passing the static fixture checks does not prove
these integration scenarios or a working durable agent team.

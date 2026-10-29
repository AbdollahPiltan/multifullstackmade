# Execution graph and project memory

Status: proposed runtime design, documented 2026-10-29. The current repository uses
[MEMORY.md](../MEMORY.md) for manual continuation and [TASKS.md](../TASKS.md) for
task status. No runtime graph engine, database, retrieval service, or automatic
resume behavior has been implemented. Framework/storage and execution choices are now selected in
[ARCHITECTURE.md](ARCHITECTURE.md); no runtime has been implemented.

## Purpose and boundaries

Give each role enough verified context to continue a bounded task without routinely
reading all source files or replaying every conversation. An execution graph records
what can happen next; persistent state records where execution stopped; project
memory records relevant knowledge; evidence records what was actually checked.
These are distinct concerns and can share a simple local store in a future MVP.
A graph database, vector database, or extra service is not required by this design.

Role inputs/outputs and authority are specified in
[AGENT-CONTRACTS.md](AGENT-CONTRACTS.md). The controller must enforce those
permissions; graph progress alone does not grant tool access.

## Directed workflow graph

The following edge table is the canonical proposed graph definition. Each node is
a stage, not an agent. A developer can own multiple task instances of a stage.

| From | To | Condition / owner |
| --- | --- | --- |
| Request | Clarify | Lead identifies requirements and material questions |
| Clarify | Plan | Requirements and acceptance criteria are explicit |
| Plan | Await human | Lead submits scope, architecture, acknowledged API contract where needed, and task dependencies |
| Await human | Implement | Human approves the plan |
| Await human | Clarify | Human requests changes |
| Implement | Checks | Required Frontend / Backend owners deliver revisions and artifacts against the accepted contract; sequential MVP scheduling |
| Checks | Independent review | Required actual checks pass on that revision |
| Checks | Repair | Required check fails; return evidence to task owner |
| Independent review | Lead review | QA and security both accept the current revision |
| Independent review | Repair | QA or security records blocking findings |
| Repair | Implement | Owner revises within the approved scope and limits |
| Lead review | Await delivery decision | Criteria met and evidence is current |
| Lead review | Repair | Lead requests a scoped correction |
| Await delivery decision | Delivered | Human accepts the defined delivery |
| Await delivery decision | Clarify | Human changes scope; re-plan affected tasks |
| Any active stage | Blocked | Missing dependency, exhausted limit or unresolved failure |
| Blocked | Last safe stage | Cause resolved, evidence reconciled and continuation authorized |
| Any nonterminal stage | Cancelled | Human cancels; pending work is stopped where possible |

Delivery acceptance does not itself imply merge or deployment authorization. Record
those external actions independently. Per-task dependency edges must be acyclic;
repair loops belong to execution attempts with bounded counters. Detect invalid
dependencies before scheduling. All relevant checks on combined changes must run
again before final acceptance. A lead cannot turn a missing check into a pass.

## Minimal persistent records

| Record | Required fields |
| --- | --- |
| Mission | ID, project scope, approved requirement/policy revisions, limits, active stage, checkpoint ID |
| Task | Stable ID, owner role, dependencies, acceptance criteria, status, current attempt, input/output references |
| Attempt | ID, task ID, actor, start/end time, input revision, result revision, outcome, usage, error, next action |
| Decision | ID, scope, rationale, source, approval status, creation revision, supersedes / superseded-by |
| Artifact | ID, task/attempt, producer, path or object reference, content digest, code revision, sensitivity |
| Check | ID, command/tool and version, environment, tested revision, relevant file digests, outcome, evidence reference, timestamp |
| Handoff | Producer, recipient, task/attempt, summary, artifacts, decisions, checks, open findings, expected next action |
| Developer message | Message/task/attempt IDs, sender/recipient, type, contract/code revision, question or proposal, impact, next action, resolution/acknowledgement reference |
| Event | Stable event ID, mission/task/attempt, actor, timestamp, event type, relevant record references |

Check outcomes include passed, failed, not run, unavailable and stale. A command
that exits successfully after discovering zero tests is not evidence of tested
behavior. Record collection counts and expected checks where relevant. Never store
private chain-of-thought; store concise decisions, rationale and observable evidence.

## Retrieve only the task context

1. Load applicable policy, mission identity and the compact checkpoint summary.
2. Validate the saved revision against the current branch, working tree and task.
3. Load approved requirements, relevant decisions, dependency outputs and findings.
4. Identify touched files and direct dependencies using file paths, symbols,
   imports, contracts, relevant diffs and targeted search.
5. Supply bounded excerpts plus artifact references to the assigned role. Fetch
   more when needed rather than silently truncating a required contract.
6. Use full inspection when necessary for integration, security or a broad change.

An index is a navigation aid. It must never claim a whole module is correct merely
because a summary says so. Cache only with keys including project/access scope,
task inputs, relevant code/policy versions and tool configuration. Invalidate when
these inputs change. Never share private context across projects or users.

## Checkpoints, stale results and restart

- Persist node results and the next safe transition atomically where possible.
- Record external action intent with an idempotency key before branch/PR creation;
  reconcile the actual remote result before retrying after an interruption.
- A checkpoint cannot guarantee exactly-once API execution, billing or external
  effects. If a paid call may have finished before its result was saved, record
  uncertainty and reconcile rather than blindly repeat it.
- Bind tests and approvals to a revision and relevant content digests. Changed
  code, requirements, tools or configuration invalidate affected evidence. When
  impact is uncertain, mark stale and rerun; do not infer a pass.
- Record failed attempts and fixes. Do not overwrite a failure with an optimistic
  summary. Checkpoint completion is distinct from human acceptance and PR merge.
- Resume only a valid pending stage; completed stages should not rerun without a
  changed input, missing evidence or an explicit reason. Enforce bounded retries,
  cancellation, and elapsed-time/resource limits across restarts.

## Ownership and public/private storage

The controller validates state and permissions; agents propose updates. The lead
owns approved mission decisions, developers own implementation handoffs, QA owns
test findings, and security owns its findings. The developer cannot self-approve.
Use conflict detection for concurrent updates; update the task result and its
evidence references consistently. Historical events are append-only; corrections
are new linked records. Retention and redaction policy must allow deletion of
sensitive data without claiming history is an undeletable secret archive.

Frontend and Backend own separate implementation boundaries, described in
[DESIGN.md](DESIGN.md). Persist structured coordination and contract acknowledgements
with the affected task. An unresolved material question blocks dependent work;
contract changes require lead review and invalidate affected evidence. Sequential
activation of only necessary developer roles is the MVP default.

Only sanitized design and short project context belong in public Git. Runtime
databases, private code, execution logs and credentials stay in an access-controlled
local/private store outside tracked files. Publish sanitized evidence summaries
and references where authorized, not full logs by default.

## Verification before claiming a working memory system

- Restart mid-mission: recover the pending stage without losing completed work.
- Interrupt after external PR creation: reconcile instead of creating a duplicate.
- Change code or requirements after tests: stale results cannot unlock acceptance.
- Fail a test, repair and retest: preserve each attempt and its actual evidence.
- Miss or contradict a summary: expand relevant inspection and correct the memory.
- Run unrelated projects: context and cached results cannot cross access boundaries.
- Compare the same representative tasks with and without selective retrieval:
  record input/output tokens, repeated reads, latency, correctness and failure cases.
  Agree budgets from evidence; do not promise a percentage reduction in advance.

The current documentation delivery verifies links, policy preservation, graph
consistency and recorded evidence only. Runtime scenarios above remain unimplemented.

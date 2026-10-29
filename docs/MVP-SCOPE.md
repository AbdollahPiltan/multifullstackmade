# v0.1 scope and acceptance baseline

Scope record MVP-001, authored 2026-10-29 for the owner's request to complete
stage one. This is a reviewable product definition, not implementation or a claim
that the owner has approved every detail below. It builds on approved role decision
DEV-001. Delivery remains subject to PR review. No application code is authorized
by this document alone.

## 1. Outcome and intended user

One developer runs an AI development team locally, agrees on a bounded module with
the Tech Lead, and receives inspectable source changes, documentation, actual test
evidence and a GitHub pull request. The run can pause, survive a process restart,
and continue with relevant saved context rather than replaying the entire project.

The product is the team orchestrator. The notes module below is its acceptance
fixture, not a change in the product's purpose and not a claim that it can already
build arbitrary production applications.

## 2. First-use boundary

- One human operator, one project and one active mission at a time.
- A local command-line entry point with conversation through the lead, plan
  approval, status inspection, pause/resume, cancellation and delivery inspection.
  Exact command names and transport are later design decisions.
- Inspectable task/dependency graph and event timeline as bounded text or a file
  export; a live interactive dashboard is outside this first release.
- Five independent roles: lead/architect, Frontend, Backend, QA/API Tester and
  Security Reviewer. Activate only needed roles and execute sequentially.
- One supported target stack, one configured real model-provider integration and
  one execution environment. Stage-two selections are recorded in
  [ARCHITECTURE.md](ARCHITECTURE.md); the model identifier remains configured.
- One small, explicitly selected local repository or a fresh fixture workspace.
  The supplied scaffold, allowed paths and starting revision are recorded inputs.
  General large/legacy repositories are outside initial acceptance.
- Durable project-scoped state, checkpoints, decisions, handoffs and check evidence.
  Retrieve relevant files and dependencies; expand inspection when evidence demands it.
- One coherent delivery PR for the fixture; developers submit separate attributed
  changes/handoffs within the mission rather than generating a PR for each message.
- Actual model-backed execution must be distinguished from an optional deterministic
  development demo. A simulated run cannot establish real-provider acceptance.

## 3. Mission inputs

| Input | Minimum required information |
| --- | --- |
| Request | Desired behavior, constraints and examples, expressed to the lead |
| Workspace | Explicit project/repository identity, clean baseline or deliberate handling of existing changes, allowed paths |
| Requirements | Acceptance criteria and the plan the human approves |
| Policy | Applicable instruction revision, role permissions and required gates |
| Provider configuration | Available provider/model and credential reference outside tracked source |
| Execution limits | Explicit maximum attempts, model/tool calls, elapsed time and output/resource limits before work starts |
| GitHub destination | Authorized owner/repository, base branch and permitted branch/PR actions |

Missing material inputs produce a consolidated question from the lead or a visible
blocked state. Numerical limits must be selected and enforced before execution;
this scope does not invent cost or performance guarantees.

## 4. Canonical operator journey

1. Submit the fixture request and workspace to the lead.
2. The lead identifies gaps, proposes architecture, ownership, acceptance criteria,
   dependencies and an API-contract milestone. No implementation starts before
   human plan approval. Contract changes later follow the approved escalation policy.
3. Backend and Frontend acknowledge a versioned contract before connected work.
   The scheduler records dependencies and gives each role the required context.
4. Each active developer produces attributed changes, tests and a structured handoff.
5. Execute actual automated checks and capture revision-bound evidence. QA validates
   the real combined feature and APIs. Security reviews the relevant design/changes.
6. Return actionable failures to their owner; repair within recorded limits. Missing,
   stale or failed required checks cannot advance the mission to acceptance.
7. The lead reviews the current revision, independently of implementation ownership.
8. Present the PR and delivery report to the human. Acceptance, merge and deployment
   are separate events; the MVP never automatically merges or deploys.

The human can inspect status and handoffs throughout. Only the lead asks product
questions; developer coordination remains inspectable and recorded.

## 5. First acceptance fixture: personal notes module

This small fixture deliberately exercises both developer roles and persistent data.
It is a proposed default chosen for stage one, replaceable through a recorded scope
revision if the owner prefers another example.

| Capability | Expected observable behavior |
| --- | --- |
| Create | Enter a nonblank title (1–120 characters after trimming) and optional body (up to 5,000 characters); save one note with a stable ID |
| List | Show saved notes with title and body; display an explicit empty state when none exist |
| Edit | Change title/body and see the saved values after reload |
| Delete | Explicitly confirm deletion; remove only the selected note |
| Persistence | Data survives restarting the sample application |
| Validation | Server rejects invalid titles/oversized fields; UI presents useful errors and retains editable input |
| Missing record | API reports a missing note without disguising it as a successful edit/delete |
| User states | Show loading, empty, failure and repeated-submit behavior; prevent accidental duplicate requests in the UI |
| Output safety | Note text renders as text; stored markup must not execute in the browser |
| Local boundary | Sample services bind to loopback and use synthetic local data; there is no hosted, authenticated, multi-user product in this fixture |

API routes, schemas, status conventions, data storage, file layout and test tooling
are chosen in later architecture/contract stages. The contract must capture the
behavior above. Any local service still needs appropriate input/origin/request bounds;
loopback binding does not waive security review. No real private notes are required.

## 6. Required delivery bundle

- Baseline and final code revision, change manifest, task ownership and versioned
  API contract with acknowledgements and relevant messages.
- Runnable fixture source, setup/run instructions, configuration example without
  credentials, developer tests and independent QA/integration tests.
- Check ledger: command/tool, environment, revision, timestamps, discovered/executed
  test counts, exit status/outcome and sanitized evidence references.
- Security findings with severity, evidence and resolution; unresolved blocking
  findings prevent lead acceptance. Review does not certify complete security.
- Lead verdict against each criterion, remaining limitations, usage summary and
  human next action. Failed/blocked delivery must remain explicit.
- One reviewable GitHub PR with validation evidence and recovery notes. Role-level
  assessments are not represented as independent GitHub approvals unless the
  later identity/permission design actually supports that distinction.

## 7. Product acceptance matrix

These are required future verification scenarios, not tests already executed.

| ID | Scenario | Pass condition |
| --- | --- | --- |
| AC-01 | Lead conversation and plan approval | Material ambiguity reaches the human through the lead; no code-writing stage starts before approval |
| AC-02 | Selective roles and ownership | Notes fixture uses both developer roles; a backend-only variation does not invoke Frontend unnecessarily; no developer self-approval |
| AC-03 | Contract and communication | Both developers reference the accepted version; material unanswered questions block dependent work; change requests reach the lead |
| AC-04 | End-to-end fixture | Create/list/edit/delete work through the real UI and API, persist across fixture restart, and match validation/error/output-safety criteria |
| AC-05 | Genuine checks | Tests actually collect and execute; zero collected tests, unavailable tools, or a textual agent claim cannot count as coverage or a pass |
| AC-06 | Repair | A controlled failing-test exercise records failure, owner, fix and rerun; exhausted configured limits produce a blocked result |
| AC-07 | Restart | Interrupt after a durable completed stage and restart; recover its evidence and next pending stage without needlessly repeating completed work |
| AC-08 | Stale evidence | Change relevant code or contract after a passing check; acceptance is blocked until affected evidence is refreshed |
| AC-09 | External reconciliation | Interrupt after remote PR creation; resume by reconciling the existing PR rather than creating a duplicate |
| AC-10 | Context and resource accounting | Record model input/output usage and source reads; a repeated unchanged task reuses valid context; expand inspection when inputs change. No unmeasured savings percentage |
| AC-11 | Isolation and private data | Negative checks prevent unauthorized path/tool access and credential/log exposure; generated code executes only in the selected isolated environment |
| AC-12 | Cancellation | Stop scheduling new work and cancel active work where supported; record residual external actions rather than claiming they were undone |
| AC-13 | Review and human delivery | Required QA/security checks and lead verdict concern the delivered revision; human receives the bundle and PR; no automatic merge/deploy |

The exact test cases and repeatable commands belong to implementation milestones.
Do not introduce false-success shortcuts just to reach a terminal graph node.

## 8. Explicitly outside v0.1

Multi-user hosting, billing, organization administration, production deployment,
arbitrary legacy projects, mobile clients, autonomous merge, parallel worker teams,
dedicated database/docs/CI agents, interactive orchestration dashboards, cross-project
memory sharing and mandatory vector/graph database services are deferred. The sample
notes UI is distinct from an orchestration dashboard and remains in scope.

## 9. Stage-one completion and next boundary

Stage one delivers this scope baseline, fixture behavior, inputs/outputs, exclusions
and measurable acceptance matrix, linked from the project brief, task ledger and
memory. Its documentation checks and checkpoint are recorded in the delivery PR.
Task T-009 remains awaiting review until the scope PR is accepted; T-010/T-011
now have stage-two selections in ARCHITECTURE.md, awaiting their own PR review. No feature
is marked implemented because its acceptance criteria have been written.

Stage two selects the stack, minimum architecture, interfaces and execution model
against this baseline. Detailed role contracts, command schemas, schemas/retention,
numeric limits and infrastructure/tool choices remain subsequent design work.
Implementation still requires a separate instruction from the owner.

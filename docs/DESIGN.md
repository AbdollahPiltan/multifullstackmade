# Proposed MVP design

Status: discussion draft. This document describes intended behavior, not existing code.

Detailed graph, memory records, context retrieval and restart semantics are in
[GRAPH-MEMORY.md](GRAPH-MEMORY.md). Current manual continuation starts at
[MEMORY.md](../MEMORY.md).

Stage-two technology and execution decisions: [ARCHITECTURE.md](ARCHITECTURE.md).
The authoritative stage-three role, path and tool permissions are in
[AGENT-CONTRACTS.md](AGENT-CONTRACTS.md); role summaries below are an overview.

Stage-four serialized API/message/tool contracts: [PROTOCOL-CONTRACTS.md](PROTOCOL-CONTRACTS.md).

Stage-five detailed graph/storage and restart design: [STATE-001](STATE-PERSISTENCE.md).

## Engineering policy

[AGENTS.md](../AGENTS.md) governs the whole repository; [PROJECT.md](../PROJECT.md)
records product decisions, authorization, milestones, and recovery context.
The proposed runtime must provide applicable policy requirements to each role and
enforce relevant permissions, limits, evidence, and approval gates through the
controller and CI. Policy text is not an implemented enforcement mechanism.

Future agents working on another repository must also read that target's approved
requirements and applicable instructions. Record the policy revision used for a
mission and reference rule IDs in findings and exceptions.

## Product boundaries

The first useful outcome is one bounded software module delivered with source,
documentation, independently executed tests, and review evidence. Start with a
single-user local application and one active mission per project. The notes demonstration fixture and minimal operator interface are defined in
[MVP-SCOPE.md](MVP-SCOPE.md); target languages and execution boundaries are selected in ARCHITECTURE.md.

The human communicates with the Tech Lead. Specialists may surface questions to
the lead, who consolidates questions and escalates changes to the approved scope.

## Roles and outputs

| Role | Responsibilities | Deliverables |
| --- | --- | --- |
| Tech Lead / Architect | Clarify requirements; define acceptance criteria, architecture, interfaces, tasks, and dependencies; coordinate work; review the result | Approved plan, architecture decisions, task graph, reasoned final review |
| Frontend Developer | Own presentation, interactions, accessibility, client state, API integration, and frontend tests/documentation; fix client defects | UI changes, contract-bound fixtures, frontend tests/docs, pull request |
| Backend Developer | Own business rules, API implementation, server validation/authorization, data schema/migrations, and backend tests/documentation; fix server defects | API/data changes, versioned contract, backend tests/docs, pull request |
| QA / API Tester | Derive independent scenarios from requirements and API contracts; execute functional, API, and integration tests; reproduce defects; verify fixes | Test definitions, execution evidence, reproducible defect reports |
| Security Reviewer | Review design risks, authorization, input boundaries, sensitive data, and dependencies; inspect scanner evidence; verify fixes | Findings with severity, location, revision, rationale, and remediation status |

The developer cannot approve their own work. QA must not weaken acceptance criteria
to make tests pass. The lead cannot override required failing checks. Security
review and scanners provide evidence, not a guarantee that a system is secure.

Architecture and test planning happen before implementation; security feedback can
also occur at design time. Separate role prompts, tools, contexts, and permissions
are more important than assigning every role a different model.

## Developer separation and coordination

Decision DEV-001 (2026-10-29, approved by the owner): replace the previous combined
Full-stack proposal with distinct Frontend and Backend roles from the MVP. The
five roles are defined independently; activate only those a task actually needs.
An API-only task does not automatically invoke Frontend. A UI-only task without
contract changes need not invoke Backend. Begin with sequential scheduling;
dependency-aware parallel execution remains a later capability.

The lead owns boundaries and acceptance criteria. Backend owns business rules and
data access; Frontend owns presentation and client interaction. Client validation
does not replace server validation. Database responsibilities stay with Backend
until a dedicated database role is justified. The lead assigns initial CI changes
to the appropriate developer; configuring CI does not create a separate agent.
Neither developer approves their own implementation or changes another role's
owned files without an explicit reassignment recorded by the lead.

Before work that connects the two roles, record a versioned API contract: methods,
paths, request/response schemas, errors, authorization, pagination/limits where
relevant, and representative valid/invalid examples. A machine-readable format
such as OpenAPI can be selected when the stack is agreed; no generator or package
is required now. Both developers acknowledge the contract; the lead accepts it as
part of the plan. Frontend fixtures refer to that version, not invented responses.

Coordination uses bounded, task-linked messages rather than an unrestricted chat:

| Message field | Meaning |
| --- | --- |
| Message / task / attempt IDs | Stable identity and traceable context |
| Sender and recipient roles | Who is asking and who must act |
| Type | Question, proposal, answer, change request, acknowledgement, or handoff |
| Contract version and code revision | Exact assumptions the message concerns |
| Question / proposal | Concrete issue with only relevant excerpts or artifact references |
| Impact and requested next action | Affected behavior, dependencies, acceptance criteria, and expected response |
| Resolution reference | Accepted answer or lead decision; unresolved issues stay visible |

Messages, decisions and acknowledgements are project-memory records. Direct
developer coordination is allowed within the approved contract. Contract, scope,
architecture or ownership changes go to the lead, who asks the human when needed.
Silence is not acknowledgement. Block dependent work while a material question is
unresolved; apply recorded attempt/time limits rather than an endless conversation.
Each role loads relevant contract/decision excerpts, not the other role's entire
conversation or repository. The human continues to communicate through the lead.

For a connected feature, the lead records sequencing and dependencies. Each role
delivers its changes and tests against the accepted contract. QA verifies actual
API behavior, fixture compatibility, and the combined frontend/backend scenario;
mock-only tests or two separately passing PRs do not establish integration success.
Changed contracts invalidate dependent fixtures, implementation checks and approvals
until reconciled. Security review and final lead review remain independent gates.

## Workflow engine

A deterministic controller owns transitions, limits, persistence, and permissions.
Agents propose plans, changes, findings, and decisions within that controller.
The workflow engine is infrastructure, not another conversational agent.

Proposed task states:

- `planned`: owner, dependencies, deliverables, and acceptance criteria recorded.
- `ready`: dependencies satisfied.
- `in_progress`: owner is working.
- `awaiting_checks`: a concrete revision is available for validation.
- `changes_requested`: checks or reviewers identified actionable issues.
- `awaiting_lead`: required checks and independent reviews passed.
- `awaiting_human`: lead accepted the result; merge or deployment needs a human.
- `done`: the defined delivery was accepted and recorded.
- `blocked`: an external dependency, exhausted limit, or unresolved issue needs action.
- `cancelled`: the human cancelled the task.

Task graphs include dependencies and revision loops. The displayed graph must
distinguish a role from an individual task or execution attempt.

## Three persistence concerns

1. **Execution state:** current node, completed work, pending dependencies, attempts,
   limits, and checkpoints used to resume a run.
2. **Project memory:** approved requirements, API contracts, architecture decisions,
   unresolved questions, and relevant prior outcomes. Each entry has a source,
   scope, version, and supersession status.
3. **Audit history and artifacts:** timestamped handoffs, owners, code revisions,
   test results, findings, review decisions, and references to produced files.

Store artifacts separately from their metadata. Context supplied to each agent
should contain the relevant approved facts and artifacts, not every conversation.
Cross-project memory sharing is outside the initial scope.

## Handoff contract

Every handoff records:

- Mission, task, attempt, producer, and intended recipient.
- Completed work and remaining questions.
- Artifact paths and exact code revision or content digest.
- Checks executed, results, evidence references, and known limitations.
- Blocking findings and the expected next action.
- Creation time and the requirement or decision that justified the work.

## Pull requests and gates

Use one PR per coherent change, rather than one PR for each agent message. A PR
progresses through checks, QA and security review, then lead review. Fixes update
that PR. The combined module is tested again before final delivery.

Approvals bind to the tested revision and applicable acceptance criteria. Relevant
checks and approvals are invalidated after changes. Missing, failed, stale, or
unavailable required checks cannot count as success.

Agent roles do not automatically imply separate GitHub accounts. Distinguish
internal role assessments from GitHub-native review approvals. Identity,
permissions, and enforcement need an explicit integration design.

## Execution and recovery

- Keep execution workspaces separate from credentials and controller data.
- Run generated code in an isolated environment with bounded resources.
- Record model calls, tool actions, failures, and retry counts.
- Bound repair loops and execution time; escalate exhausted limits to the lead.
- Resume completed steps from durable checkpoints.
- Use idempotency keys and reconciliation for external actions such as PR creation.
  A checkpoint alone does not guarantee exactly-once effects or billing.
- Keep merge and deployment under human control in the MVP.

## Open decisions

- Exact locked dependency/image versions and minimal scaffold details for the selected stack.
- CLI commands and bounded graph/status export details; the stage-one operator interface is local CLI.
- Detailed application schema, migrations and retention within the selected SQLite architecture.
- Detailed provider interface and model identifiers per role within the selected OpenAI adapter.
- Validated Docker profiles, numerical limits and exact permitted tool schemas.
- GitHub authentication, bot identity, review enforcement, and artifact storage.
- Numeric budgets, retry limits, and the definition of an accepted delivery.

No runtime or integration has been implemented yet.

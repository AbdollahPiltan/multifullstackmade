# Proposed MVP design

Status: discussion draft. This document describes intended behavior, not existing code.

## Product boundaries

The first useful outcome is one bounded software module delivered with source,
documentation, independently executed tests, and review evidence. Start with a
single-user local application and one active mission per project. The first target
language and demonstration module remain open decisions.

The human communicates with the Tech Lead. Specialists may surface questions to
the lead, who consolidates questions and escalates changes to the approved scope.

## Roles and outputs

| Role | Responsibilities | Deliverables |
| --- | --- | --- |
| Tech Lead / Architect | Clarify requirements; define acceptance criteria, architecture, interfaces, tasks, and dependencies; coordinate work; review the result | Approved plan, architecture decisions, task graph, reasoned final review |
| Full-stack Developer | Implement source, API and data changes; write unit tests and usage documentation; configure initial CI; fix reported defects | Versioned code changes, unit tests, documentation, pull request |
| QA / API Tester | Derive independent scenarios from requirements and API contracts; execute functional, API, and integration tests; reproduce defects; verify fixes | Test definitions, execution evidence, reproducible defect reports |
| Security Reviewer | Review design risks, authorization, input boundaries, sensitive data, and dependencies; inspect scanner evidence; verify fixes | Findings with severity, location, revision, rationale, and remediation status |

The developer cannot approve their own work. QA must not weaken acceptance criteria
to make tests pass. The lead cannot override required failing checks. Security
review and scanners provide evidence, not a guarantee that a system is secure.

Architecture and test planning happen before implementation; security feedback can
also occur at design time. Separate role prompts, tools, contexts, and permissions
are more important than assigning every role a different model.

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

- First target language, repository shape, and demonstration module.
- CLI versus a small web interface; how the graph is inspected.
- Python / LangGraph / SQLite versus alternatives; schema and migration strategy.
- Model provider abstraction and configurable model selection per role.
- Sandbox implementation, permitted commands, and network policy.
- GitHub authentication, bot identity, review enforcement, and artifact storage.
- Numeric budgets, retry limits, and the definition of an accepted delivery.

No runtime or integration has been implemented yet.

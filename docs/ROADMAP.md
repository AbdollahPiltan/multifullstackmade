# Roadmap

The release capabilities below are proposed goals. Current task status and completion
evidence live only in [TASKS.md](../TASKS.md). There are no released versions or
completed runtime features yet. The stage-one baseline and future acceptance matrix
are in [MVP-SCOPE.md](MVP-SCOPE.md); scope review is not runtime completion.

## v0.1 — Local MVP

- Review the notes fixture and acceptance baseline, then select its target language.
- Finalize role inputs, outputs, permissions, and the handoff schema.
- Implement an explicit workflow graph and durable local checkpoints.
- Record project decisions, task ownership, artifacts, and an audit timeline.
- Add a deterministic demo mode and a configurable real model provider.
- Implement the five initial roles with selective activation, sequential scheduling, versioned API contracts, and bounded revision loops.
- Isolate generated code execution and capture actual test results.
- Integrate branch / PR creation with revision-bound review evidence.
- Require independent QA and security checks before lead acceptance.
- Leave merge and deployment to a human.
- Demonstrate interruption, restart, failed tests, repair, and final delivery.

Acceptance: one module moves from an approved plan to a reviewable delivery;
state survives a process restart; failures cannot silently become successes;
every handoff and decision is attributable and tied to its artifacts.

## v0.2 — Specialist teams and visibility

- Separate a dedicated database role from Backend where useful; Frontend and Backend are already distinct in v0.1.
- Add dedicated architecture, documentation, and CI/CD roles as needed.
- Visual task graph and artifact / evidence inspection.
- Dependency-aware parallel tasks with conflict handling and integration tests.
- Improve context retrieval, usage reporting, and provider configuration.

## v0.3 — Shared use

- Multi-user project isolation and access control.
- Durable workers, resumable jobs, and remote execution environments.
- Team-level policies and audited approval workflows.
- Deployment integration with explicit permissions and release controls.

## Branches and versions

`main` is the integration branch. Use short-lived branches such as `feat/<topic>`,
`fix/<topic>`, and `docs/<topic>`, reviewed through pull requests. Mark actual
releases with version tags. Use a maintenance branch only when a released version
needs ongoing support; do not create speculative version branches in advance.

## Next discussion

Review MVP-001, then select the stack and minimal architecture in stage two.
Implementation needs a separate instruction after the design work.

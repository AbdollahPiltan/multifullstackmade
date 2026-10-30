# multifullstackmade

A graph-based AI development team with a Tech Lead, persistent project memory,
independent testing, security review, and traceable handoffs.

[فارسی](README.fa.md) · [Design](docs/DESIGN.md) · [Roadmap](docs/ROADMAP.md) · [Contributing](CONTRIBUTING.md)

Engineering policy: [AGENTS.md](AGENTS.md), adopted from
[Strict Development Rules](https://github.com/AbdollahPiltan/strict-development-rules).
Project decisions, current scope, and progress: [PROJECT.md](PROJECT.md).
Completed work, pending reviews, and remaining tasks: [TASKS.md (فارسی)](TASKS.md).
Resume work from [MEMORY.md](MEMORY.md); read the proposed
[graph and memory design](docs/GRAPH-MEMORY.md) when relevant.

Stage-one product scope: [MVP-SCOPE.md](docs/MVP-SCOPE.md).
Selected stage-two architecture: [ARCHITECTURE.md](docs/ARCHITECTURE.md).

Stage-three role contracts and tool permissions: [AGENT-CONTRACTS.md](docs/AGENT-CONTRACTS.md).

Stage-four API/message/tool schemas: [PROTOCOL-CONTRACTS.md](docs/PROTOCOL-CONTRACTS.md).

Stage-five graph, storage and recovery: [STATE-PERSISTENCE.md](docs/STATE-PERSISTENCE.md).

Stage-six limits, repair and cancellation: [EXECUTION-LIMITS.md](docs/EXECUTION-LIMITS.md).

Stage-seven sandbox and tool-access design: [SANDBOX-PROFILES.md](docs/SANDBOX-PROFILES.md).

Stage-eight GitHub identity and delivery: [GITHUB-DELIVERY.md](docs/GITHUB-DELIVERY.md).

## Status

**Planning / pre-MVP.** This repository currently contains the project specification
and contribution guidelines. There is no runnable application, agent runtime, or
working GitHub automation yet. Everything described below is planned behavior.

## The idea

Describe a software module to a Tech Lead. Agree on its requirements and acceptance
criteria. The lead plans and delegates implementation, testing, and security review.
Track each task, decision, delivery, and revision through a persistent execution graph.

The human talks to the Tech Lead; specialist activity remains inspectable.

## Proposed MVP

- One user, one project, and one bounded development mission at a time.
- Five roles: Tech Lead / Architect, Frontend Developer, Backend Developer, QA / API Tester,
  and Security Reviewer.
- An explicit workflow graph with durable checkpoints and restart recovery.
- Project memory for approved requirements, decisions, artifacts, and evidence.
- Activate only the developer roles a task needs; start with sequential execution.
- Versioned API contracts, structured developer messages, and isolated workspaces.
- A pull request workflow: automated checks, independent QA and security review,
  then Tech Lead review. Human approval controls merge and deployment.
- Bounded retries and execution limits, with escalation to the lead on failure.

These are proposed scope boundaries, not implemented features or a final stack decision.

## Proposed workflow

1. Human and Tech Lead agree on requirements, architecture, and acceptance criteria.
2. The lead assigns tasks, owners, dependencies, and expected deliverables.
3. The developer implements code, unit tests, documentation, and CI configuration.
4. A pull request triggers automated checks.
5. QA tests behavior and APIs; the Security Reviewer examines risks and findings.
6. Failed checks or blocking findings return to the responsible role for revision.
7. The lead reviews the current revision after the required checks pass.
8. The human decides whether to merge or deploy.

Every approval and test result must refer to an exact code revision. Relevant
checks rerun after changes. Combined changes require integration testing.

## Development direction

The selected baseline is Python 3.12, LangGraph, SQLite, a local CLI, an OpenAI
Responses adapter and Docker execution. The notes fixture uses FastAPI and plain
browser HTML/CSS/JavaScript. See ARCHITECTURE.md for boundaries and alternatives.
These are architecture decisions, not installed dependencies or verified runtime
features; exact versions, role permissions and operation schemas follow later.

Use short-lived feature branches and pull requests into `main`. Use version tags
for releases; create long-lived version branches only when a supported release
needs independent maintenance.

## Participate

Start with [the roadmap](docs/ROADMAP.md) and propose changes through issues.
Contributions to scope, failure recovery, acceptance criteria, and role boundaries
are welcome before implementation begins.

## License

[MIT](LICENSE).

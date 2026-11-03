# Project memory / حافظهٔ ادامهٔ کار

Updated: 2026-11-03. Compact derived context, not a runtime memory service.
Verify Git, applicable policy and relevant evidence before relying on this summary.

## Start here

1. Follow AGENTS.md, read this file, then check Git status/log and relevant PR state.
2. Load only matching TASKS.md rows, PROJECT.md decisions and linked source/evidence.
3. Expand inspection for dependencies, stale/missing evidence or contradictions.
4. Before handoff update compact memory, task evidence and material decisions.
   Keep detailed history in Git/PRs; never reduce required correctness/security checks.

## Confirmed constraints and authorization

- Public MIT repository: AbdollahPiltan/multifullstackmade. Preserve all 75 upstream
  normative rules and the MIT notice; source provenance is pinned in AGENTS.md.
- Human primarily talks to Tech Lead; five roles are lead, frontend, backend, qa,
  security, selectively activated and sequential in the initial MVP.
- Owner explicitly requested stage nine and then continuation/completion: T-018
  executable foundation, dependency/tool setup, tests/build/CI and PR are authorized.
  Earlier design-only authorization is superseded for this scoped milestone.
- Do not automatically implement T-019 onward, merge/deploy, change settings, call
  paid models or claim a qualified sandbox/GitHub mission adapter exists.
- Python 3.12.14 / uv 0.13.6, LangGraph + SQLite adapter, Pydantic v2 and jsonschema
  are installed/locked. Optional OpenAI, FastAPI/Uvicorn and Playwright packages
  are locked/import-checked; no notes server, browser or model call is started.
- CLI --version and contracts work. doctor deliberately exits 1 because mission
  execution is absent; executable discovery is not auth/daemon/host qualification.
- No direct main pushes, force-pushes or automatic merge. Use verified feature PRs.
- Credentials, execution databases, private source/state/transcripts remain outside Git.

## Retrieval index

| Need | Read |
| --- | --- |
| Engineering policy and provenance | [AGENTS.md](AGENTS.md) |
| Scope, authorization, decisions, recovery | [PROJECT.md](PROJECT.md) |
| Single task/status/evidence ledger | [TASKS.md](TASKS.md) |
| Setup, actual CLI, required checks and package boundaries | [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) |
| Overview and cooperation | [docs/DESIGN.md](docs/DESIGN.md) |
| Graph/memory overview | [docs/GRAPH-MEMORY.md](docs/GRAPH-MEMORY.md) |
| Notes fixture and AC-01–AC-13 | [docs/MVP-SCOPE.md](docs/MVP-SCOPE.md) |
| Stack and module boundaries | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Role/tool/path authority | [docs/AGENT-CONTRACTS.md](docs/AGENT-CONTRACTS.md) |
| Canonical wire/API schemas | [docs/PROTOCOL-CONTRACTS.md](docs/PROTOCOL-CONTRACTS.md) |
| Domain/checkpoint/artifact consistency and retention | [docs/STATE-PERSISTENCE.md](docs/STATE-PERSISTENCE.md) |
| Numeric budgets, retry/repair/cancellation | [docs/EXECUTION-LIMITS.md](docs/EXECUTION-LIMITS.md) |
| Isolation and image/host qualification | [docs/SANDBOX-PROFILES.md](docs/SANDBOX-PROFILES.md) |
| Publication principal, draft CI and reconciliation | [docs/GITHUB-DELIVERY.md](docs/GITHUB-DELIVERY.md) |
| Future release goals | [docs/ROADMAP.md](docs/ROADMAP.md) |

## Checkpoints and continuation

- PR #1 (policy/tasks) was verified merged on 2026-10-29. Earlier design deliveries
  remain traceable in TASKS.md, Git and PRs #2/#4–#11; do not infer merge from a summary.
- `81b762a` / PR #12: GH-001; 57 synthetic cases, prior validators, 43 files/194
  local links and policy/MIT preservation checked. PR #12 verified open at stage-nine start.
- Current branch: codex/executable-scaffold, based on open PR #12's codex/github-delivery.
  Deliver against that dependency; verify ancestry before later retargeting.
- Current T-018 output: installable 0.1.0a1 package, read-only CLI, locked environment,
  controller tests and CI source; `5b3188a`, [PR #13](https://github.com/AbdollahPiltan/multifullstackmade/pull/13),
  awaiting maintainer review. Native CI results are linked in that PR; verify latest head.
- Actual local checks so far: 22 pytest tests, mypy, Ruff, offline secret scan and
  all five design validators passed. Source/wheel build and a hash-locked fresh
  wheel install outside checkout passed. OSV advisory audit found no known
  vulnerabilities in 104 applicable records on 2026-10-31 (strict OSV audit).
  Local tests/lint/types rechecked on 2026-11-03; native CI evidence belongs in the PR.
- Doctor/catalog inspect the installed bundle; they do not run a graph mission,
  load target code, access credentials or invoke Docker/GitHub/provider operations.
- Next task is T-019 mission graph/checkpoint implementation, then T-020 memory;
  T-021–T-026 retain demo/provider/roles, qualified sandbox, GitHub and full acceptance.

## Runtime invariants still to implement

- One project/mission, five sequential roles, notes browser/API CRUD fixture; real
  combined QA/security checks and exact-revision human delivery are required.
- Controller alone validates permissions, evidence and state. No role receives raw
  shell/network/SQL, credentials, Docker socket or direct GitHub/merge/deploy authority.
- Domain results are authoritative; checkpoints are separate/opaque and artifacts
  immutable. Reconcile unknown effects and preserve reservations across restart.
- LIM-001: 40 model requests/mission, 2 repairs/task and 6/mission, 3,600 active
  seconds and 86,400 lifetime seconds; no automatic resets or hidden retry layers.
- SBX-001: no egress/host mounts/credentials, bounded resources, reviewed browser
  seccomp derivative only where qualified. All six image releases remain null.
  Docker CLI is absent locally; real SB-01–SB-12 are not tested.
- GH-001: one operator User principal; local gates -> draft -> native CI -> final
  lead verdict -> ready -> human acceptance. No fabricated native reviews; unknown
  creates require reconciliation. Runtime binding/check manifest remain unconfigured.
- Foundation CI tests controller source, not generated code or product-mission gates.

## Trust and maintenance

Source/evidence outrank stale summaries; human instructions outrank saved plans.
Correct summaries with linked provenance. Never store private reasoning, secrets,
full transcripts or private run logs here. Keep this file below ~120 lines; use
linked documents/Git for detail. Token savings are not a measured result.

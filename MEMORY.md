# Project memory / حافظهٔ ادامهٔ کار

Updated: 2026-10-30. This is a compact, human-maintained project summary, not a
running memory service. Verify it against Git and the current task before relying on it.

## Start here

1. Follow applicable AGENTS.md instructions, then read this short file.
2. Check `git status --short --branch` and `git log -3 --oneline`; verify the
   relevant PR state when publication or merge status affects the task.
3. Read only the matching task rows in [TASKS.md](TASKS.md), relevant decisions in
   [PROJECT.md](PROJECT.md), and the files linked below. Use targeted searches.
4. Expand inspection when changes, dependencies, missing evidence, or contradictions
   require it. Never skip necessary code or security review to save tokens.
5. At handoff update this summary, the affected task rows, and evidence references.
   Keep historical detail in Git / PRs; do not grow this file into a transcript.

## Confirmed constraints

- Public repository: AbdollahPiltan/multifullstackmade; MIT license.
- The human primarily talks to the Tech Lead. Track task ownership, handoffs,
  decisions, code revisions, and actual test evidence in a persistent workflow.
- Finish design discussion before implementing application code. Current authorization
  covers stage-seven sandbox/tool-access design, static policy fixtures and
  GitHub delivery; not an API server, agent runtime or permission engine.
- ARCH-001 selects Python 3.12, uv, argparse, LangGraph, SQLite, Pydantic v2,
  an OpenAI Responses adapter, Docker, Git/gh and pytest/HTTPX/Playwright Chromium.
  Notes uses FastAPI/Uvicorn plus plain HTML/CSS/JavaScript, with no Node build stack.
  Exact dependencies/images need locking and compatibility tests at scaffold.
- DEV-001 approves lead/architect, Frontend, Backend, QA/API Tester and Security;
  activate needed roles sequentially. No role runtime has been implemented.
- No application, runtime agents, database, automated checkpointing, or CI exists.
- No direct main pushes, force-pushes, automatic merging, or deployment.

## Retrieval index

| Need | Read |
| --- | --- |
| Applicable engineering policy | [AGENTS.md](AGENTS.md) |
| Scope, authorization, open decisions, recovery | [PROJECT.md](PROJECT.md), relevant sections only |
| Completed / pending work and evidence | [TASKS.md](TASKS.md), relevant task IDs only |
| Roles, handoffs, acceptance gates | [docs/DESIGN.md](docs/DESIGN.md) |
| Graph, memory records, retrieval, stale evidence | [docs/GRAPH-MEMORY.md](docs/GRAPH-MEMORY.md) |
| Stage-one inputs, outputs, fixture and acceptance | [docs/MVP-SCOPE.md](docs/MVP-SCOPE.md) |
| Stage-two stack, boundaries, sandbox and planned source layout | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Exact role authority, owned paths and review gates | [docs/AGENT-CONTRACTS.md](docs/AGENT-CONTRACTS.md) |
| Wire/API schemas, errors, tool formats and validation command | [docs/PROTOCOL-CONTRACTS.md](docs/PROTOCOL-CONTRACTS.md) |
| Durable commit/restart, graph fixture, SQL design, retention and restore | [docs/STATE-PERSISTENCE.md](docs/STATE-PERSISTENCE.md) |
| Numeric ceilings, persistent budgets, retry/repair, clocks and cancellation | [docs/EXECUTION-LIMITS.md](docs/EXECUTION-LIMITS.md) |
| Isolation, paths, six check profiles and image/host qualification | [docs/SANDBOX-PROFILES.md](docs/SANDBOX-PROFILES.md) |
| Release goals | [docs/ROADMAP.md](docs/ROADMAP.md) |

## Last recorded checkpoints and checks

| Checkpoint | Recorded outcome | Limit |
| --- | --- | --- |
| `a291371` on main | Initial public project documentation | Design only |
| `5eb38fd` in PR #1 | Root policy and brief; 75 original engineering rules and MIT notice preserved | PR #1 verified merged on 2026-10-29 |
| `0a77334` in PR #1 | TASKS.md, 35 unique task IDs; 13 files, 46 local links, whitespace and final-newline checks passed | Documentation checks, not application tests |
| `70c3724` in PR #2 | Graph/memory design; 15 files, 68 local links, 36 task IDs, 18 transitions, policy preservation and whitespace checks passed | Documentation only; PR #2 still open when checked |
| `9814f52` in PR #4 | DEV-001 role split; 15 files, 71 local links, 37 task IDs, five-role consistency and unchanged-policy checks passed | Documentation only; PR #4 verified open at scope-task start |
| `e955463` in PR #5 | Scope/notes fixture and AC-01–AC-13; 16 files, 78 links, 37 task IDs and documentation checks passed | PR #5 verified open at architecture-task start |
| `e669624` in PR #6 | ARCH-001; 17 files, 90 links, 37 task IDs, 13 acceptance cases, preserved 75 rules/MIT and documentation checks passed | PR #6 verified open at role-contract task start |
| `7ac3d2d` in PR #7 | ROLE-001; 18 files, 102 links, 37 tasks, five roles, 13 capability rows and 11 role cases checked; rules/MIT preserved | PR #7 verified open at protocol-task start |
| `2c2e191` in PR #8 | PROTO-001; 48 protocol + 11 API examples, 3 length boundaries, 11 tools and 5 operations validated | PR #8 verified open at stage-five start |
| `200c7cf` in PR #9 | STATE-001; 13 stages/18 edges, 11 tables, 17 rejected SQL cases, rollback/version conflict and synthetic backup checked; 28 files/135 local links and policy preserved | PR #9 verified open at stage-six start; synthetic checks on Python 3.10.6 / SQLite 3.37.2, no runtime integration claim |
| `f3863ca` in PR #10 | LIM-001; closed profile and 50 synthetic cases; earlier validators passed; 33 files/154 links, 37 tasks and 75 pinned rules/MIT checked | PR #10 verified open at stage-seven start; Python 3.10.6 tooling, no runtime enforcement |
| Current sandbox design | SBX-001; six frozen profiles/55 synthetic cases, prior validators passed; 38 files/172 local links and 75 pinned rules/MIT checked | Final commit in sandbox PR/report; Docker CLI absent, no image or real sandbox qualification |

## Current continuation

- Branch: `codex/sandbox-profiles`, based on open PR #10 (`codex/execution-limits`).
- Deliver the sandbox-design PR against that dependency. Verify ancestry before retargeting
  dependent PRs to main; do not auto-merge or rewrite shared history.
- T-016 tracks SBX-001, awaiting review; T-015 is the preceding limits policy.
  T-009/T-010/T-011/T-036/T-037 are prior documentation deliveries.
- OpenAPI defines five notes operations; the internal schema defines 11 typed tools.
  Schema validity is not authorization or real test evidence. Use
  scripts/validate_contracts.py with its documented disposable validation environment.
- ROLE-001 denies raw shell/network/credentials and direct GitHub writes to all
  roles. Lead proposes/coordinates; developers own product paths; QA/Security own
  independent tests. Shared config changes require separate validated authorization.
- MVP-001 selects a local single-user CLI orchestrator, sequential roles, inspectable
  graph, durable continuation and one reviewable PR. The notes browser/API fixture
  exercises create/list/edit/delete, validation, persistence and safe text rendering.
- AC-01–AC-13 define future checks, including restart, stale evidence, repair,
  reconciliation and usage accounting; none are claimed as runtime tests already run.
- API contracts and structured questions/answers connect Frontend and Backend.
  Record version, sender/recipient, task, impact, acknowledgement and next action.
  Contract/scope changes go to the lead; QA tests the actual combined feature.
- STATE-001 pins domain results as authority, separate opaque graph checkpoints and
  immutable objects. Reconcile unknown effects; recheck gates after input changes.
  Retention is operator-controlled; complete restore still needs integration tests.
  Validate fixtures: python3 scripts/validate_state_design.py (no dependencies).
- LIM-001: 40 model requests/mission, 2 repairs/task and 6/mission, 3,600 active
  seconds and 86,400 lifetime seconds. Reservations/unknown effects survive restart.
  Validate: python scripts/validate_execution_limits.py (same jsonschema environment).
- SBX-001: no egress/host mounts/credentials; six fixed checks, owned path grants,
  reviewed seccomp derivative for browser profiles only. Null releases block execution.
  Validate: python scripts/validate_sandbox_profiles.py (same jsonschema environment).
- Next: stage-eight GitHub identity/integration (T-017), then separately authorized scaffold.
  Do not start runtime implementation without authorization or claim Docker/CI
  or application dependencies already work.
- Design delivery has no local blocker; Docker/image/host qualification is absent.
  Maintainer review and effective sandbox checks remain pending before runtime.

## Maintenance and trust

Summaries are derived context, not proof or new permission. Code and test artifacts
take precedence over stale summaries; explicit human instructions take precedence
over saved plans. Mark superseded decisions rather than silently rewriting history.
Never publish credentials, private source, full conversations, or private run logs here.
Keep this file below approximately 120 lines as a maintenance target; archive detail
into linked documents. Token savings are an intended benefit, not a measured result.

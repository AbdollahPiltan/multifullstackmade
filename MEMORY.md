# Project memory / حافظهٔ ادامهٔ کار

Updated: 2026-10-29. This is a compact, human-maintained project summary, not a
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
  covers stage-two architecture documentation and GitHub PR delivery; not runtime code.
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
| Current architecture documentation | ARCH-001 technology and execution selections | Exact final commit and checks belong in its PR / report |

## Current continuation

- Branch: `docs/mvp-architecture`, based on open PR #5 (`docs/mvp-scope`).
- Deliver the architecture PR against that dependency. Verify ancestry before retargeting
  dependent PRs to main; do not auto-merge or rewrite shared history.
- T-010/T-011 track stage-two stack selection, awaiting review; T-009 is the
  preceding scope delivery. T-036/T-037 are prior documentation deliveries.
- MVP-001 selects a local single-user CLI orchestrator, sequential roles, inspectable
  graph, durable continuation and one reviewable PR. The notes browser/API fixture
  exercises create/list/edit/delete, validation, persistence and safe text rendering.
- AC-01–AC-13 define future checks, including restart, stale evidence, repair,
  reconciliation and usage accounting; none are claimed as runtime tests already run.
- API contracts and structured questions/answers connect Frontend and Backend.
  Record version, sender/recipient, task, impact, acknowledgement and next action.
  Contract/scope changes go to the lead; QA tests the actual combined feature.
- Next: detailed role/tool contracts (T-012), then API/message contracts (T-013).
  T-014–T-017 retain storage/profile/limit/integration detail. Do not start runtime
  implementation without authorization or claim Docker/CI/dependencies already work.
- No known local technical blocker. Maintainer review and MVP decisions remain pending.

## Maintenance and trust

Summaries are derived context, not proof or new permission. Code and test artifacts
take precedence over stale summaries; explicit human instructions take precedence
over saved plans. Mark superseded decisions rather than silently rewriting history.
Never publish credentials, private source, full conversations, or private run logs here.
Keep this file below approximately 120 lines as a maintenance target; archive detail
into linked documents. Token savings are an intended benefit, not a measured result.

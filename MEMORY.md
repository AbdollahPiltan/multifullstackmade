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
  covers documenting graph/memory, the approved developer-role split, and GitHub PR delivery.
- Python, LangGraph, SQLite, provider selection, UI, and numerical budgets remain
  open choices. DEV-001 approves five distinct roles: lead/architect, Frontend,
  Backend, QA/API Tester and Security. Activate only needed roles; execute
  sequentially in the MVP. No role runtime has been implemented.
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
| Release goals | [docs/ROADMAP.md](docs/ROADMAP.md) |

## Last recorded checkpoints and checks

| Checkpoint | Recorded outcome | Limit |
| --- | --- | --- |
| `a291371` on main | Initial public project documentation | Design only |
| `5eb38fd` in PR #1 | Root policy and brief; 75 original engineering rules and MIT notice preserved | PR #1 verified merged on 2026-10-29 |
| `0a77334` in PR #1 | TASKS.md, 35 unique task IDs; 13 files, 46 local links, whitespace and final-newline checks passed | Documentation checks, not application tests |
| `70c3724` in PR #2 | Graph/memory design; 15 files, 68 local links, 36 task IDs, 18 transitions, policy preservation and whitespace checks passed | Documentation only; PR #2 still open when checked |
| Current developer-role split | DEV-001 in docs/DESIGN.md; structured coordination and integration gates | Exact commit and final checks belong in the delivery PR / report |

## Current continuation

- Branch: `docs/split-developer-roles`, based on the open PR #2 branch.
- Deliver against `docs/graph-memory` first. PR #1 is merged; PR #2 still targets
  its old dependency branch when last checked. Verify ancestry and retarget dependent
  PRs to main when appropriate; do not merge or rewrite shared history automatically.
- T-037 tracks the approved role split. T-036 tracks graph/memory documentation.
  Both are documentation deliveries, not implemented runtime capabilities.
- API contracts and structured questions/answers connect Frontend and Backend.
  Record version, sender/recipient, task, impact, acknowledgement and next action.
  Contract/scope changes go to the lead; QA tests the actual combined feature.
- Next product discussion: agree on a first module, interface and measurable MVP
  acceptance criteria (T-009–T-013). Do not start implementation without authorization.
- No known local technical blocker. Maintainer review and MVP decisions remain pending.

## Maintenance and trust

Summaries are derived context, not proof or new permission. Code and test artifacts
take precedence over stale summaries; explicit human instructions take precedence
over saved plans. Mark superseded decisions rather than silently rewriting history.
Never publish credentials, private source, full conversations, or private run logs here.
Keep this file below approximately 120 lines as a maintenance target; archive detail
into linked documents. Token savings are an intended benefit, not a measured result.

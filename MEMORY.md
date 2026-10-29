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
  covers documenting graph/memory, persisting these instructions, and GitHub PR delivery.
- Python, LangGraph, SQLite, provider selection, UI, and numerical budgets remain
  open choices. Four initial roles are proposed, not implemented.
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
| `5eb38fd` in PR #1 | Root policy and brief; 75 original engineering rules and MIT notice preserved | Not merged when last checked on 2026-10-29 |
| `0a77334` in PR #1 | TASKS.md, 35 unique task IDs; 13 files, 46 local links, whitespace and final-newline checks passed | Documentation checks, not application tests |
| Current graph/memory documentation | Scope: MEMORY.md, graph/memory design, entry-point links and task ledger | Exact final commit and verification outcome are recorded in its PR / delivery report to avoid self-referential commits |

## Current continuation

- Branch: `docs/graph-memory`, based on the open PR #1 documentation branch.
- The graph/memory PR must first target that dependency branch. After PR #1 is
  integrated, verify ancestry and retarget to main if necessary; do not merge or
  change shared history automatically.
- T-036 tracks this documentation delivery. T-014 remains open for detailed runtime
  design and implementation choices; writing the design does not complete runtime work.
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

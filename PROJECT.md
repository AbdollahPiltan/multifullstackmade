# Project Brief and Progress

Engineering policy: [AGENTS.md](AGENTS.md). Product design: [docs/DESIGN.md](docs/DESIGN.md).
Task status and completion evidence: [TASKS.md](TASKS.md).
Continuation entry point: [MEMORY.md](MEMORY.md). Proposed graph and memory contract:
[docs/GRAPH-MEMORY.md](docs/GRAPH-MEMORY.md).
This brief adapts the upstream [project template](https://github.com/AbdollahPiltan/strict-development-rules/blob/0754e297cb8898700b1196f9ecd40884f6c9f86c/templates/PROJECT.md).
Consult the pinned [startup and recovery guide](https://github.com/AbdollahPiltan/strict-development-rules/blob/0754e297cb8898700b1196f9ecd40884f6c9f86c/PROJECT-START.md)
when setup or recovery needs attention; routine tasks should use this brief.

## Product

| Field | Value |
| --- | --- |
| Project name | multifullstackmade |
| Intended outcome and users | An open-source AI development team that turns agreed module requirements into reviewable software with traceable work and validation evidence. Public contributors and future users can inspect and reuse the project. |
| Confirmed direction | The human communicates primarily with the Tech Lead. An execution graph, durable progress, project memory, task ownership, and versioned handoffs are central requirements. Start with an MVP and evolve through later versions. |
| Minimum useful scope | Proposed: one user, one project, one bounded mission, four roles, durable checkpoints, independent QA / API tests and security review, then lead acceptance and human-controlled merge / deployment. |
| Explicit exclusions | No runtime implementation in the policy-adoption task. No multi-user hosted platform, automatic deployment, or speculative infrastructure. No final language, model provider, or UI decision yet. |
| Product specifications and acceptance criteria | [Design](docs/DESIGN.md) and [v0.1 roadmap](docs/ROADMAP.md) are discussion drafts. The first example module and final acceptance criteria still need agreement. |
| Current assigned task | Document the graph/memory design, add compact continuation memory and repository-wide continuation instructions, verify and publish through a dependent feature-branch PR. |
| Next milestone | Discuss and finalize the v0.1 example module, interface, role contracts, and measurable acceptance criteria. Application implementation requires a separate user instruction. |

## Setup and authorization

| Field | Value |
| --- | --- |
| Languages, frameworks, and supported versions | Not selected. Python / LangGraph / SQLite are initial candidates, not dependencies or approved requirements. |
| Architecture and data-model references | [docs/DESIGN.md](docs/DESIGN.md); there is no implemented data model. |
| GitHub owner/repository | [AbdollahPiltan/multifullstackmade](https://github.com/AbdollahPiltan/multifullstackmade) |
| Repository visibility | Public, explicitly requested by the owner. |
| Remote name and URL | `origin`: `https://github.com/AbdollahPiltan/multifullstackmade.git` |
| Default branch | `main`, verified from GitHub and local tracking metadata. |
| Current documentation feature branch | `docs/graph-memory`, based on the still-open PR #1 branch `chore/adopt-strict-development-rules`. Target that dependency first; retarget after its integration if needed. |
| Commit identity | `AbdollahPiltan`; use the account's public noreply address for published commits. No credentials belong here. |
| Authorized actions | The owner requested public repository creation, project-wide adoption of the linked rules, a file listing completed and remaining tasks, and graph/memory documentation with persistent continuation instructions. These documentation changes, feature-branch publication, and a reviewable PR are in scope. This does not authorize unrelated repository settings, cloud resources, application implementation, merging the adoption PR, or deployment. |
| PR, review, and merge requirements | AUT-07 prohibits direct default-branch pushes and force-pushes. Use reviewed PRs. Future agent output additionally follows the proposed revision-bound QA, security, and lead gates. |
| Technical enforcement | At adoption, GitHub reports `main` as unprotected with no required status-check contexts; no CI workflow exists. The written policy is a development requirement, not a claim that protections or agent gates are already configured. |

Local checkout paths are environment-specific and intentionally omitted from the public brief.
Verify the working directory and `git remote -v` before changing Git metadata.

## Verification and operation

| Field | Value |
| --- | --- |
| Installation and local run instructions | Not applicable yet: the repository contains documentation only. |
| Required documentation checks | `git diff --check`; verify relative Markdown links exist and remain inside the repository; compare engineering rules and license notice with the pinned upstream file; review the final diff and intended file list for scope and sensitive data. |
| Runtime test, lint, type, and CI commands | Not applicable yet. Define reproducible commands and appropriate automation with the first executable contribution. Do not invent passing runtime results. |
| Security and sensitive data | Publish sanitized source and examples only. Never commit credentials, private execution state, private repository data, or sensitive transcripts. Future runtime permissions and sandbox boundaries are unresolved. |
| Workload and performance budgets | Not established. Select representative workloads and agree on budgets before implementation makes performance claims. |
| Deployment target and authorization | No deployed application or deployment authorization. A local prototype is proposed. |
| Recovery constraints | Documentation can be reverted through a PR. Git history does not recover external GitHub effects, execution databases, secrets, or deployments. Define runtime backup / recovery procedures when relevant. |

## Milestones and checkpoints

Keep the authoritative task and milestone status, evidence, and checkpoint references
in [TASKS.md](TASKS.md). Release goals and acceptance criteria remain in
[docs/ROADMAP.md](docs/ROADMAP.md); avoid maintaining a second status table here.

Record this task's final commit hash and PR in the PR description / final report, or
in a later normal project update. Do not create a self-referential commit-hash loop.

## Decisions, exceptions, and blockers

| Item | Decision / evidence | Impact or next action |
| --- | --- | --- |
| Policy source | Upstream commit `0754e297cb8898700b1196f9ecd40884f6c9f86c`, AGENTS.md blob `0a503ff22f8d7d8a52397107f8d39d5f4e53642b` | Keep the upstream MIT notice. Review future updates explicitly through a PR. |
| Local policy changes | Adoption metadata, project-specific scope, and populated Project decisions table | Preserve all engineering rule IDs and normative requirements; maintain product details here. |
| AUT-03 / prior discussion | The owner asked to finish discussion before building application code | Adopt documentation now; do not treat the generic startup prompt or roadmap as permission to implement every milestone. |
| VER-01 / VER-03 applicability | No application, dependencies, CI pipeline, or deployment exists | Run documentation and provenance checks; runtime, API, data, load, and UI checks become applicable with the relevant code. This is applicability scoping, not a waiver of future controls. |
| Runtime agent policy | No agent controller exists yet | Before enabling future project agents, load the applicable policy into their task context and enforce relevant gates in the controller / CI. A Markdown file alone does not enforce runtime behavior. |
| Git authentication | The assistant integration can access GitHub; public Git fetch worked at bootstrap | Verify local push authentication separately. Never paste tokens into chat, command arguments, remotes, or project files. |

## Recovery notes

- Baseline before policy adoption: `a2913714213ee2a2248e0fa346a25f70059382b3` on `main`.
- Policy-adoption changes depend on the existing documentation and add no runtime,
  application data, cloud resources, or deployment effects.
- Recover published changes through a revert commit on a feature branch and a PR.
  Inspect merge parents before reverting a merge; do not reset shared history or force-push.
- Verify recovery with the applicable documentation checks and ensure project
  guidance remains consistent. Unmerged feature-branch work does not change `main`.
- Preserve checkpoint references when selecting a PR merge strategy; a squash or
  rebase can change which commit IDs appear on the default branch.

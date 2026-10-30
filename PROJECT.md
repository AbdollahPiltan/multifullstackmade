# Project Brief and Progress

Engineering policy: [AGENTS.md](AGENTS.md). Product design: [docs/DESIGN.md](docs/DESIGN.md).
Task status and completion evidence: [TASKS.md](TASKS.md).
Stage-one scope baseline and acceptance matrix: [docs/MVP-SCOPE.md](docs/MVP-SCOPE.md).
Stage-two selected stack and boundaries: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).
Stage-three role/tool authority: [docs/AGENT-CONTRACTS.md](docs/AGENT-CONTRACTS.md).
Stage-four wire/API contracts and validation: [docs/PROTOCOL-CONTRACTS.md](docs/PROTOCOL-CONTRACTS.md).
Stage-five durable state, recovery and retention: [docs/STATE-PERSISTENCE.md](docs/STATE-PERSISTENCE.md).
Stage-six execution ceilings and repair/cancellation policy: [docs/EXECUTION-LIMITS.md](docs/EXECUTION-LIMITS.md).
Stage-seven sandbox and tool-access design: [docs/SANDBOX-PROFILES.md](docs/SANDBOX-PROFILES.md).
Stage-eight GitHub identities, publication and reconciliation: [docs/GITHUB-DELIVERY.md](docs/GITHUB-DELIVERY.md).
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
| Confirmed direction | DEV-001 approves separate Frontend and Backend from the MVP, selective role activation, sequential initial execution, versioned API contracts and structured coordination. The human communicates primarily with the Tech Lead. An execution graph, durable progress, project memory, task ownership, and versioned handoffs are central requirements. Start with an MVP and evolve through later versions. |
| Minimum useful scope | Stage-one baseline MVP-001: local single-user operator interface, one bounded mission, five sequential selectively activated roles, inspectable graph, durable context, actual QA/security evidence and one delivery PR. Personal notes is the first fixture; see docs/MVP-SCOPE.md. |
| Explicit exclusions | No runtime implementation in this scope task. No multi-user hosted platform, automatic deployment, parallel execution, advanced orchestration dashboard, arbitrary legacy repositories or speculative infrastructure. Stack/provider are selected in ARCH-001; a minimal local CLI operator interface and a browser UI for the notes fixture are scoped. |
| Product specifications and acceptance criteria | [MVP-001 scope](docs/MVP-SCOPE.md) defines the first fixture, delivery boundary and AC-01–AC-13. Review is pending; this defines acceptance, not passing test results. Design and roadmap remain supporting documents. |
| Current assigned task | Complete stage eight: specify publication identity/authority, draft CI/readiness, private intents and external reconciliation; validate design fixtures and deliver a dependent PR. No product adapter or runtime is implemented. |
| Next milestone | Design stages one through eight are documented. Next is T-018: build the minimal executable scaffold when the owner requests implementation; later T-023/T-024 must prove SB/GH runtime qualification. No automatic implementation starts with this design delivery. |

## Setup and authorization

| Field | Value |
| --- | --- |
| Languages, frameworks, and supported versions | ARCH-001 baseline: CPython 3.12; uv; argparse CLI; LangGraph + SQLite checkpoint adapter; Pydantic v2; sqlite3; official OpenAI Python SDK / Responses API; Docker; Git + gh. Notes fixture: FastAPI/Uvicorn and plain browser HTML/CSS/JavaScript; pytest/HTTPX/Playwright Chromium. Exact compatible package versions and images will be locked and tested at scaffold, not in this documentation change. |
| Architecture and data-model references | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/DESIGN.md](docs/DESIGN.md) and graph/memory contract; STATE-001 reference domain schema; no installed database or runtime data model. |
| GitHub owner/repository | [AbdollahPiltan/multifullstackmade](https://github.com/AbdollahPiltan/multifullstackmade) |
| Repository visibility | Public, explicitly requested by the owner. |
| Remote name and URL | `origin`: `https://github.com/AbdollahPiltan/multifullstackmade.git` |
| Default branch | `main`, verified from GitHub and local tracking metadata. |
| Current documentation feature branch | `codex/github-delivery`, based on the open PR #11 branch `codex/sandbox-profiles`. Deliver against that dependency; verify ancestry before later retargeting. |
| Commit identity | `AbdollahPiltan`; use the account's public noreply address for published commits. No credentials belong here. |
| Authorized actions | The owner requested public repository creation, project-wide adoption of the linked rules, a file listing completed and remaining tasks, graph/memory documentation with persistent continuation instructions, the Frontend / Backend role split with structured cooperation, completion of stage-one product scope, stage-two technology/architecture selection, completion of stage-three role/tool contracts, stage-four API/message/tool schemas with validation tooling, stage-five graph/storage/recovery design with static validation fixtures, stage-six execution-limit/retry/repair/cancellation policy with validated numeric profiles, stage-seven sandbox/tool-access design with static policy fixtures, and stage-eight GitHub identity/publication/reconciliation design with private-intent/static examples. These documentation changes, feature-branch publication, and a reviewable PR are in scope. This does not authorize unrelated repository settings, cloud resources, application implementation, merging the adoption PR, or deployment. |
| PR, review, and merge requirements | AUT-07 prohibits direct default-branch pushes and force-pushes. Use reviewed PRs. Future agent output additionally follows the proposed revision-bound QA, security, and lead gates. |
| Technical enforcement | At adoption, GitHub reports `main` as unprotected with no required status-check contexts; no CI workflow exists. The written policy is a development requirement, not a claim that protections or agent gates are already configured. |

Local checkout paths are environment-specific and intentionally omitted from the public brief.
Verify the working directory and `git remote -v` before changing Git metadata.

## Verification and operation

| Field | Value |
| --- | --- |
| Installation and local run instructions | No application run command yet: design documents, reference schemas and validation tooling only. |
| Required documentation checks | `git diff --check`; verify relative Markdown links exist and remain inside the repository; compare engineering rules and license notice with the pinned upstream file; review the final diff and intended file list for scope and sensitive data. |
| Runtime test, lint, type, and CI commands | Not applicable yet. Contract validation tooling: python scripts/validate_contracts.py with disposable jsonschema 4.25.1 and openapi-spec-validator 0.7.2. State design: python3 scripts/validate_state_design.py (standard library, synthetic in-memory SQLite). Limits/sandbox/GitHub design: python scripts/validate_execution_limits.py, python scripts/validate_sandbox_profiles.py and python scripts/validate_github_delivery.py in the same disposable jsonschema environment. Runtime setup/CI commands are still future work; do not invent passing runtime results. |
| Security and sensitive data | Publish sanitized source and examples only. Never commit credentials, private execution state, private repository data, or sensitive transcripts. ARCH-001 defines the Docker boundary and ROLE-001 defines role/tool authority. SBX-001 specifies access/profile rules and qualification gates; actual filesystem, Docker and browser enforcement remains implementation work. |
| Workload and performance budgets | LIM-001 selects initial admission ceilings for the notes fixture; no latency/throughput/currency guarantees or measured optimization. Enforce and measure at implementation before performance claims. |
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
| GH-001 (2026-10-30) | docs/GITHUB-DELIVERY.md; one operator publication principal, five controller-only effects, draft -> native CI -> ready -> human acceptance, bounded intent reconciliation | 57 synthetic cases passed; actual auth/remote fault/CI integration not implemented. No review/merge/deploy/settings capability added. |
| ARCH-001 publication refinement | Local checks and independent QA/Security/Lead precede draft publication; PR-triggered CI precedes ready/final delivery | Resolves circular CI ordering; workflow and issuer manifest must be configured before a product mission. Controller does not rewrite PR bodies or push workflow changes mid-mission. |
| SBX-001 (2026-10-30) | docs/SANDBOX-PROFILES.md and frozen six-profile policy; UID/mount/network/path/secret boundaries, browser seccomp and image-release gates | 55 synthetic cases passed; Docker CLI unavailable here, so no effective sandbox test or image release. T-018/T-023 must implement and qualify before execution. |
| ARCH-001 refinement | Browser profiles require a reviewed seccomp derivative for unprivileged user namespaces; all others retain engine default | Minimal compatibility refinement, not a strict-rule waiver; preserve other syscall denials, pin derivative and prove SB-08. No root/host IPC/SYS_ADMIN/--no-sandbox fallback. |
| LIM-001 (2026-10-30) | docs/EXECUTION-LIMITS.md and closed notes_local_v1 numeric profile; persistent reservations, bounded retries/repair, time/cancellation, storage and resource admission | 50 synthetic design examples validated; actual enforcement, metering and host/profile checks remain future work. |
| STATE-001 (2026-10-30) | docs/STATE-PERSISTENCE.md, 13-stage/18-edge graph and reference v1 domain schema; restart, context, retention and backup design | Static fixtures validated; actual LangGraph crash/restart, filesystem durability, process locks and complete restore remain implementation checks. |
| PROTO-001 (2026-10-29) | docs/PROTOCOL-CONTRACTS.md, OpenAPI 3.1 and JSON Schema 2020-12 define five API operations, 11 tool contracts and closed records | Shape validation works; semantic authority, real API behavior and replay remain future implementation requirements. |
| ROLE-001 (2026-10-29) | Five role contracts and controller-mediated capability matrix in docs/AGENT-CONTRACTS.md, including private/test/shared-file boundaries and rejection rules | Documentation review pending; serialized contracts now in PROTO-001; runtime enforcement is not implemented. |
| ARCH-001 (2026-10-29) | Selected stage-two architecture in docs/ARCHITECTURE.md, including stack, modular boundaries, provider and execution environment | Review pending; lockfile, compatible package versions and runtime verification remain future work; STATE-001 specifies storage/migration design and LIM-001 selects numeric ceilings. |
| MVP-001 (2026-10-29) | Stage-one default baseline authored under the owner's completion request: local CLI team orchestrator with a personal-notes acceptance fixture, exact outcomes in docs/MVP-SCOPE.md | Scope PR review pending; stage-two stack selection is now in ARCH-001. Numeric ceilings are now selected by LIM-001; runtime implementation remains separate. |
| DEV-001 (2026-10-29) | Owner approved replacing the combined developer proposal with separate Frontend and Backend; see docs/DESIGN.md | Five role contracts are specified in ROLE-001 (T-012); implement T-022 later. This supersedes the previous combined-role proposal without authorizing runtime code. |
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

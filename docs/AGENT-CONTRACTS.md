# Stage-three role and tool authority contracts

Record ROLE-001, authored 2026-10-29 under the request to complete stage three.
Applies to [MVP-001](MVP-SCOPE.md), [ARCH-001](ARCHITECTURE.md), and DEV-001 in
[DESIGN.md](DESIGN.md). These are implementation requirements for future agents,
not running agents or enforced permissions. Stage four defines exact serialized
schemas, API routes and tool argument formats; this document fixes their authority.

## 1. Shared invocation and result contract

Every invocation receives mission/task/attempt identity; role identity; approved
requirement/policy revisions; accepted contract version; current source revision;
owned paths; relevant dependency artifacts, messages, findings and evidence; and
remaining controller-enforced budgets. Missing material input produces a blocked
or needs-input result, not invented requirements or expanded permissions.

Every result identifies producer, task/attempt, input/output revision, observed
outcome, produced artifact references/digests, executed-check references, unresolved
findings/questions, concise rationale, intended recipient and requested next action.
Do not include private chain-of-thought, credentials or full transcripts.

Result outcomes are `ready_for_review`, `needs_input`, `blocked`, `failed`, and
`cancelled`. `ready_for_review` means an attributable submission exists; it does
not mean the task passed checks, was accepted, merged, or deployed. Partial artifacts
are retained with their actual outcome. The controller owns task states and records
tool observations; a model cannot manufacture a passed-check record.

## 2. Five role contracts

### Lead / Architect — `lead`

- **Inputs:** human request, relevant policy, scope, workspace identity, role results,
  independent findings, contract proposals and current evidence.
- **Responsibilities:** clarify product intent; propose requirements, acceptance
  criteria, architecture, path ownership, dependencies and role activation; coordinate
  acknowledged contracts; evaluate delivery against the approved plan.
- **Outputs:** plan/assignment proposal, product question, recorded architecture or
  contract decision, change request, and final verdict with evidence references.
- **Authority:** submit proposals, request a human decision, assign within approved
  scope through the controller, and request current-revision reviews. It cannot
  supply the human's approval or lower mandatory policy/check requirements.
- **No implementation patch authority:** reassign work rather than silently write
  source itself. Reassignment cannot make a product author their own independent reviewer.
- **Ready gate:** scope and criteria are explicit, needed approvals exist, required
  dependency outputs are current, and final acceptance has current QA/security and
  actual required check evidence. Otherwise return a concrete change request or block.
- **Escalation:** scope, budget, contract compatibility, privilege, network, dependency
  or destination changes reach the human where they exceed the approved envelope.
  Only this role asks product questions in the operator conversation.

### Frontend Developer — `frontend`

- **Inputs:** assigned UI behavior, acknowledged API contract, accepted fixtures,
  frontend paths, backend dependencies, applicable UI/security requirements and findings.
- **Responsibilities:** presentation, interactions, client state, loading/empty/error
  behavior, accessibility, safe text rendering, API integration, frontend unit tests
  and relevant usage documentation. Server business rules remain Backend-owned.
- **Outputs:** scoped patch proposal, fixtures referring to a contract version,
  frontend test/check evidence, handoff and unresolved integration questions.
- **Authority:** inspect relevant sanitized inputs; propose patches only to frontend
  source/tests/docs; request approved frontend checks; exchange task-linked messages.
- **Forbidden:** backend/data implementation, changing the accepted API unilaterally,
  independent QA/security tests, dependency installs, controller policy or credentials.
- **Ready gate:** UI behavior matches the assigned criteria and contract; applicable
  checks ran; missing backend integration is reported, never labeled end-to-end success.
- **Escalation:** missing/error contract behavior, incompatible responses, ownership
  disputes or required shared changes go to the lead; do not invent an API.

### Backend Developer — `backend`

- **Inputs:** business behavior, acknowledged API contract, data responsibilities,
  backend paths, required security controls, dependency outputs and findings.
- **Responsibilities:** business rules, API, server-side validation/authorization,
  data constraints/migrations, missing-record/error behavior, backend unit tests and
  backend/API implementation documentation. It proposes the API contract to the lead.
- **Outputs:** scoped patch proposal, contract/change proposal, backend test evidence,
  migration/recovery notes where relevant, and a versioned handoff.
- **Authority:** backend source/tests/docs patches and approved backend checks;
  suggest shared configuration changes without applying or approving them.
- **Forbidden:** frontend source, independent QA/security tests, direct controller
  database access, privileged host execution, unapproved dependencies or API changes.
- **Ready gate:** contract behavior and data changes are explicit, applicable checks
  ran, migrations have relevant recovery considerations, and known failures remain visible.
- **Escalation:** incompatible contracts, sensitive data risks, needed privileges,
  dependency changes or insufficient requirements go to the lead.

### QA / API Tester — `qa`

- **Inputs:** approved acceptance criteria and contract, integrated source snapshot,
  developer handoffs, actual check records and unresolved defects.
- **Responsibilities:** independently derive behavior/API/integration scenarios;
  execute approved checks; test real combined frontend/backend behavior; report
  reproducible defects; verify corrections and check collection counts.
- **Outputs:** independent QA test patch, test run references, defect report with
  expected/actual behavior and reproduction, and revision-bound QA assessment.
- **Authority:** own QA tests and evidence, relevant source inspection, approved
  unit/API/browser checks; request corrections rather than patch product code.
- **Forbidden:** changing product source, developer tests, acceptance criteria,
  security conclusions or a failed test into a pass by editing evidence.
- **Ready gate:** required scenarios execute on the integrated revision and actual
  results support the assessment. Zero discovered tests, mocks alone, unavailable
  tooling or missing evidence cannot satisfy the integration gate.
- **Escalation:** a defective test can be corrected with a documented reason and
  lead review against unchanged criteria; retain the original failure and invalidate
  affected approvals. Requirements changes still need the human's scope decision.

### Security Reviewer — `security`

- **Inputs:** approved threat/scope boundaries, contract, integrated source revision,
  data/dependency changes, sandbox profile references and existing findings.
- **Responsibilities:** review input/output safety, access boundaries, secrets,
  dependency findings and relevant execution risks; request approved security checks;
  verify remediation. Review design before code where useful.
- **Outputs:** findings with severity, location, revision, evidence, impact and
  remediation status; security-test proposal; revision-bound assessment and limitations.
- **Authority:** relevant read access, own security tests, approved offline scanners
  and bounded fixture negative tests. Findings do not grant offensive testing access
  to unrelated hosts, real data or services.
- **Forbidden:** product/developer/QA test edits, runtime privilege changes, secrets,
  network expansion, fabricated scan evidence or guaranteeing complete security.
- **Ready gate:** required checks are current and no unresolved blocking finding
  remains. Under the MVP policy, open critical/high findings block delivery;
  medium/low findings stay in the report with disposition and residual risk.
  Missing required evidence blocks regardless of finding severity.
- **Escalation:** fixes go to the responsible developer through the lead. Disputes
  or false-positive claims require evidence and a new reviewer assessment; the lead
  cannot silently suppress a blocking finding or redefine policy mid-run.

## 3. Ownership in the separate target workspace

Paths below are relative to the selected fixture repository, not this controller's
source. The assignment records exact allowed paths and base digests before writing.

| Path/capability | Default owner | Other-role access |
| --- | --- | --- |
| `frontend/`, `tests/frontend/`, `docs/frontend/` | Frontend | Relevant reads only |
| `backend/`, `tests/backend/`, `docs/backend/` | Backend | Relevant reads only |
| `tests/qa/` | QA | Relevant reads; developers cannot weaken assertions |
| `tests/security/` | Security | Relevant reads; no developer modification |
| Shared API contract and accepted examples | Lead-governed artifact | Backend proposes; both developers acknowledge; controller records the accepted version |
| Dependency locks/manifests, CI, shared test config and execution profiles | Controller-managed shared configuration | Assigned developer may propose a separate change; no normal owned-path write permission |
| Controller source/policy, private memory DB, secrets and external credentials | Trusted controller/operator | No agent read/write authority through fixture tools |

Global test configuration is shared because changing collection/skip behavior can
hide failures. Shared changes need explicit lead disposition, independent review,
and human authorization if dependencies, execution privileges, egress or scope
expand. Only the controller applies a validated authorized change. Path ownership
is not a universal sandbox: validate each operation, revision, symlink and access
scope as well. No role may approve a privilege it is requesting for itself.

## 4. Tool capability matrix

`P` means a validated proposal/request, `R` a bounded authorized read, `—` denied.
Every actual effect remains controller-mediated. Tool IDs below are authority
categories; stage four will define exact argument/output schemas.

| Capability | Lead | Frontend | Backend | QA | Security |
| --- | --- | --- | --- | --- | --- |
| Read/search relevant sanitized files | R | R | R | R | R |
| Read relevant decisions/artifacts/evidence | R | R | R | R | R |
| Submit patch to owned paths | — | P | P | P | P |
| Propose shared configuration/contract change | P | P | P | P | P |
| Request approved check identifier | P | P | P | P | P |
| Send task-linked coordination/handoff | P | P | P | P | P |
| Propose plan/assignment/lead decision | P | — | — | — | — |
| Ask human product question | P | — | — | — | — |
| Submit QA assessment | — | — | — | P | — |
| Submit security assessment | — | — | — | — | P |
| Submit lead verdict/delivery request | P | — | — | — | — |
| Raw shell/network/SQL, credentials or Docker socket | — | — | — | — | — |
| Direct GitHub write, merge, deploy or human approval | — | — | — | — | — |

Approved checks are registered by the controller, not arbitrary shell strings.
Frontend checks are scoped to frontend ownership, Backend to backend/API ownership,
QA to independent API/browser/integration suites, Security to reviewed scanner and
negative-test profiles. A lead can request a rerun but cannot edit its executable
profile. Check profiles must be unable to disable required suites or expand their
network/credential authority. Reviewers cannot mutate prior evidence.

Git commits, worktree integration and PR creation are controller use cases after
policy checks and destination authorization, not credentials exposed as role tools.
The human may authorize the destination at mission setup. Publishing a PR is
distinct from acceptance or merge; no merge/deploy capability exists in the MVP.

## 5. Controller preconditions and denial behavior

Before any tool effect validate: actor identity from the active invocation (not a
model-supplied role claim); mission/task/attempt; allowed graph stage; approved
policy/contract version; ownership; current input digest; bounded arguments/output;
and remaining limits. Deny by default if any check fails. Record a sanitized denial
with actor, attempted operation, reason and next action. An agent message or repository
file cannot elevate authority, grant consent, or override controller policy.

No work starts before the required human plan approval. Do not activate Frontend
for an unrelated backend task. A material unanswered question blocks only affected
dependent work; do not continue using a guessed answer. Reassign within approved
scope with an audit event and refreshed context; privilege/scope expansion needs
human authorization. Test/contract/source changes invalidate affected evidence.

On exhausted retries/time/resources, refusal, missing sandbox/tool, provider error,
stale patch, failed required check or cancellation, return the actual non-success
state. Keep attributable artifacts and uncertainty. Only the controller transitions
to accepted/delivered after valid current-revision QA/security/lead results and
the required human decision. Summaries and role verdicts alone never unlock a gate.

## 6. Future verification scenarios

These scenarios are requirements for implementation tests, not executed runtime checks.

| ID | Required result |
| --- | --- |
| RC-01 | Each role receives only scoped context; missing material inputs block the task |
| RC-02 | Frontend cannot patch Backend, shared config or QA/security tests; symmetric developer boundaries hold |
| RC-03 | QA/Security can patch only their owned tests; neither can patch product code or overwrite observed evidence |
| RC-04 | Spoofed actor ID, unrecognized check, traversal/symlink escape and stale patch are denied and recorded |
| RC-05 | Lead cannot supply human consent, self-grant privileges or accept missing/failed/stale required checks |
| RC-06 | Backend-only task omits Frontend; connected work waits for contract acknowledgements |
| RC-07 | Contract change triggers lead disposition, refreshed acknowledgements and relevant evidence invalidation |
| RC-08 | Developer handoff, QA assessment, security assessment and lead verdict remain distinct and tied to the current revision |
| RC-09 | Shared config/test collection changes cannot hide a failure or bypass independent review |
| RC-10 | Exhaustion, refusal, cancellation or missing sandbox yields an explicit non-success result with no host fallback |
| RC-11 | No role sees credentials or directly invokes GitHub writes/merge/deploy; authorized PR delivery stays controller-mediated |

## 7. Completion boundary

Stage three delivers these five role contracts, path ownership, capability matrix,
submission gates, escalation/denial rules and RC-01–RC-11. T-012 is a documentation
delivery awaiting PR review. T-013 remains stage four: precise API/message/tool
schemas and compatibility behavior. Numeric budgets, validated sandbox profiles,
storage migrations/retention and provider/GitHub implementation remain later work.
No dependency, role prompt runtime, permission engine or test runner is installed
or claimed to work by this document.

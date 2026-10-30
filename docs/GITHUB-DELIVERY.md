# Stage-eight GitHub identity and delivery design

GH-001, 2026-10-30, completes design task T-017. Baselines: [MVP-001](MVP-SCOPE.md),
[ARCH-001](ARCHITECTURE.md), [ROLE-001](AGENT-CONTRACTS.md),
[PROTO-001](PROTOCOL-CONTRACTS.md), [STATE-001](STATE-PERSISTENCE.md),
[LIM-001](EXECUTION-LIMITS.md) and [SBX-001](SANDBOX-PROFILES.md).
This specifies the future controller; it does not install an adapter, CI workflow,
repository protection, GitHub App or credentials. Current documentation PRs use
ordinary verified documentation publication, not a claimed working agent pipeline.

The frozen policy is [github-delivery.json](../contracts/github-delivery.json).
Its [schema](../contracts/github-delivery.schema.json) also defines a private
PublicationIntent record. This is controller journal data, not a twelfth role tool
or an extension to PROTO-001. Shape validity cannot prove authorization or execution.

## 1. Identities and explicit authorization

| Identity | Meaning / authority |
| --- | --- |
| Human operator | Supplies actual scope/publication consent and decides acceptance; merge/deploy remain separate human actions |
| Internal role | lead/frontend/backend/qa/security from an authenticated invocation; no GitHub credential or direct remote-write capability |
| Controller publication principal | One explicitly selected existing gh account; API numeric user ID is pinned, login is display/routing metadata |
| Git author/committer | Approved public identity on commits; neither a commit email nor an Agent-Role trailer proves GitHub account identity or signature |
| Native reviewer/check issuer | Actual GitHub user/App/workflow identity observed through GitHub; never inferred from an internal role label |

Five internal roles do not create five independent GitHub reviewers. Record QA,
Security and Lead assessments with their exact revision and limitations as internal
evidence. Do not post fabricated approvals, impersonate reviewer accounts, forge
signatures or ask the author's credential to approve its own PR. Native reviews
follow [GitHub review semantics](https://docs.github.com/en/pull-requests/reference/pull-request-reviews);
required native approvals need actual eligible separate maintainers. Do not auto-request
reviewers or notify other accounts as a side effect of a role message.

Before a product mission can publish, capture an operator-authored private
authorization artifact: github.com host; numeric repository ID plus owner/name;
same-repository base/head scope; observed default/base refs and base SHA; expected
publication user ID; allowed actions; permitted public source/evidence scope;
policy/plan/contract digests and expiry. Bind its artifact digest to every intent.
The operator must approve disclosure to that repository even if local work was
already allowed. No auto-fork, repository creation, visibility change or host redirect.

Preflight reads effective API identity and repository capability using the exact
selected credential context. Verify numeric IDs and host; renamed repositories or
changed account routing require reconciliation, not blind redirect following.
Missing auth, changed principal, wrong repository or insufficient capability blocks
publication; never fall back to another logged-in account or edit repository settings.
The checked-in policy has `binding: null`: it contains no current mission consent.
The future trusted registry supplies an authenticated operator binding, not model JSON.
A missing required-check manifest also blocks remote product publication.

## 2. Credentials, commands and least privilege

Only the trusted host controller calls Git/gh with fixed argument arrays, explicit
host/repository/ref and bounded sanitized output. Model text supplies no shell,
command suffix, remote URL, credential helper, editor, pager or gh extension.
Rebuild the adapter environment; disable interactive prompts and HTTP debug logs.
Use either the selected approved gh credential store or an explicitly authorized
environment credential reference. Never print tokens, run token-display commands,
put a token in a remote/argument/body, or mount credential/SSH/Docker sockets into
SBX workers. Avoid inherited Git hooks, filters, config and credential programs.

Environment overrides matter: [gh documents](https://cli.github.com/manual/gh_help_environment)
that token environment variables override stored credentials. Clear unapproved
GH_TOKEN/GITHUB_TOKEN, host/repo/config/editor/pager/debug overrides and Git transport
configuration before selecting the approved context. Re-check API user ID and ensure
HTTPS Git uses the same selected gh credential source; author metadata is not proof.
The MVP supports one github.com same-repository HTTPS destination, not arbitrary
Enterprise hosts, SSH identities, forks or token/account switching.

Publication uses an approved operator User credential, not an Actions GITHUB_TOKEN
or a bot/App principal in this MVP. Token provenance must be checked, not inferred
from an environment variable's name. Actions-generated events have different
workflow-trigger semantics; the required draft workflow must be proven with the
selected publication credential before mission execution.

Logical capabilities are repository metadata/content/PR read, contents write for
the fenced branch and PR write for the allowed lifecycle; checks/Actions observation
is read-only. Exact token feasibility/scopes must be tested at implementation.
Existing OAuth credentials may be broader; the controller must still deny unlisted
operations. Do not silently create/refresh a broader token. No admin/settings,
workflow modification, check/status fabrication, review-write or merge capability
is exposed by the controller. CI uses no model/publication secret and an explicit
read-only token; see [GitHub token guidance](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication).

## 3. Allowed effects and branch ownership

The controller may perform only these actions under the operator binding:

| Action | Additional gate |
| --- | --- |
| create_branch | New `codex/mission-<mission_id>` in the approved repository; journal intent before effect; existing unknown branch is a conflict |
| push_fast_forward | Only the owned mission ref, expected old head, approved candidate snapshot and ordinary non-force push |
| create_draft_pr | Local required checks + QA/Security + Lead pass; sanitized disclosure authorized; exact head/base observed |
| convert_to_draft | Existing owned open PR; required before pushing a repair of a previously ready delivery |
| mark_ready | Existing owned draft; current local and configured native checks pass on the pinned head/base/environment |

All other writes are denied, including direct default/base-branch pushes, force
push (including force-with-lease), branch deletion, automatic merge, auto-merge,
deploy, retarget/reopen/close, settings/protection changes, review/status creation,
comments and automatic reviewer requests. Unlisted workflow reruns are also denied.
CLI [ready/draft operations](https://cli.github.com/manual/gh_pr_ready) may implement
the two state changes through a fixed trusted adapter, not a role-supplied command.

Use the project writer lock and domain state-version checks. A preflight ref read
is not a remote compare-and-swap: a normal push prevents non-fast-forward overwrite,
but cannot lock out other maintainers. Verify remote refs after every effect;
unexpected advancement blocks and preserves both histories. Never force, reset
shared history or silently adopt an unknown existing branch. Record expected old
and desired new SHA with a canonical intent digest and scoped operation key.
Validate refs with the trusted Git ref-format check and the bound mission identity;
reject option-like, control/whitespace or non-head ref forms. Never construct a
remote URL or API route from model text.

Commit author/committer is the approved public controller/operator identity. Role
attribution comes from task/attempt/result evidence and optionally truthful textual
trailers, not invented specialist email accounts. No claim of verified signatures
unless GitHub actually verifies the configured signing identity.

## 4. Local gates, draft CI and human delivery

This refines ARCH-001's publication ordering to avoid a CI circular dependency:
local checks and independent reviews precede **draft publication**; PR-triggered CI
then precedes readiness/final human acceptance. A draft is visible software, so it
still requires explicit publication consent and sanitization.

1. Integrate attributed changes in the private candidate workspace. Pin source,
   base/head, requirement, policy, contract, image/profile and test digests.
2. Execute required local checks, independent QA/Security and Lead review. Missing,
   failing, stale, cancelled, unavailable or zero-test evidence blocks publication.
3. Journal/push the approved mission branch and reconcile its exact remote SHA.
   Create one draft PR against the approved base; persist its repository/number/node
   identity and observed response before advancing the graph.
4. Observe the configured unprivileged pull_request checks on the draft. The trusted
   workflow must run on opened/synchronize and applicable lifecycle events without
   skipping drafts or required jobs; [workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request)
   are part of its reviewed configuration. No pull_request_target execution of
   untrusted code with privileged secrets.
5. After native CI, collect the final Lead verdict with the complete current
   evidence, re-read remote refs and mark ready only if every gate still passes.
   Present the exact PR/head/base and delivery report through the lead.
6. Capture actual human acceptance of that bundle, recheck its pinned inputs and
   observed PR, then record delivered. A native ready flag is not acceptance or
   permission to merge. No merge/deploy command exists in the MVP.

The prepublication Lead review authorizes only the draft under local gates;
it is not the final submit_delivery verdict and cannot claim CI already passed.
No repeated developer/QA work is needed merely because native evidence was added
without changing any inputs, but the final Lead verdict must reference that evidence.

Required native checks are a nonempty operator-reviewed manifest: expected check
name, trusted issuer/App ID, workflow identity/config digest and tested head/base/tree.
The policy's `required_checks: null` means not configured, **not no checks needed**.
At scaffold/CI integration choose actual commands/identities and prove draft triggers;
no made-up passing check or workflow is defined by this documentation change.
Workflow configuration is a reviewed pre-mission prerequisite. Role proposals to
change CI follow shared-configuration review and separate operator application;
the publication controller does not push workflow/configuration changes mid-mission.
Observe native [check-run data](https://docs.github.com/en/rest/checks/runs#list-check-runs-for-a-git-reference)
with bounded pagination; a green combined status, matching name alone, skipped,
neutral, duplicate ambiguous issuer, stale or incomplete result is insufficient.
Only an unambiguously selected current attempt with conclusion success satisfies
each required check. Model text and PR body cannot create that fact.

Use an explicitly head-based CI checkout; if testing GitHub's synthetic merge
revision, its recorded tree and base/head binding must also be verified. A moved
base invalidates the candidate/gates even if head checks remain green. Integrate
the new base through a reviewed normal merge/new commit on the mission branch,
rerun local gates and push normally to trigger new CI; no rebase/force-push shortcut.
For a repair of a ready PR, confirm conversion to draft before changing remote head.
Independent external edits still require reconciliation; no claim of an atomic
transaction across Git, GitHub and human decisions is made.

The initial PR description is deliberately immutable to the controller in this
MVP. It identifies its initial revision/evidence and says later heads require fresh
evidence; current native checks and the operator's versioned delivery report supply
the latest status. Do not overwrite maintainer annotations or pretend metadata writes
have compare-and-swap semantics. A human may publish a later sanitized report; no
automatic comments/body rewrites are required or authorized by this baseline.

## 5. Intent journal and uncertain-effect reconciliation

Persist a controller-owned PublicationIntent artifact before any remote effect:
mission/task/attempt/operation identity; action; repository/principal IDs; base/head
refs and SHAs; expected old remote head; source, policy and authorization digests;
plus a public-safe correlation marker. The artifact digest is STATE-001's operation
request_digest; link its artifact reference from the budget/intent ledger. A PR
number alone is not globally unique. Keep private credentials/transcripts out of it.
Before handing a request to transport, durably mark that dispatch may have begun
and reserve its budget. A crash after that point is unknown even if nothing was
actually sent. Never infer not_dispatched merely from a missing response.

The marker is a lookup hint, not authentication. Ownership reconciliation requires
the approved numeric repository/head-repository/principal identities, exact base/head
refs, expected SHA, saved creation intent and observed PR metadata. The initial
HTML marker may be copied/spoofed; absence or mismatch blocks adoption. Do not bind
an arbitrary existing PR by title or a role's claimed author. Same mission repairs
use the recorded PR identity and new intent keys, not a new PR per agent/attempt.

| Observation after interruption | Action |
| --- | --- |
| One owned open PR, exact expected binding/head/base/marker | Reuse observed identity; record outcome without another create |
| One closed or merged PR | Record terminal external state; no recreate/reopen/merge and no inference of controller acceptance |
| Multiple candidates or wrong author/repository/head/base/marker | Block conflict/ambiguity; operator reconciliation required |
| No candidate, complete bounded lookup, request definitely not dispatched | First create may proceed under remaining consent/limits |
| No candidate after a dispatched/unknown create | Keep unknown; no blind retry or exactly-once claim; visibility delay is not proof of absence |
| Partial pagination, auth/rate error, unavailable server or uncertain observation | Lookup incomplete; preserve intent/reservation and stop dependent publication |
| Push response lost | Inspect owned ref; exact desired SHA may be recorded, expected old SHA may allow a proven-safe dispatch, any other state blocks |
| Ready/draft response lost | Re-read owned PR and refs; reuse the observed state or re-evaluate safe eligible action under LIM-001 |

Query state=all with exact repository/head filters and validate base after retrieval
so a retargeted PR is not hidden by the query. Use at most 100 rows/page and two
pages; continuation beyond that is incomplete, never absence. A later explicit
inspection may continue from the saved cursor. Do not poll continuously: at most
six observations per wait session with capped backoff/jitter under LIM-001, then
block with the last observation and next action. Every API request has the existing
30-second GitHub operation deadline; throttling/Retry-After and overall budgets
still apply. Bound response bytes/artifacts under LIM-001; oversize/truncated
observations are incomplete, not a pass or absence.
SDK/CLI automatic write retry layers must be suppressed or preflight
must block. No automatic repeat of a possibly applied create.

Cancellation closes dispatch first and records pending remote effects. It cannot
undo a push or published PR; do not delete branches or close PRs as cleanup. Reconcile
late observations for history while leaving cancelled delivery unaccepted. Restore
of a local backup rechecks live identity/refs/PR before effects; backup time is not
GitHub time. Logs/errors remain bounded and sanitized, including rate diagnostics.

## 6. Verification boundary and next milestone

Run `python scripts/validate_github_delivery.py` in the existing disposable
jsonschema environment. It validates the frozen policy, private intent shape and
synthetic authority/reconciliation/check-gate examples. It does not invoke Git,
GitHub, gh, CI, accounts or credentials. No new package is installed.

| ID | Required future integration evidence |
| --- | --- |
| GH-01 | Wrong effective token/account/repository/host and missing publication consent block without credential disclosure |
| GH-02 | Default/base/foreign branch, force push, merge, review/status fabrication and settings changes denied |
| GH-03 | Kill after push/create/ready response loss; reuse exact observed effect without duplicate PR |
| GH-04 | Closed/merged/multiple/spoofed candidates, incomplete pages and delayed visibility fail closed |
| GH-05 | Draft CI actually runs; required issuer/workflow/head/base and executed suites verified; skipped/missing/stale results block |
| GH-06 | Repair converts owned PR to draft first; changed base/head invalidates gates and normal merge/push refreshes CI |
| GH-07 | Human acceptance pins exact bundle; self-approval/internal role text cannot substitute for native review or consent |
| GH-08 | Cancellation/restore/rate limit/timeout preserves intent and residual external effects with no destructive cleanup |
| GH-09 | Foreign concurrent ref/PR edit is detected; no force history or maintainer-body overwrite |
| GH-10 | Fully authorized disposable destination demonstrates local checks -> draft -> CI -> ready -> human acceptance, with no auto merge/deploy |

All ten scenarios are unimplemented. Live fault testing needs an explicitly
authorized disposable repository, qualified SBX images and a reviewed native-check
manifest; real publication by this assistant does not prove that runtime adapter.
T-017's design is ready for review. Design stages one through eight are now
documented; T-018 is the next separately requested implementation milestone. No
application scaffold, paid model call, protection change or deployment starts here.

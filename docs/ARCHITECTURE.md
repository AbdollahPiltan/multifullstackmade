# Stage-two architecture baseline

Architecture record ARCH-001, authored 2026-10-29 under the owner's request to
complete stage two, against [MVP-001](MVP-SCOPE.md) and DEV-001 in
[DESIGN.md](DESIGN.md). This is a selected, reviewable implementation baseline;
it is not installed software, a compatibility test result or a runtime security
certification. Implementation still needs a separate instruction.

## 1. Stack decisions

| Area | Selected baseline | Reason / boundary |
| --- | --- | --- |
| Controller language | CPython 3.12, latest available security patch within that minor when scaffolding | One supported minor first; no claim to support untested Python versions |
| Packaging | uv, pyproject.toml and committed uv.lock | Reproducible dependency resolution; no packages added in this documentation task |
| Operator interface | Python argparse CLI and bounded text/JSON output | Standard-library interface suffices; no hosted controller API or dashboard |
| Workflow | LangGraph StateGraph and its SQLite checkpoint adapter | Explicit transitions and persisted continuation; one graph runner, not stacked orchestration frameworks |
| Typed contracts | Pydantic v2 | Validate role input/output, messages and configuration at boundaries |
| Domain memory | Python sqlite3 with parameterized SQL and explicit transactions | Local single-writer workload; no database service or ORM required initially |
| Model integration | Official OpenAI Python SDK, Responses API, behind a provider adapter | One real integration first; explicitly configured model per role, no hardcoded latest model |
| Code execution | Locally managed Docker Engine-compatible Linux containers | Disposable execution against a recorded source snapshot; no automatic host execution fallback |
| GitHub integration | Local Git plus authenticated gh CLI, called through bounded typed commands | Reuse existing operator login; controller-only credential access; one delivery PR |
| Notes backend | FastAPI, Uvicorn, Pydantic v2 and sqlite3 | Small Python HTTP application and separate fixture data |
| Notes frontend | Plain HTML/CSS/browser JavaScript ES modules, served by the notes backend | No React, bundler, Node runtime or separate frontend server needed for this fixture |
| Verification | pytest, HTTPX, Python Playwright/pytest plugin with Chromium; Ruff and mypy for controller checks | Unit, contract/API and real UI integration evidence; tool versions locked at scaffold |
| CI | GitHub Actions with ordinary unprivileged pull_request jobs | Offline/deterministic checks by default; paid real-model runs require explicit operator action |

Python 3.12 remains in the official supported-version lifecycle; this is a deliberate
baseline, not a claim it is the newest release. Review patch availability at scaffold.
[Python lifecycle](https://devguide.python.org/versions/).
uv supports lock/sync workflows; use locked sync in reproducible checks and fail
on an outdated lock. [uv documentation](https://docs.astral.sh/uv/concepts/projects/sync/).

Resolve exact compatible library versions in the first authorized scaffold change,
commit the lock and validate Python/import/test compatibility there. Pin execution
images by digest after review. Do not invent a dependency lock, package patch
versions or a successful compatibility matrix in a design-only change. Initial
target hosts are Linux and macOS with Docker access; Windows support is deferred
until tested. Missing Python, Docker, gh or credentials produces an explicit
prerequisite error, not an implicit install or permission change.

## 2. Modular monolith and dependency direction

One local trusted controller process owns orchestration and access to model/GitHub
credentials. Roles are separate configurations and validated boundaries, not five
services or accounts. Domain policy must not depend on a CLI, LangGraph state
format, SQL connection, Docker client or SDK response class.

| Boundary | Responsibility | Permitted dependency direction |
| --- | --- | --- |
| CLI | Parse operator requests, show lead messages/status and explicit approvals | Application services only |
| Application/controller | Mission use cases, dependency scheduling, limits, approval gates and recovery coordination | Domain plus narrowly scoped adapter interfaces |
| Domain | Task/attempt states, permissions, contract versions, evidence validity, findings, acceptance rules | Standard types / typed contracts; no external effects |
| Role runner | Construct bounded role context, request model output, validate proposed actions | Provider and tool interfaces mediated by controller policy |
| Memory/context | Retrieve approved decisions, indexed files and current evidence; invalidate stale summaries | Domain records plus repository and read-only artifact access |
| Adapters | LangGraph, SQLite, provider, filesystem/Git, Docker, gh and clock | Implement controller-facing interfaces; no independent acceptance decisions |

Use interfaces only for real external boundaries; do not create an interface for
every class. No Redis, queue service, vector database, graph database, cloud worker,
Supabase project, Kubernetes or second agent orchestration framework is needed.

## 3. Planned source layout

These are future paths, not files created by this PR:

```text
src/multifullstackmade/
  cli.py                 operator entry point
  application/           mission use cases and policy-controlled transitions
  domain/                states, contracts, evidence and acceptance rules
  roles/                 five role definitions and bounded context assembly
  memory/                retrieval, summaries and invalidation
  adapters/              graph, storage, provider, GitHub, sandbox and filesystem
tests/
  unit/                  domain invariants and controller behavior
  integration/           persistence, Git, Docker and provider/gh adapter contracts
  acceptance/            MVP scenarios using deterministic and explicitly live modes
fixtures/notes/          reviewed minimal target scaffold and acceptance specification
```

The controller repository and generated fixture workspace are separate. The notes
fixture has backend/ API/data ownership and frontend/ static-asset ownership;
FastAPI mounts its reviewed static assets at the same origin. Shared API contract
artifacts belong to the lead-approved boundary. Frontend cannot modify Backend
files, and neither developer can change independent QA tests to erase a failure.
FastAPI exposes schema-driven APIs and uses Pydantic for validation.
[FastAPI features](https://fastapi.tiangolo.com/features/).

## 4. Graph, storage and restart

Use one stable mission ID as the LangGraph thread identifier. Keep large code,
logs and test artifacts out of graph state; store references and small typed node
results. Persist completed-node outputs and use explicit human-interrupt points.
LangGraph distinguishes checkpoints from long-term stores, and interrupted nodes
restart their node body on resume. Keep side effects outside replayed prompt code
or reconcile them before repetition.
[Persistence](https://docs.langchain.com/oss/python/langgraph/persistence),
[interrupt semantics](https://docs.langchain.com/oss/python/langgraph/interrupts).

Use one private data directory per project outside tracked source. Separate the
LangGraph-owned checkpoint SQLite file from application-owned domain SQLite data
and hashed artifact files; do not modify LangGraph's internal schema. The notes
application uses a different database and must never mount controller memory.
SQLite runs without a separate database server.
[Python sqlite3](https://docs.python.org/3.12/library/sqlite3.html).

An atomic transaction in one database is not atomic across all these stores or
across GitHub. Persist artifact content safely before committing its reference;
domain attempt results are the authoritative reconciliation record. Journal external
action intent with a unique operation key, execute it, record observed result,
then advance the graph. On restart inspect domain results and remote state before
reissuing a model/tool/PR operation. Uncertain paid calls remain uncertain, not
silently retried with an exactly-once claim. Partial orphan artifacts can be cleaned
only after reference reconciliation. Never hold a SQL transaction over a model call.

Enforce one active writer/mission with a project lock and a clear busy error.
Use versioned application migrations, short transactions and bounded busy timeouts.
Later migration design must back up and verify recovery of both database files and
artifact references consistently. Checkpoints are not substitutes for backups.

## 5. Model and role execution

Use Responses API function calling for proposed tools and structured outputs for
typed role results. OpenAI's schema features constrain the shape, not whether the
action is authorized or factually correct; the controller validates both arguments
and permissions. Handle refusals, incomplete outputs and provider failures as
explicit non-success results. Keep provider response details behind the adapter.
[Official function-calling guide](https://developers.openai.com/api/docs/guides/function-calling),
[structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs).

Only the lead communicates product questions to the operator. Each developer gets
the accepted contract, its owned paths, relevant dependencies and findings. Messages
and acknowledgements use the structured contract in DESIGN.md. Sequential role
scheduling does not imply always invoking all roles. QA and Security produce
independent evidence; lead approval cannot override required failures.

The operator supplies a model identifier supporting the required tools/schema
capabilities; preflight checks compatibility instead of replacing it silently.
One model may serve all roles initially. API credentials remain in environment or
operator credential storage, never in role prompts, fixtures, logs or Git. Sending
selected code to the configured model is a remote disclosure: mission setup must
identify the provider and approved project scope. Live usage is metered; record
actual input/output usage and uncertain results. Disable competing retry layers
and put eligible bounded retries under one controller policy. Model-specific
token budgets and numeric retry/time limits remain T-015 design, required before run.

## 6. Tool and sandbox boundary

Agents propose typed operations: bounded file read/search, patch submission,
contract/message handoff and an approved check identifier. They do not receive an
unrestricted host shell, arbitrary network client, raw SQL against controller data,
Docker socket or GitHub token. Resolve paths, reject traversal/symlink escapes,
enforce owned paths and patch-base digests before applying a proposal to a private
worktree. Tool arguments and repository content are untrusted inputs, not policy.

Only the trusted controller invokes Docker/Git/gh with argument arrays and sanitized
environments. Generated source, imports, tests, package hooks and commands run in
containers, not on the controller host. No host Docker socket, home directory,
credential files or controller state is mounted into those containers. Use reviewed,
prebuilt images with locked dependencies; the agent cannot install arbitrary
packages or enable egress as part of a check. Image preparation is a separate
operator-controlled action with explicit network access.

Container profiles require non-root execution, dropped capabilities, default
seccomp, no-new-privileges, read-only root/source snapshot, bounded writable tmpfs,
CPU/memory/PID limits, a command deadline and bounded logs. Docker does not set
resource constraints by default; inspect effective support rather than assuming
requested limits were enforced. Containers share kernel/daemon risk and are not
a complete boundary for arbitrary hostile code. This MVP admits only the scoped
small fixture; an unsupported profile blocks execution.
[Docker security](https://docs.docker.com/engine/security/),
[resource constraints](https://docs.docker.com/engine/containers/resource_constraints/).

For automated API/browser tests, run the notes server and Chromium in the same
test container, using its internal loopback with no external network. Store fixture
data in bounded writable temporary storage and capture evidence with size limits.
This avoids exposing ports merely for automated acceptance. A separate explicit
human preview profile may bind only host 127.0.0.1; restrict origins/hosts and
requests there. No default host-network mode, privileged execution or silent
fallback to running generated code on the host.

## 7. Verification, GitHub and delivery

Controller unit tests exercise policy and failure handling with deterministic
provider/tool doubles. Integration tests cover SQLite restart/reconciliation and
typed adapter boundaries. Fixture API tests hit the real application; Playwright
Chromium tests exercise the actual browser/API integration. Playwright's Python
pytest integration supports browser tests; install the browser in the reviewed
test image and record its version with evidence.
[Playwright Python](https://playwright.dev/python/docs/intro).

Ruff/mypy, pytest and dependency/secret checks become reproducible required commands
in the scaffold milestone. CI uses locked dependencies and no model/GitHub write
secrets for untrusted PR code. CI configuration cannot safely run generated code
with privileged secrets just because an agent authored it. Paid model and external
PR-creation acceptance are explicit opt-in tests against an authorized disposable
destination; report them as not run when unavailable, rather than as simulated passes.

GitHub actions are controller-mediated. Use Git worktrees per assigned developer
and an integration worktree; record ownership while preserving a single final PR.
The operator authorizes the destination/base and gh identity. After required
checks, QA/security and lead review, create/update that PR through a reconciled
operation. Do not claim that five roles imply five independent GitHub reviewers.
No merge/deployment tool is exposed in the MVP.

## 8. Alternatives and consequences

| Alternative | Decision |
| --- | --- |
| TypeScript-only controller | Valid future option; Python keeps graph, model, validation and test tooling in one first-release runtime |
| FastAPI HTTP controller | Deferred; the controller is CLI-local. FastAPI is selected only for the generated notes fixture |
| React/Next.js fixture | Deferred; a small CRUD fixture does not justify a frontend build stack |
| PostgreSQL / distributed queue | Deferred; one active local mission does not need a server or distributed scheduling |
| Vector or graph DB memory | Deferred; structured IDs, path/symbol indexes and targeted search are enough to start; measure retrieval quality before adding embeddings |
| OpenAI Agents SDK plus LangGraph | Not selected; avoid overlapping agent loops. Keep one graph controller and direct provider adapter |
| Unrestricted coding CLI per role | Not selected for MVP; typed operations make tool authority, attribution and replay explicit |
| Host subprocess execution of generated code | Not selected; missing sandbox is a blocker |

Tradeoffs: Docker is a real prerequisite, a limited tool/target stack constrains
generality, and vanilla frontend limits framework demonstrations. These reduce
initial implementation scope while preserving observable end-to-end collaboration.
They do not establish performance or token savings without measurements.

## 9. Remaining design stages and implementation gate

Stage two selects technologies, boundaries, the future source layout, storage
approach and execution model. Stage three specifies exact role/tool authority;
stage four specifies API/message schemas and operation contracts. T-014–T-017
still need migration/retention detail, numerical limits, sandbox validation matrix
and GitHub identity/reconciliation detail. T-018 creates the actual scaffold only
after implementation is requested. A lockfile, container image, installed tool,
passing runtime test or configured CI is not claimed by this document.

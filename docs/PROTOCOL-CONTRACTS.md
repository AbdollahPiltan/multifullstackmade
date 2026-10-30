# Stage-four API, message and tool contracts

Record PROTO-001, contract version `1.0.0`, authored 2026-10-29. This completes
the serialized-contract design under [ROLE-001](AGENT-CONTRACTS.md),
[ARCH-001](ARCHITECTURE.md) and [MVP-001](MVP-SCOPE.md). No API server, model tool,
permission engine or evidence producer is implemented by this document.

## 1. Authoritative files and standards

| File | Contract |
| --- | --- |
| [notes.openapi.json](../contracts/notes.openapi.json) | Five fixture HTTP operations, request/response models, pagination and errors |
| [protocol.schema.json](../contracts/protocol.schema.json) | Invocation, coordination, role result, tool request/response, evidence, task snapshot, human decision and event |
| [protocol.examples.json](../contracts/protocol.examples.json) | Synthetic positive/negative shape cases; not real mission results |
| [notes.examples.json](../contracts/notes.examples.json) | Valid/invalid fixture API shapes |

The HTTP document uses [OpenAPI 3.1.0](https://spec.openapis.org/oas/v3.1.0.html).
The internal records use [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core).
These are selected dialects, not claims to be the newest standards. The schema
files, this document's semantics and ROLE-001 apply together. Unknown object fields
are rejected, never silently ignored. Missing required nullable fields must be
present as null. Formats such as UUID/date-time require format-aware validation.

Canonical stored schemas are not copied blindly into a model API's supported
schema subset. A future provider adapter must derive supported individual tool
parameter schemas and still validate the complete canonical result locally; a
provider that cannot support the needed shape is blocked, not silently downgraded.

## 2. Notes fixture HTTP API

Same-origin local service with base path `/api/v1`. No authentication is claimed;
this boundary is the synthetic, single-user loopback fixture only. Bind to loopback
for explicit human preview, reject unexpected hosts/origins, and do not enable
permissive CORS. Automated acceptance stays inside the isolated test container.

| Method/path | Request | Success |
| --- | --- | --- |
| GET `/api/v1/notes` | `limit` default 20, range 1–100; optional UUID `after` | 200 NotePage |
| POST `/api/v1/notes` | NoteInput JSON | 201 Note; Location points to the relative saved-note URL |
| GET `/api/v1/notes/{note_id}` | UUID path ID | 200 Note |
| PUT `/api/v1/notes/{note_id}` | Full replacement NoteInput JSON | 200 Note |
| DELETE `/api/v1/notes/{note_id}` | No body; UI confirms before sending | 204 with no response body |

NoteInput requires title and permits body; omitted body becomes empty, including
PUT. Null is not an empty string. Title is at most 120 Unicode code points on the
wire; clients trim before submission and the server independently trims using
Python 3.12 string-whitespace semantics, rejects blank results, and enforces the
normalized 1–120 bound. This extra raw-wire bound prevents excessive padding.
Body is at most 5,000 code points. Preserve body content as text, never executable
markup. Reject unknown fields and wrong JSON types instead of coercing them.

Note contains server-generated UUID v4 ID, title/body and server UTC created_at /
updated_at timestamps. PUT preserves ID/created_at and updates updated_at; creates
never overwrite an existing UUID. Edits to the same note are serialized with
last successful write winning: no multi-user optimistic concurrency is claimed.
Persistence must survive restart; deletes remove only the selected record. A repeated
delete of a missing note returns 404, not 204.

List in ascending canonical UUID string order. `after` is an exclusive ordering
cursor and need not identify a currently existing note. Return `next_after` as the
last returned ID only when another record exists; otherwise null. Ordering is stable
for an unchanged dataset, not a snapshot guarantee across concurrent mutations.
The UI reloads after writes and can request subsequent pages; an empty list is a
valid 200 with items empty and next_after null. No unbounded list operation exists.

GET/DELETE accept no request body. POST/PUT require application/json (optional
UTF-8 charset), with at most 32,768 UTF-8 bytes before JSON parsing. Character limits
are separate from that byte limit. Reject malformed JSON, invalid UUID/query values,
unknown query keys and oversized bodies. Mutation methods must not be retried
automatically: a lost POST response may hide a successful create. Internal tool
operation keys do not imply HTTP mutation idempotency.

### Uniform error behavior

All errors use the OpenAPI Error envelope, including framework validation errors:
`error.code`, sanitized `message`, `request_id` and bounded `details` entries with
field/reason. No SQL, tracebacks, file paths, secrets or echoed note content.
The controller is not this HTTP service and exposes no hosted control API.

| HTTP status | Meaning / stable error.code |
| --- | --- |
| 400 | Malformed JSON, invalid path/query or forbidden body: invalid_request |
| 403 | Host/origin outside the explicit local profile: forbidden_origin |
| 404 | Valid UUID does not identify a saved note: not_found |
| 409 | Temporary storage/write conflict: conflict; no success disguised as failure |
| 413 | Raw body exceeds byte limit: payload_too_large |
| 415 | POST/PUT content type unsupported: unsupported_media_type |
| 422 | Invalid JSON field shape/value after applicable normalization: invalid_request |
| 500 | Unexpected failure: internal_error; diagnostics remain private and sanitized |

An error code must match its status even though a reusable error schema lists
all codes. Route/method errors outside these five operations use ordinary HTTP
404/405 behavior with a sanitized error; any framework error exposed as JSON must
use the same envelope. [LIM-001](EXECUTION-LIMITS.md) now specifies local transport
admission and numeric bounds without adding HTTP response shapes.

## 3. Invocation, messages and results

Every canonical record carries protocol_version `1.0.0`. Context includes mission,
task, attempt and invocation IDs; 40-character Git SHA-1 source revision; accepted
contract version and SHA-256 digest; and policy SHA-256 digest. These identifiers
are scoped to this project/mission. Existing human ledger IDs are not automatically
runtime task instances. SHA-256 Git repositories are outside this initial revision
format and must fail preflight instead of truncating a revision.

Invocation is controller-authored: role, requirements/contract artifact references,
owned paths, relevant dependency artifacts/messages, available check IDs and remaining
model/tool/repair/output-token/deadline limits. Example budgets are synthetic values,
not operational defaults; [LIM-001](EXECUTION-LIMITS.md) now selects the numeric
profile, whose enforcement is required before a run.
The active invocation identity is authenticated out of band; copying an invocation
ID or declaring a role in a message does not authorize the caller.

Message fields include sender, recipient, kind, reply_to (nullable), summary, impact,
next_action, bounded artifact/check/finding references and optional resolution_ref.
Kinds are question, proposal, answer, change_request, acknowledgement and handoff.
Only active scoped roles may be recipients; human communication uses ask_human
from the lead, not a fabricated human sender. Sender must equal the authenticated
role. Acknowledgement/answer refers to an existing relevant message and the exact
accepted contract digest. An acknowledgement is not approval of scope expansion.

RoleResult distinguishes ready_for_review, needs_input, blocked, failed and cancelled.
It records actual produced artifacts, optional output revision, findings/questions,
check references, rationale and recipient/next action. A developer's ready submission
must reference its applied revision; a read-only review may reference the unchanged
input revision. No role result or message creates check evidence or human consent.

Plan contains assignments, owners, dependencies, exact owned-path grants, deliverables,
acceptance IDs, required check IDs and an API-contract artifact. The controller checks
unique task IDs, acyclic dependencies, nonoverlapping grants and plan/contract approval.
If a contract is still a proposal, the plan can be recorded but cannot unlock connected
implementation until lead disposition, required human approval and both acknowledgements.

Assessment belongs only to QA or Security, with matching authenticated reviewer,
current revision/context, verdict, covered acceptance IDs, check IDs, findings and
limitations. Finding severity/disposition must have evidence; resolving or marking
false_positive creates a new revision-linked assessment, not overwritten history.
Passing QA requires current applicable collected/executed tests; Security cannot
pass with unresolved critical/high findings or missing required checks.

TaskSnapshot uses the exact task states from DESIGN.md and carries owner, dependency,
attempt, artifact, required-check and open-finding references. It is a controller
observation, not an agent transition command. HumanDecision is captured by the
controller from the actual operator and pins the approved/rejected plan or delivery
artifact; no role tool accepts it as caller-supplied approval. Event records trusted
creation time, actor, record kind and artifact digest, with a linked supersession
reference for corrections. Thus messages/results have auditable timestamps without
trusting a model-provided clock. Validate event/record kind consistency at runtime.

## 4. Eleven typed tool calls

ToolRequest includes request_id, operation_key, immutable invocation context and a
discriminated call containing tool and arguments. All result objects are closed.
The role allowlist is recorded as schema metadata `x-tool-role-allowlist`; metadata
is not executed by JSON Schema, so runtime policy must explicitly enforce it.

| Tool | Arguments | Successful result | Extra runtime condition |
| --- | --- | --- | --- |
| read_file | relative path, start_line, line_count (1–200) | artifact reference, bounded content, truncated | Scope/path checks and immutable source digest |
| search_files | literal (not regex), paths, max_matches (1–50) | bounded path/line/excerpt matches, truncated | Relevant allowed paths; no arbitrary shell search |
| read_artifact | artifact ID/digest, offset, max_characters (1–65,536) | matching reference, content, truncated | Project/access scope and digest match |
| submit_patch | 1–20 write/delete changes, rationale | proposal ID, recorded/applied, optional output revision | Owned paths; current base digests; lead denied |
| propose_change | kind, rationale, impact, proposal artifact, affected tasks | proposal ID, recorded | lead_decision kind only for lead; no application by this tool |
| request_check | registered profile ID, source digest | check ID and controller evidence reference | Profile must be permitted and immutable; no shell argument |
| send_message | Message | message ID, recorded | Matching sender, active recipient and reply context |
| propose_plan | Plan | plan ID, awaiting_authorization | Lead only; recording does not approve |
| ask_human | question, reason, affected tasks | question ID, awaiting_human | Lead only; no fabricated response |
| submit_assessment | Assessment | review ID, recorded | QA/Security only and matching reviewer; no automatic acceptance |
| submit_delivery | verdict, review/check/acceptance IDs, limitations, summary | delivery ID, recorded | Lead only; controller rechecks all independent gates |

Patch writes specify path, base_digest (null only for absent file) and content;
deletes require a digest and have no content. No rename shortcut, binary patch or
arbitrary host path is accepted. Reject duplicate paths, traversal, symlink escapes,
protected files, stale bases and writes outside owned grants before any change.
Apply all changes atomically to the candidate workspace or leave it unchanged.
A recorded proposal is not an applied patch. Content is bounded to 65,536 characters
per file and 20 files per request; runtime must also cap UTF-8 bytes and total work
under LIM-001, and must never silently truncate a patch.

Initial registered profile IDs: frontend_unit (Frontend/QA), backend_unit
(Backend/QA), api_contract (Backend/QA), qa_integration (QA), security_static
(Security), security_negative (Security). Lead may request reruns of required profiles
but cannot edit their commands. Invocation available_check_ids further restricts
the set. A tool request cannot add a check profile. Exact commands/images are
reviewed at scaffold and profile validation; they are not executable strings in
model output. Container restrictions from ARCH-001 apply to every profile.

ToolResponse is controller-authored and correlated by request_id and immutable
context. `ok` means the requested operation produced its typed result; for
request_check it does not mean the check passed. Failed variants carry denied,
failed, unavailable or cancelled plus code, sanitized message, retryable and next
action. Codes are permission_denied, invalid_arguments, stale_revision,
stale_contract, limit_exceeded, not_found, conflict, tool_unavailable,
execution_failed and cancelled. Retryable is advice subject to controller budget
and replay safety, never authorization to retry a non-idempotent action.

## 5. Evidence, replay and semantic gates

Only the controller produces Evidence from observed tool execution: profile,
environment/source digests, revision context, UTC start/end, outcome, exit code,
nullable collected/executed test counts, artifact references and reason. Valid
outcomes are passed, failed, not_run, unavailable, stale and cancelled. Do not mark
test checks passed when no tests executed, despite a zero process exit code.
Non-test scanner counts may be null, with an explicit profile classification.

JSON Schema cannot enforce referential truth, actor identity, graph state, timestamps
ordering, current Git state or whether a test ran. The zero-test evidence shape in
the example bundle is intentionally structurally valid and semantically unacceptable
for a required test gate. Implementation must cover these additional rejections:

- Authenticated role mismatch, unauthorized tool/profile/path, forged evidence or approval.
- Unknown cross-project references, mismatched artifact digest, stale policy/contract/revision.
- Invalid reply/acknowledgement chain, duplicate task IDs or cyclic dependencies.
- Patch base mismatch, conflicting path changes, symlink/protected-file escape.
- Status/code mismatch, end time before start, tests executed exceeding collected,
  zero-test success, or missing/failed/stale required evidence.
- QA/security assessment that does not match the active reviewer and tested revision.
- Lead verdict that lacks valid independent reviews or claims merge/deploy authority.

operation_key is scoped to mission/task/attempt and identifies one canonical tool
request. Identical replay returns its recorded observation without reapplying effects;
reuse with different tool, context or arguments returns conflict. An uncertain
external action is reconciled before replay. Cached results cannot unlock a gate
after code/contract changes; mark affected observations stale. Request IDs correlate
responses and are not a substitute for operation-key/revision checks.

## 6. Versioning, validation and next boundary

For v1 all fields and enums are closed. Even adding an optional field or enum value
can break a strict old consumer; treat wire-shape or semantic changes as a new major
contract unless every affected consumer explicitly negotiates the new version.
Patch releases can correct explanations without changing accepted behavior. The
artifact digest pins the exact schema bundle; a version string alone is insufficient.
Backend proposes, both developers acknowledge, lead reviews, and the human approves
material scope expansion. Invalidate affected fixtures, checks and approvals.

Validation commands (tooling only, outside the application environment):

```sh
python -m pip install jsonschema==4.25.1 openapi-spec-validator==0.7.2
python scripts/validate_contracts.py
git diff --check
```

Use a disposable environment for the first command. No application dependency or
lockfile is added in this design task. The validator checks local schemas/OpenAPI,
references, role allowlists and positive/negative shape examples. It does not prove
controller authorization, API behavior or runtime acceptance. Format validation is
enabled; all references are local and validation requires no remote schema retrieval.

T-013 delivers these contracts for review. Stage-five [STATE-001](STATE-PERSISTENCE.md)
specifies graph/storage/migration/retention without changing these wire contracts.
Stage-six LIM-001 specifies numeric execution limits and retry/repair/cancellation.
T-016/T-017 retain validated sandbox profiles and external identity/reconciliation detail. T-018 remains the future scaffold;
no server, agent, permission engine or model integration is started here.

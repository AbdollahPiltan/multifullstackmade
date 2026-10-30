# Stage-six bounded execution policy

LIM-001, 2026-10-30, completes design task T-015. This selects initial **admission
ceilings**, not measured latency, cost or throughput guarantees. Applies to the
local notes MVP from [MVP-001](MVP-SCOPE.md), [ARCH-001](ARCHITECTURE.md),
[ROLE-001](AGENT-CONTRACTS.md), [PROTO-001](PROTOCOL-CONTRACTS.md) and
[STATE-001](STATE-PERSISTENCE.md). No runtime scheduler, provider retry loop,
container profile or cancellation handler is implemented by this delivery.

The machine-readable baseline is [execution-limits.json](../contracts/execution-limits.json),
validated by [its schema](../contracts/execution-limits.schema.json). Units are in
field names: seconds, UTF-8 bytes, tokens, counts and MiB (1,048,576 bytes).
An operator may lower ceilings at mission creation within this profile's schema
and cross-limit consistency checks;
no role may raise them. Zero disables repairs where explicitly allowed, not an
unlimited sentinel. Raising a ceiling requires a reviewed policy/profile revision
and explicit operator adoption. Existing consumption/reservations are preserved
when adopting any changed policy; reject ceilings below outstanding usage.

## 1. Scheduling and count ceilings

| Scope | Initial maximum |
| --- | --- |
| Concurrent active missions per project | 1, including blocked missions |
| Concurrent role invocations, model requests, tools or containers | 1 each; no speculative/background role execution |
| Planned tasks / ready queue | 16 tasks / 16 ready IDs; deterministic plan order after satisfied dependencies |
| Role invocations per mission | 32; clarification/review/resume invocations also count |
| Model requests | 40 per mission, 8 per task attempt, 4 per invocation |
| Tool proposals | 240 per mission, 48 per task attempt, 24 per invocation; denied/invalid proposals count |
| Actual check executions | 24 per mission; every rerun/retry that executes counts |
| Repair attempts | 2 per task, 6 total per mission; initial attempt plus at most two repairs per task |
| Structured messages | 128 per mission, 16 per task; maximum reply-chain depth 6 |

Reject a full queue before accepting more work. Do not create unlimited waiting
futures; accepted tasks are durable records, not 16 simultaneously running workers.
Admission is atomic across all applicable scopes. A replay returning a recorded
observation consumes a tool proposal slot if dispatched by a role, but does not
consume a new effect/check execution. Transport retries consume request slots;
they do not grant extra invocations or repairs. An operator status read/cancel is
not a role tool call and remains available when role budgets are exhausted.

A task attempt is STATE-001's attributed work attempt. It may have several bounded
invocations; starting another invocation cannot reset its counters. A review or
clarification task is also counted. Resuming a human interrupt before any new
provider dispatch need not create an invocation; dispatching one does. Keep counted
operation identities so replay/reconciliation cannot double-charge a reservation.
Do not create replacement missions/tasks or rename work to evade a depleted budget;
new missions require an explicit operator request and preserve prior provenance.

## 2. Deadlines, waits and cancellation

| Deadline | Initial maximum |
| --- | --- |
| Mission lifetime from first creation | 86,400 seconds, includes human waits, deliberate pauses, blocked time and process downtime |
| Mission active execution | 3,600 seconds, includes retries/backoff and running tools |
| Task active execution / invocation | 900 / 300 seconds |
| Model request / ordinary file/message tool / GitHub operation | 120 / 10 / 30 seconds |
| SQLite busy wait | 1 second; conflict is reported, no nested retry loop |
| frontend_unit / backend_unit / security_static | 60 seconds each |
| api_contract / security_negative / qa_integration | 90 / 90 / 180 seconds |
| Graceful stop before force-stop / total cleanup allowance | 5 / 15 seconds |

Before dispatch choose the earliest enclosing mission/task/invocation/operation
deadline; retries never reset it. Ordinary tools exclude request_check, whose
registered profile deadline applies. Deadline includes output collection; budget
remaining must be positive. A queue wait consumes mission active time while the
runner is active; sequential scheduling must not hide it as a paused interval.

Persist creation time, absolute expiry, cumulative active seconds and the last
durable observation. Use a monotonic clock for intervals inside one process;
monotonic values are not portable timestamps across restarts. On recovery, conservatively
charge the unobserved interval since the last durable observation as active unless
a durable quiescent human-wait/pause marker proves no effect was running. Ambiguous
or backward wall-clock movement blocks resume for reconciliation, never replenishes
time. The 24-hour lifetime is not extended by pausing or restarting. After expiry,
cancel/reconcile residual effects and report blocked/expired, not delivered.
[Python's monotonic clock](https://docs.python.org/3.12/library/time.html#time.monotonic)
is suitable for measuring elapsed intervals inside the running process.

Human waits and explicit quiescent pauses stop active timers after effects settle,
but not the lifetime clock. There is no fabricated reply or automatic plan acceptance.
There is no new paused wire state: retain the valid graph stage and durable wait
reason. On resume re-evaluate limits, ownership, input digests and unknown effects.

On operator cancellation, atomically persist cancellation and close the admission
barrier before returning acknowledgement. Check that barrier before each dispatch
and after each returned observation. Signal running owned work, allow at most five
seconds, then force-stop owned processes/containers through trusted adapters; stop
observing after the fifteen-second cleanup deadline and record any unresolved
effect. No generic kill-by-name command. Network cancellation cannot undo a remote
effect or promise that a provider stopped billing. Late results stay historical;
they cannot advance cancelled tasks or release an uncertain reservation as success.
Trusted reconciliation may settle actual usage later without reopening the mission.
The mission may be terminal cancelled while cleanup remains unresolved; retain the
project's external execution slot and refuse a new active mission until reconciled.
No model invocation is required to honor operator cancellation or inspect status.
Persist the cleanup deadline once; restart cannot extend it. Bounded cleanup may
continue for at most fifteen seconds after expiry/cancellation, solely to stop or
observe effects, never to perform additional product work.

## 3. Retry and repair are different policies

Only the controller owns retries. Disable automatic repeat layers in SDKs, HTTP
clients and wrappers; otherwise fail adapter preflight. Maximum **three dispatches
including the first**, all charged to their enclosing request/time/token budgets.

A still-pending operation intent may contain these safe transport dispatches, each
with a durable dispatch ID and its own request/token reservation. This is separate
from a new work/repair attempt. Once a final ToolResponse is observed, replay of its
operation key returns that observation; it does not restart retries. A changed
authorized action uses a new key. A repeated role request cannot create a second
dispatcher for an already pending intent.

| Observation | Automatic retry behavior |
| --- | --- |
| Read-only observation failed transiently; no effect can occur | Eligible under remaining limits |
| Transport proves request was not dispatched | Eligible; preserve the durable intent and record the new dispatch |
| 429/503 or another adapter-classified transient failure | Eligible only when repetition is safe and absence of an applied/unknown effect is established |
| Timed-out/disconnected paid call, patch, Git write or PR request with uncertain result | No automatic retry; reconcile first, preserve reservation |
| Invalid shape/path/permission, stale contract/base, authentication error | No unchanged retry; fix the cause through the authorized path |
| Provider refusal or incomplete/invalid role output | Explicit non-success; lead disposition, never a retry-until-compliant loop |
| Failed test, security finding or zero executed tests | Evidence for diagnosis/repair, not a transient transport retry |
| Missing sandbox, unsupported profile, exhausted limit or cancellation | Block/cancel; no host fallback or retry loop |

Eligible retry delay uses full jitter: `U(0, min(16, 2 * 2**(dispatches_used-1)))`
seconds. If Retry-After is valid, wait at least that long using
`max(jitter, retry_after_seconds)`. Parse both delay-seconds and HTTP dates at the
adapter boundary; negative/past values become zero, invalid values are ignored with
a diagnostic. If the required wait exceeds 60 seconds or leaves no positive
execution time, block with earliest retry time rather than silently shortening it.
Honor the protocol's [Retry-After semantics](https://www.rfc-editor.org/rfc/rfc9110.html#name-retry-after).
Backoff is cancellable and consumes active time. Remaining operation timeout is
clamped to the remaining enclosing deadline after delay. A retryable field in
ToolResponse is advice, not permission or a guarantee that a replay is safe.

For a repair, persist the failing evidence and owner, concrete diagnosis, planned
change and affected acceptance/check IDs. Reserve both per-task and mission repair
slots atomically before a new attempt. A repair slot remains consumed after a
failed/cancelled/unknown attempt. No unchanged retry without new diagnosis or a
changed condition. Route shared-contract/configuration changes through the lead
and required authorization; do not reassign paths to bypass the failed gate.
Rerun relevant combined checks and independent review on the new snapshot. A lead
cannot override failing, missing, stale or zero-test evidence. Exhausted limits
produce a compact lead/operator blocker with the last failure and required next action.

## 4. Metered usage and durable reservations

| Budget | Initial maximum |
| --- | --- |
| Model input / output per request | 16,000 / 4,000 tokens |
| Total model tokens per mission | 400,000, input plus output, including uncertain reservations |
| Complete serialized provider input | 65,536 UTF-8 bytes, including tools/system/selected context |
| Serialized model response / tool request envelope | 1,048,576 bytes each |

Before a model dispatch reserve the verified input-token bound plus the output
ceiling and a model-request slot. Include tool definitions and all provider-visible
content in the input bound. Preflight must verify a tokenizer/counter or a proven
conservative bound for the explicitly configured model. Do not equate characters,
UTF-8 bytes or another model's tokenizer with tokens; unavailable accounting blocks
live execution. Effective output limit is the smallest configured, model-supported,
invocation and remaining budget cap, and must be positive.

On a completed observation settle tokens using actual provider input/output usage,
including reported reasoning/output usage without double-counting nested details.
Cached input still counts here. Refund only provably unused reserved tokens;
dispatch-count slots remain spent. Unknown usage retains its reservation. An
observed usage above the reserved bound blocks further dispatch and triggers an
accounting incident; never silently clamp a billed observation. These are controller
admission limits, not a guaranteed currency cap or statement of provider billing.
The configured model and any pricing report are verified separately at live setup.

Persist a versioned budget-ledger artifact referenced by STATE-001 missions. It
contains policy/profile digest, scope IDs, cumulative spent values, outstanding
operation reservations, settled operation IDs, time/wait observations and expiry.
Update it and the effect intent in the same short domain transaction. Every retry,
repair and resumed invocation consults it. `spent + reserved + proposed <= ceiling`
must hold for every applicable budget before dispatch; equality is allowed.
Do not run more than one pending dispatch while reconciling an unknown operation.

PROTO-001 Invocation.remaining_budget remains unchanged: model_calls/tool_calls
are the minimum remaining count over applicable scopes; repair_attempts is the
minimum task/mission allowance; max_output_tokens is the effective positive request
limit; deadline is the earliest active UTC deadline. Token/storage/other counters
remain trusted controller state, not caller-modifiable extra wire fields. If no
positive output allowance remains, block before creating an invocation; never emit
zero for the schema's positive max_output_tokens field.

## 5. Bytes, storage, resources and overload

| Scope | Initial ceiling / response at limit |
| --- | --- |
| Candidate source snapshot | 128 regular files, 2,097,152 total bytes; no symlink/special-file expansion |
| Source file / one patch request | 262,144 bytes per file / 1,048,576 total envelope bytes; existing 65,536-character/file and 20-change shape caps still apply |
| One tool read response | 262,144 serialized bytes, plus existing per-tool line/character/match caps |
| Event page / selected context records / untrusted JSON depth | 100 / 100 / 32; paginate records, reject excessive nesting before recursive validation |
| One artifact | 4,194,304 bytes; reject before persisting larger content |
| Combined stdout/stderr per check / per mission | 1,048,576 / 8,388,608 bytes; stream with bounds; truncation cannot satisfy a required check |
| Private project directory, including databases/WAL/objects/staging/managed worktrees | 536,870,912 bytes, includes retained missions; reserve before writes |
| Diagnostic/control reserve inside that directory | 16,777,216 bytes within the total, unavailable to ordinary effects |
| Check container | 2 CPU quota units, 1,024 MiB memory, total memory+swap equal to memory, 128 PIDs, 128 MiB writable tmpfs |

Admission must account for serialized UTF-8 bytes and transient copies. Existing
PROTO-001 character caps remain in addition to these byte caps, so a shape-valid
proposal can still be rejected with limit_exceeded. Never truncate a patch, required
contract or JSON record into a different accepted operation. Paginate optional
reads; a missing required excerpt blocks the dependent invocation.

Reserve maximum bounded effect output plus database/WAL/staging headroom before
starting an effect. On storage exhaustion stop scheduling and checkpoint a sanitized
limit_exceeded observation using the reserved control area. If durable recording
also fails, stop effects and require explicit recovery; never report completion.
No automatic history purge to create space. Explicit cleanup follows STATE-001;
operator-controlled image caches, backups and existing source repositories outside
the managed directory are reported separately and never silently deleted.

Resource limits require effective runtime verification, not just command flags.
Docker has [no resource constraints by default](https://docs.docker.com/engine/containers/resource_constraints/).
[SBX-001](SANDBOX-PROFILES.md) now fixes profile requirements and the image-release
gate. Pin actual images and validate CPU/memory/PID/tmpfs enforcement before running
on supported hosts. Failure/timeout/OOM/log overflow is non-success evidence, not a
passing test. No network egress, host execution fallback or new permission is
implied by this policy. These caps are for the small fixture and may require a
reviewed revision after measurement.

The notes API retains PROTO-001's 32,768-byte request body and 1–100 item page cap.
Its reviewed local server profile must additionally enforce 8 active connections,
zero application request backlog and a 10-second connection/request lifetime;
excess connections are closed/rejected at transport admission, shown as a visible
network error by the client. No new 429/503 JSON shape is invented. Any later HTTP
overload response needs an explicit compatible contract revision before exposure.
The local synthetic-data profile has no public ingress or public per-user rate
policy; SBX-001 requires future admission tests under repeated connections.
A hosted API would need
its own authentication/rate/ingress design and remains outside this MVP.

## 6. Failure reporting and future acceptance

Limit/cancellation/unknown-effect responses use existing PROTO-001 statuses/codes;
graph exhaustion becomes blocked with the last safe stage and saved counters.
Report scope, limit name, observed/reserved values, last evidence, unresolved
operation IDs and allowed next action, without secret content. Missing capability
is unavailable, a check failure is failed, cancellation is cancelled; none is passed.
No depleted model budget is needed to prepare a controller-authored status/blocker.

Run `python scripts/validate_execution_limits.py` in the existing disposable
contract-validation environment (jsonschema 4.25.1). It validates the closed profile
and positive/negative design examples for bounds, atomic admission, retry windows,
repair totals and cancellation/expiry. It uses synthetic arithmetic and never
dispatches work. Also run the earlier contract and state-design validators.

| ID | Required future runtime evidence |
| --- | --- |
| LM-01 | Exact count/token boundary accepted once; next dispatch denied across all enclosing scopes |
| LM-02 | Kill/restart after reservation and unknown paid effect; no budget reset/refund or blind repetition |
| LM-03 | Third task repair or seventh mission repair denied; original failure/owner/attempt history retained |
| LM-04 | Retry-After, jitter, attempt ceiling and earliest deadline honored with cancellation during backoff |
| LM-05 | SDK/wrapper retry suppression verified with observed dispatch counts, including faults |
| LM-06 | Human wait pauses active time only; lifetime expires; backward/ambiguous clocks block recovery |
| LM-07 | Cancel closes admission before acknowledgement; grace/cleanup bounded; late result cannot accept delivery |
| LM-08 | Queue/connection/body/patch/log/artifact/storage limits exercised; no hidden unbounded buffer or forged pass |
| LM-09 | Container CPU/memory/PID/tmpfs enforcement, OOM and timeout produce genuine non-success evidence |
| LM-10 | Unknown tokenizer/usage or missing capability blocks; actual metering and representative timings reported |

These ten scenarios remain unimplemented. SBX-001 now provides sandbox/access design;
[GH-001](GITHUB-DELIVERY.md) now specifies GitHub identity and external reconciliation.
T-018 starts the scaffold only after
implementation is requested.
No currency savings, performance target or successful runtime enforcement is claimed.

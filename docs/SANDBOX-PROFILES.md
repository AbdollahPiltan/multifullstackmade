# Stage-seven sandbox and tool-access design

SBX-001, 2026-10-30, completes the design deliverable T-016. Baselines:
[ARCH-001](ARCHITECTURE.md), [ROLE-001](AGENT-CONTRACTS.md),
[PROTO-001](PROTOCOL-CONTRACTS.md), [STATE-001](STATE-PERSISTENCE.md) and
[LIM-001](EXECUTION-LIMITS.md). This is a reviewed-design candidate and static
validation tooling, not a working sandbox or a security certification.

Docker CLI is not installed/on PATH in this task environment. No container, image
pull/build, daemon configuration or hostile-code execution was attempted. Real
image digests, locked tool/browser versions and host enforcement evidence must be
produced during the separately authorized scaffold/image qualification work.

## 1. Trust boundary

The local trusted controller alone holds provider/GitHub credentials, the project
lock, domain/checkpoint data and access to Docker/Git/gh. A role proposes one of
PROTO-001's eleven typed operations; authenticated invocation identity, current
revision, ownership, limits and tool allowlists are checked before every effect.
Text in a repository, model response, filename or tool error grants no permission.

Generated source, tests, imports, build hooks and fixture processes are untrusted
code. Execute them only in a qualified disposable container. Host-side work is
limited to bounded data parsing, safe file operations and explicit trusted
Git/Docker/gh adapters; do not import a target Python module, run its shell scripts,
load its plugins, install its dependencies or execute its hooks on the host.
Git hooks, external filters, credential helpers, submodules and repository config
from an untrusted target are not executable instructions: adapters must disable or
isolate them. GitHub identity and external operation details are now specified in
[GH-001](GITHUB-DELIVERY.md).

Containers share kernel/daemon risk; this MVP admits only the scoped synthetic
notes fixture. It does not claim isolation suitable for arbitrary hostile public
repositories. [Docker security](https://docs.docker.com/engine/security/) describes
the daemon, kernel and configuration boundaries. No automatic privilege/network
expansion or host fallback is permitted when a capability is unavailable.

## 2. Common execution envelope

The machine-readable policy is [sandbox-profiles.json](../contracts/sandbox-profiles.json),
with [a closed schema](../contracts/sandbox-profiles.schema.json). It describes
requirements; it is not a Docker command/config file. No role may supply Docker
flags, entrypoints, mount sources, environment variables or arbitrary commands.

| Boundary | Requirement for every automated profile |
| --- | --- |
| Runtime | Linux container on a qualified local Linux/macOS Docker environment; remote daemon, Windows and automatic installation are outside MVP |
| Identity | Non-root driver UID/GID 10001; service UID/GID 10002 where needed; no supplementary host groups |
| Privileges | No privileged mode/devices, drop all capabilities, no-new-privileges, private PID/IPC namespaces, no host namespace/socket sharing |
| Filesystem | Read-only root and immutable source export at `/src`; trusted harness/suites in the pinned image; no write access to image or tests |
| Mounts | Only the verified source export plus private bounded tmpfs; no home, Git metadata, controller state, credential store, Docker/SSH socket or arbitrary bind mount |
| Network | `none`, no published ports, DNS/egress, host gateway, links or extra network attachments; IPv4 loopback only for in-container HTTP tests |
| Environment | Rebuilt allowlist, never inherited host environment; no API/GitHub/cloud/proxy credentials or extra loader/plugin paths |
| Resources | LIM-001 CPU/memory+swap/PID/log/deadline ceilings, rechecked against effective host support |
| Lifecycle | One owned container/check identity, bounded startup/collection/stop, no restart policy, no automatic image pull |

Docker's [none network](https://docs.docker.com/engine/network/drivers/none/)
provides loopback without an external interface. This is separate from the host
controller's authorized provider/GitHub connection. Automated fixture requests use
127.0.0.1 in that container, never a host port or remote URL.

Use tmpfs partitions within LIM-001's total 128 MiB: `/tmp` 32 MiB owned by driver,
`/run/notes` 32 MiB owned by service, `/dev/shm` 64 MiB owned by driver. Private data
directories use 0700; noexec/nosuid/nodev on writable tmpfs. The source export is
readable but immutable; ignore the image's writable defaults. The service database
and temporary files live only in its partition; set HOME/cache/temp paths explicitly.
No disk-backed writable layer is an unbounded fallback. Browser compatibility with
these constraints must be tested; inability to start is unavailable, not passed.

The trusted controller starts service processes as UID 10002 through a fixed adapter
operation when a profile needs them, then runs the driver as UID 10001. It does not
grant SETUID capabilities or a Docker socket to either process. The driver uses
HTTP/browser interfaces to the service rather than importing service code. Same-user
unit tests still execute untrusted code and cannot alone establish independent
QA/security evidence. Different UIDs, read-only suites and denied ptrace/capabilities
reduce tampering opportunities; runtime attack tests remain required.

Allowlisted fixed environment: PATH to reviewed image executables; LANG=C.UTF-8,
TZ=UTC, HOME/TMPDIR/cache paths in the assigned tmpfs; PYTHONDONTWRITEBYTECODE=1;
PYTHONNOUSERSITE=1; PYTEST_DISABLE_PLUGIN_AUTOLOAD=1. Any required Python/pytest
plugin is explicitly pinned by the harness, never loaded from target configuration.
Use isolated interpreter mode with bytecode disabled (`-I -B`) and trusted test config/collection paths; target
conftest.py, sitecustomize, .pth files and local pytest.ini must not alter the harness.
Approved unit-test imports execute inside the container only. Target code may still
lie about behavior or printed reports; an exit code/report file alone is insufficient
proof of independent execution. Validate expected suites/counts and cross-check the
observed service/browser behavior with independent test evidence.

Mandatory fixture acceptance suites are frozen in the image. Developer/QA/Security
tests from the source export are additional attributed suites run separately;
their configuration or results cannot suppress/replace the mandatory driver.
Record their exact source digests and expected collection before execution. New
requirements outside the frozen fixture require reviewed suite/manifest changes.
Browser debugging uses private pipes, with no listening debug endpoint accessible
to the service or outside the container.

## 3. Six registered profiles

| Profile | Requesting roles | Driver / service behavior | Seccomp | Deadline |
| --- | --- | --- | --- | --- |
| frontend_unit | Frontend, QA, Lead rerun | Trusted browser harness runs frontend interaction/unit scenarios; controlled fixture service | reviewed browser derivative | 60 s |
| backend_unit | Backend, QA, Lead rerun | Isolated target unit tests plus trusted collection assertions; no independent-review claim from developer tests | engine default | 60 s |
| api_contract | Backend, QA, Lead rerun | Trusted HTTP driver against real notes service, exact PROTO-001 requests/errors | engine default | 90 s |
| qa_integration | QA, Lead rerun | Trusted Chromium driver, real browser + API CRUD/persistence/error scenarios | reviewed browser derivative | 180 s |
| security_static | Security, Lead rerun | Read-only source/dependency/secret analysis with reviewed offline scanners/advisory data | engine default | 60 s |
| security_negative | Security, Lead rerun | Trusted negative HTTP/input/output scenarios against the fixture service | engine default | 90 s |

Lead reruns are limited to required profiles included in its invocation; Lead
cannot edit the command. Role allowlist alone is insufficient: task relevance,
available_check_ids, snapshot, remaining limits and qualified release must agree.
The six IDs and role sets match PROTO-001. Profiles map to fixed image harness IDs;
neither test selectors nor user-provided command suffixes can skip required suites.
Changes to harness, locks, CI, collection rules or scanners follow the separate
shared-configuration authorization path in ROLE-001.

The image must supply all dependencies and Chromium before execution. Offline
dependency analysis requires a dated, reviewed advisory snapshot and explicit
freshness rule; absent/expired data or a missing required scanner yields unavailable.
The initial advisory-age ceiling is seven days (604,800 seconds) at check start;
clock uncertainty blocks freshness validation rather than treating data as current.
No live scanner download, pip install, browser installation or package lifecycle
hook is allowed during a check. Exact tools/lock versions and accepted advisory
freshness observations are recorded with the real image release, not invented by this design.

## 4. Browser seccomp amendment and image release gate

ARCH-001 originally requested default seccomp for all profiles. SBX-001 refines
that architecture choice for the two browser profiles only: require a reviewed,
digest-pinned derivative of the qualified engine default allowing the minimal
unprivileged user-namespace operations Chromium needs. Other profiles retain the
engine default. Never use seccomp=unconfined, --no-sandbox, host IPC or SYS_ADMIN
to make a failing browser start. Root Chromium is also prohibited.

This amendment has a concrete compatibility reason. Official
[Playwright Docker guidance](https://playwright.dev/python/docs/docker) describes
non-root execution and a seccomp derivative for Chromium's sandbox; its convenient
host-IPC/root examples do not satisfy this project's envelope. Docker advises
[retaining default syscall restrictions](https://docs.docker.com/engine/security/seccomp/).
The derivative must preserve those denials except individually reviewed user-namespace
rules, retain argument restrictions, and be validated on the selected engine/kernel.
There is no seccomp JSON here that claims a tested rule set. If the derivative,
noexec tmpfs or Chromium compatibility is unqualified, block the browser profile.

The checked-in profiles contain `release: null` deliberately. This is **not an
executable release**. At image qualification, record a controller-reviewed release
artifact containing:

- Image repository and exact sha256 digest/platform, source revision, locked tool
  and browser versions, build provenance and dependency/license/secret review.
- Harness/suite/collection manifest digests; required scanner IDs, dated advisory
  content digest and accepted age; no missing/empty required suites.
- Custom browser seccomp digest and its reviewed base/patch, or qualified engine
  default identity; engine/kernel/architecture and effective resource capabilities.
- Current SB-01–SB-12 evidence for that exact envelope and LIM-001 digest;
  approving operator/reviewer identity and qualification timestamp.

No invented image digest, mutable latest tag or synthetic observation may unlock
execution. `release` stays null until these artifacts exist; the runtime's trusted
release registry supplies a validated reference, not caller-edited JSON. Qualification
is invalidated by image, harness, seccomp, policy, resource or material host changes.
Image preparation is an explicit operator action with approved network access and
no mission credentials. Pull/build/qualification work is outside this design-only
delivery; pinned manifests must be committed/referenced at that later checkpoint.

There is no automated preview profile in this release. ARCH-001 allowed a possible
explicit local preview, but safely combining host reachability, origin checks and
denied egress requires separate qualification. Keep it disabled until that profile
is reviewed; never replace `network=none` with bridge/host just to show a browser.
Automated Chromium tests and screenshots remain the planned first acceptance path.
LIM-001's API connection/lifetime limits still apply inside the automated profiles.

## 5. Path, patch and artifact boundary

The model's relative path is untrusted even when it passes JSON Schema. Restrict
to PROTO-001's ASCII path alphabet/240-character bound; reject absolute, drive/UNC,
backslash, percent escapes, empty/dot/dot-dot components, doubled separators, NUL,
hidden components and case-fold collisions. Do not decode an encoded path into a
second operation. Protected names are denied case-insensitively.

| Fixture root | Ordinary patch owner |
| --- | --- |
| frontend/, tests/frontend/, docs/frontend/ | frontend |
| backend/, tests/backend/, docs/backend/ | backend |
| tests/qa/ | qa |
| tests/security/ | security |

Only exact task grants inside these roots allow ordinary writes; prefix strings
cannot grant frontend-evil/ or another role's tests. Lead has no patch authority.
Relevant sanitized reads may cross role roots when approved for that invocation;
arbitrary root reads are denied. Shared API files/configuration/locks/CI and all
controller/private/credential paths are outside ordinary patch authority, even
when a broad path grant is presented. Protected test/config names include conftest.py,
pytest.ini, pyproject.toml, setup.cfg/setup.py, tox.ini, requirements*.txt, package*.json,
lock files and dependency/security tool configuration at any depth. Renaming or
placing such a file under owned code does not bypass the shared-change gate.

For actual filesystem operations, open the approved source root by directory handle
and traverse without following symlinks. Reject symlinks, special files, hardlinks
(nlink != 1), mount escapes and changed file identity; verify type, base digest and
ownership on the opened object. Do not rely solely on resolve()/string-prefix checks
or a precheck followed by an unchecked open. The controller holds the writer lock;
workers only see a separate immutable export. Host changes detected during export
invalidate the snapshot. The future Linux/macOS adapter must test platform-specific
no-follow/open-at behavior and collision handling.

Normalize exported source files to 0444 and directories to 0555 inside an
owner-only host parent, so both non-root container identities can read the bind
mount without exposing the export through its host parent. Do not preserve target
ownership, setuid bits, executable modes or extended privileges.

Apply a validated multi-file patch to a staged candidate, not partially to the live
integration tree. Validate every path/digest/quota first; commit the whole proposal
or retain the prior snapshot. Only regular sanitized source files enter the export;
exclude .git, secrets, controller data and arbitrary untracked paths. Record its
manifest/digest. The source mount is controller-chosen, never a request argument.

read_artifact resolves an authorized project/mission reference, verifies digest and
availability, and streams bounded data; an object reference is not permission to
read a private path. Corrections/redaction follow STATE-001. Capture bounded logs
privately, filtering/redacting secrets at capture before persistence, public
summaries or model context, consistent with STATE-001. Never rely on a
container-generated report alone as a trusted actor/approval. Keep actual
process exit/timeout/OOM, expected collection/execution and environment digests in
controller-authored Evidence. Missing or ambiguous evidence cannot count as pass.

## 6. Qualification matrix and verification boundary

| ID | Required future effective-runtime evidence |
| --- | --- |
| SB-01 | Non-root identities, dropped capabilities, no-new-privileges, private namespaces and seccomp verified; prohibited syscalls/privilege gain denied |
| SB-02 | Root/source/harness writes, extra mounts, host sockets, home and controller memory access denied |
| SB-03 | External DNS/IP/metadata/host-gateway access denied; internal IPv4 HTTP/browser scenario succeeds without host port |
| SB-04 | Traversal, symlink/hardlink, case alias, special-file and path-swap races rejected by the real filesystem adapter |
| SB-05 | Cross-role/shared-config patch attempts denied; multi-file failure leaves source unchanged |
| SB-06 | CPU/memory+swap/PID/tmpfs limits enforced; unsupported capability and OOM fail closed |
| SB-07 | Deadline, log overflow, cancellation and orphan-container reconciliation preserve genuine failure/unknown evidence |
| SB-08 | Both browser profiles start with Chromium sandbox enabled under the exact seccomp derivative, private IPC and bounded noexec tmpfs |
| SB-09 | Untrusted config/plugins/environment cannot skip trusted suites, leak credentials or change expected collection; independent driver tampering attempts rejected |
| SB-10 | Qualified image/harness/host/secret/advisory change invalidates release; missing release never dispatches or pulls an image |
| SB-11 | Real fixture/API connection/body/lifetime bounds and visible client error behavior work inside the envelope |
| SB-12 | All six profiles execute expected suites with separate QA/security gates; replay references the same source/environment and stale evidence blocks delivery |

Run `python scripts/validate_sandbox_profiles.py` in the existing disposable
jsonschema validation environment. It validates policy/schema, role/profile/limit
consistency and synthetic path/request/envelope rejection examples. It starts no
container and is not evidence that SB-01–SB-12 pass. Earlier contract/state/limits
validators remain applicable. No new dependency or application code is installed.

T-016's sandbox/tool design is ready for review. Image creation and effective
qualification remain explicit implementation prerequisites, tracked by T-018/T-023
and the matrix above. GH-001 now specifies GitHub identity/integration; no deployment,
credential access, merge permission or arbitrary-code execution is authorized here.

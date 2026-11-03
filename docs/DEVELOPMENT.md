# Stage-nine executable foundation

SCAF-001, 2026-10-31, implements T-018 under the owner's explicit request to
complete stage nine. This is the first installable controller package and CLI.
It does not implement missions, real role invocation, durable project state,
the notes application, Docker qualification or a GitHub publication adapter.
Existing architecture/contracts still define those later capabilities.

## Install and inspect

Use Python 3.12.14 and uv 0.13.6. The supported interpreter range is 3.12.14+
within the 3.12 minor; only the recorded tested version/platform is verified.
Install the tooling explicitly using its official installation method; neither
CLI command downloads missing prerequisites. Then, from a clone:

```sh
uv python install 3.12.14
uv sync --locked --all-extras
uv run --no-sync multifullstackmade --version
uv run --no-sync multifullstackmade contracts --json
uv run --no-sync multifullstackmade doctor --json
```

The first command is an explicit Python setup action. If a suitable interpreter
is already installed, select it with `uv sync --python /path/to/python3.12`.
An ordinary install without optional packages is `uv sync --locked`; use all
extras for development/compatibility checks. `uv.lock` pins hashes/versions for
core, development and optional groups. The Hatchling build backend and uv CI
version are pinned too. Do not update dependencies as a side effect of a run.

`contracts` returns names, byte counts and SHA-256 digests for the fifteen bundled
design artifacts; it never treats their examples as executed tests or approval.
Its output contains no source contents or arbitrary file reads. Missing, oversized,
unexpected or incomplete bundle data produces exit 1 and a sanitized error. Exit 0
means catalog inspection succeeded, not that a team or sandbox works.

`doctor` reports Python/executable availability plus explicitly unavailable or
unverified engine/sandbox/publication capabilities. It reads no tokens, invokes no
external tools and performs no network/authentication/daemon probe. **Exit 1 is
expected at this milestone**, including when Docker's executable exists: there is
no implemented mission engine or qualified release. `available` for a tool means
only that an executable was found. CLI syntax errors use argparse exit 2. There
is intentionally no `run`, model-call, shell, merge or deployment command.

## Package and module boundaries

`src/multifullstackmade/cli.py` composes read-only application inspection services
with local adapters and renders text/JSON. Domain result records contain no CLI,
SDK, persistence or transport logic. Dependencies are explicit injected probes/loaders;
no placeholder interfaces, empty future modules or services are introduced.

The authoritative JSON/SQL remains in repository `contracts/`. Hatch includes
the exact bytes inside the wheel; an editable install reads this package's known
source checkout, never the caller's working directory. It is an internal bundled
catalog, not the SBX filesystem/role permission implementation. The build check
and clean wheel-install exercise detect missing payloads or accidental dependence
on the source tree. Source distributions retain setup sources and public documents.

Core dependencies are LangGraph + its SQLite adapter, Pydantic v2 and jsonschema.
`provider` adds the OpenAI package, `notes` adds FastAPI/Uvicorn, and `browser`
adds the Python Playwright test integration. These optional packages are locked
and import-checked; no client/server or Chromium process is started. There is no
frontend Node build stack or installed browser binary.

The dependency smoke test executes a tiny trusted one-node graph with an in-memory
SQLite checkpointer, and checks the resulting saved state. This proves the selected
Python/library interfaces work together; it is not T-019 mission persistence,
restart reconciliation, a private project database or a five-role demo. Foundation
tests deny network connections and disable tracing; no live model/provider is used.

## Required checks

```sh
uv sync --locked --all-extras
uv run --no-sync ruff check src tests scripts/verify_repository.py scripts/check_secrets.py scripts/check_wheel.py
uv run --no-sync ruff format --check src tests scripts/verify_repository.py scripts/check_secrets.py scripts/check_wheel.py
uv run --no-sync mypy
uv run --no-sync pytest
uv run --no-sync python scripts/verify_repository.py
uv run --no-sync python scripts/validate_contracts.py
uv run --no-sync python scripts/validate_state_design.py
uv run --no-sync python scripts/validate_execution_limits.py
uv run --no-sync python scripts/validate_sandbox_profiles.py
uv run --no-sync python scripts/validate_github_delivery.py
uv run --no-sync python scripts/check_secrets.py
uv build --no-build-isolation
uv run --no-sync python scripts/check_wheel.py
git diff --check
```

Format/lint/type scope is the new controller, tests and new verification helpers;
the earlier design validators retain their existing style. Their examples remain
shape/design checks, not application acceptance. The repository helper verifies
local links, syntax, task identity and fingerprints from the pinned upstream policy.
It requires a Git checkout; package inspection itself works without Git or a checkout.

The secret scan disables online credential verification. The two public upstream
policy fingerprints in the repository helper have precise inline allowlist comments;
they are SHA-256 identifiers, not credentials. No broad file exclusion or automatic
baseline is used. Other findings fail without printing potential secret values.
Never mark a genuine credential safe to make a check pass.

Audit the complete resolved environment without sending project source:

```sh
uv export --locked --all-extras --no-emit-project -o /tmp/multifullstackmade-audit.txt
uv run --no-sync pip-audit --require-hashes --disable-pip --strict --vulnerability-service osv --timeout 30 -r /tmp/multifullstackmade-audit.txt
```

Audit uses OSV public package/version advisory queries. With OSV, require-hashes
checks hash presence; actual artifact hash verification comes from locked uv sync
and the fresh-install hash check, not from the advisory query. An unavailable audit service
is reported as a failed/unavailable check, not a security pass. A clear result is
an observation at that time, not a guarantee against future vulnerabilities.

The foundation CI workflow uses immutable official action commits, locked Python/uv,
read-only contents permission, no persisted checkout credentials, a bounded timeout
and no model/publication secret. It runs on feature-branch pushes and PRs, including
drafts. It checks the controller foundation only; it does not qualify generated-code
containers or supply the GH-001 product-mission native-check manifest.

## Verify installation outside the checkout

After a build, export locked core requirements, create a fresh temporary environment,
install those requirements with hashes, then the wheel with `--no-deps`. Run `uv pip
check` and the two CLI inspection commands from outside the source directory. CI
contains the exact sequence. Hash verification may require fetching original
registry wheels even when an extracted cache exists; the local project wheel
itself installs offline. No package is published to PyPI by this build or workflow.

Keep `.venv`, `dist`, caches and all private state out of Git. Use a fresh or empty
dist directory for a build so the wheel check cannot select an old artifact. There
is no deployed service/database to roll back. Recover source through a revert PR;
recreate the environment from the matching lockfile, not from a mixed installed state.

Sources: [uv locked sync](https://docs.astral.sh/uv/concepts/projects/sync/),
[uv Python setup](https://docs.astral.sh/uv/guides/install-python/) and
[Hatch forced inclusion](https://hatch.pypa.io/latest/config/build/#forced-inclusion).
Actual check results and compatibility versions belong in the milestone PR/report.

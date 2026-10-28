# Contributing

The project is in design / pre-MVP. There is no application to install or test yet.

Read [AGENTS.md](AGENTS.md) and the task-relevant parts of [PROJECT.md](PROJECT.md)
before contributing. The engineering policy applies across design, implementation,
review, and delivery. The project brief records current authorization and open
decisions; a planned roadmap item is not automatic authorization to implement it.

## Proposals

Open an issue describing the problem, a concrete example, the proposed behavior,
and how it would be verified. Check existing issues before starting substantial
work. Scope and architecture proposals should be discussed before implementation.

English and Persian discussions are welcome. Keep the main README and design
documents accessible to the wider community, and update translated material when
the relevant behavior changes.

## Pull requests

1. Fork the repository and create a focused branch from `main`.
2. Keep changes scoped to one problem and link the relevant issue.
3. Explain the resulting behavior and include meaningful validation evidence.
4. Update documentation and clearly distinguish plans from working features.
5. Wait for maintainer review before merging.

Do not push directly to `main` or force-push shared history (AUT-07). Before
committing, inspect the final diff and include only intended, verified changes
(AUT-08). Use meaningful milestone commits, record checkpoint references in the PR,
and report actual checks, failures, and remaining blockers (AUT-10–AUT-13).

Use rule IDs for applicable findings and material exceptions. An exception must
record its reason, impact, and mitigation; irrelevant infrastructure is not required.

Until executable code exists, validate Markdown links, consistency, and clarity.
Run `git diff --check` and review the changed files for sensitive data. Policy
updates must preserve their upstream provenance, rule requirements, and license
notice unless a deliberate change is documented. See PROJECT.md for the full
current verification scope.
Once code is introduced, its setup and required checks must be documented in the
same contribution. Do not claim a check passed when it was not executed.

## Data and credentials

Do not commit API keys, tokens, private repository contents, execution databases,
agent transcripts, or project memory containing private information. Use dummy
data for examples and keep local credentials outside version control.

## Releases

Use short-lived feature branches and version tags. Release and merge decisions
remain with the maintainers. No deployment permission is implied by a contribution.

## Updating the upstream policy

The adopted revision and local customizations are recorded in AGENTS.md. Inspect
later upstream changes and apply them through a dedicated branch and PR; do not
silently replace the local policy from a moving upstream branch. Preserve product
decisions and the upstream license notice.
